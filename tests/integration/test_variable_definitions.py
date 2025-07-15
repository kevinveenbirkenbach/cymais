import unittest
import os
import yaml
import re
from glob import glob

class TestVariableDefinitions(unittest.TestCase):
    def setUp(self):
        # Project root
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../../')
        )
        # Gather all definition files: include any .yml under vars/ and defaults/, plus group_vars/all
        self.var_files = (
            glob(os.path.join(self.project_root, 'roles/*/vars/*.yml')) +
            glob(os.path.join(self.project_root, 'roles/*/defaults/*.yml')) +
            glob(os.path.join(self.project_root, 'group_vars/all/*.yml'))
        )
        # Valid file extensions to scan for usages
        self.scan_extensions = {'.yml', '.j2'}

        # Regexes
        # Match simple Jinja variable usage: {{ var }} or with filters {{ var|filter }}
        self.simple_var_pattern = re.compile(r"{{\s*([a-zA-Z_]\w*)\s*(?:\|[^}]*)?}}")
        # Match Jinja2 set definitions: {% set var = ... %}
        self.jinja_set_def = re.compile(r'{%\s*set\s+([a-zA-Z_]\w*)\s*=')
        # Match Jinja2 for-loop variable definitions
        self.jinja_for_def = re.compile(r'{%\s*for\s+([a-zA-Z_]\w*)(?:\s*,\s*([a-zA-Z_]\w*))?\s+in')
        # Match Ansible set_fact mapping start
        self.ansible_set_fact = re.compile(r'^(?:\s*[-]\s*)?set_fact\s*:\s*$')
        # Match ansible vars block start
        self.ansible_vars_block = re.compile(r'^(?:\s*[-]\s*)?vars\s*:\s*$')
        # Match ansible loop_control loop_var definition
        self.ansible_loop_var = re.compile(r'^\s*loop_var\s*:\s*([a-zA-Z_]\w*)')
        # Match keys under a mapping block
        self.mapping_key = re.compile(r'^\s*([a-zA-Z_]\w*)\s*:\s*')

        # Build initial defined-vars set from all var definition files
        self.defined = set()
        for vf in self.var_files:
            try:
                with open(vf, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                if isinstance(data, dict):
                    self.defined.update(data.keys())
            except Exception:
                pass

    def test_all_used_vars_are_defined(self):
        undefined_uses = []

        # Walk all .yml and .j2 files
        for root, _, files in os.walk(self.project_root):
            for fn in files:
                ext = os.path.splitext(fn)[1]
                if ext not in self.scan_extensions:
                    continue

                path = os.path.join(root, fn)
                in_set_fact = False
                set_fact_indent = None
                in_vars_block = False
                vars_block_indent = None

                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for lineno, line in enumerate(f, 1):
                        stripped = line.lstrip()
                        indent = len(line) - len(stripped)
                        # Detect start of a set_fact mapping
                        if self.ansible_set_fact.match(stripped):
                            in_set_fact = True
                            set_fact_indent = indent
                            continue
                        # Inside set_fact, collect keys
                        if in_set_fact:
                            if indent > set_fact_indent and self.mapping_key.match(stripped):
                                key = self.mapping_key.match(stripped).group(1)
                                self.defined.add(key)
                                continue
                            else:
                                in_set_fact = False

                        # Detect start of a vars block under a task or play
                        if self.ansible_vars_block.match(stripped):
                            in_vars_block = True
                            vars_block_indent = indent
                            continue
                        # Inside vars block, collect keys and skip usage scanning
                        if in_vars_block:
                            if indent > vars_block_indent:
                                # any mapping key under vars is a definition
                                m = self.mapping_key.match(stripped)
                                if m:
                                    key = m.group(1)
                                    self.defined.add(key)
                                continue
                            else:
                                in_vars_block = False

                        # Detect loop_control loop_var definitions
                        m_loop = self.ansible_loop_var.match(stripped)
                        if m_loop:
                            self.defined.add(m_loop.group(1))

                        # collect any {% set foo = ... %} definitions
                        for m in self.jinja_set_def.finditer(line):
                            self.defined.add(m.group(1))
                        # collect any {% for var1, var2 in ... %} definitions
                        for m in self.jinja_for_def.finditer(line):
                            self.defined.add(m.group(1))
                            if m.group(2):
                                self.defined.add(m.group(2))

                        # collect simple usages only
                        for m in self.simple_var_pattern.finditer(line):
                            var = m.group(1)
                            # skip known Jinja builtins and whitelisted names
                            if var in ('lookup', 'role_name', 'domains', 'item', 'host_type', 'inventory_hostname', 'role_path', 'playbook_dir', 'ansible_become_password', 'inventory_dir'):
                                continue
                            if var not in self.defined:
                                # check fallback names defaults_var or default_var
                                if (f"defaults_{var}" in self.defined or
                                    f"default_{var}" in self.defined):
                                    continue
                                undefined_uses.append(
                                    f"{path}:{lineno}: '{{{{ {var} }}}}' used but not defined"
                                )

        if undefined_uses:
            self.fail(
                "Undefined Jinja2 variables found (no fallback 'default_' or 'defaults_' key):\n" +
                "\n".join(undefined_uses)
            )

if __name__ == '__main__':
    unittest.main()
