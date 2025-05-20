import pytest
import sys, os
from pathlib import Path

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../cli")
    ),
)

# 2) Import from the cli package
import cli.create_credentials as gvc

class DummyProc:
    def __init__(self, returncode, stdout, stderr=''):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

# Monkeypatch subprocess.run for encrypt_with_vault
@pytest.fixture(autouse=True)
def mock_subprocess_run(monkeypatch):
    def fake_run(cmd, capture_output, text):
        name = None
        # find --name=<key> in args
        for arg in cmd:
            if arg.startswith("--name="):
                name = arg.split("=",1)[1]
        val = cmd[ cmd.index(name) - 1 ] if name else "key"
        # simulate Ansible output
        snippet = f"{name or 'key'}: !vault |\n    encrypted_{val}"
        return DummyProc(0, snippet)
    monkeypatch.setattr(gvc.subprocess, 'run', fake_run)

def test_wrap_existing_vaults():
    data = {
        'a': '$ANSIBLE_VAULT;1.1;AES256...blob',
        'b': {'c': 'normal', 'd': '$ANSIBLE_VAULT;1.1;AES256...other'},
        'e': ['x', '$ANSIBLE_VAULT;1.1;AES256...list']
    }
    wrapped = gvc.wrap_existing_vaults(data)
    assert isinstance(wrapped['a'], gvc.VaultScalar)
    assert isinstance(wrapped['b']['d'], gvc.VaultScalar)
    assert isinstance(wrapped['e'][1], gvc.VaultScalar)
    assert wrapped['b']['c'] == 'normal'
    assert wrapped['e'][0] == 'x'

@pytest.mark.parametrize("pairs,expected", [
    (['k=v'], {'k': 'v'}),
    (['a.b=1', 'c=two'], {'a.b': '1', 'c': 'two'}),
    (['noeq'], {}),
])
def test_parse_overrides(pairs, expected):
    assert gvc.parse_overrides(pairs) == expected

def test_apply_schema_and_vault(tmp_path):
    schema = {
        'cred': {'description':'d','algorithm':'plain','validation':{}},
        'nested': {'inner': {'description':'d2','algorithm':'plain','validation':{}}}
    }
    inv = {}
    updated = gvc.apply_schema(schema, inv, 'app', {}, 'pwfile')
    apps = updated['applications']['app']
    assert isinstance(apps['cred'], gvc.VaultScalar)
    assert isinstance(apps['nested']['inner'], gvc.VaultScalar)

def test_encrypt_leaves_and_credentials():
    branch = {'p':'v','nested':{'q':'u'}}
    gvc.encrypt_leaves(branch, 'pwfile')
    assert isinstance(branch['p'], gvc.VaultScalar)
    assert isinstance(branch['nested']['q'], gvc.VaultScalar)

    inv = {'credentials':{'a':'b'}, 'x':{'credentials':{'c':'d'}}}
    gvc.encrypt_credentials_branch(inv, 'pwfile')
    assert isinstance(inv['credentials']['a'], gvc.VaultScalar)
    assert isinstance(inv['x']['credentials']['c'], gvc.VaultScalar)
