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
        # Gather all definition files recursively under vars/ and defaults/, plus group_vars/all
        self.var_files = []
        patterns = [
            os.path.join(self.project_root, 'roles', '*', 'vars', '**', '*.yml'),
            os.path.join(self.project_root, 'roles', '*', 'defaults', '**', '*.yml'),
            os.path.join(self.project_root, 'group_vars', 'all', '*.yml'),
        ]
        for pat in patterns:
            self.var_files.extend(glob(pat, recursive=True))

        # Valid file extensions to scan for definitions and usages
        self.scan_extensions = {'.yml', '.j2'}

        # Regex patterns
        self.simple_var_pattern = re.compile(r"{{\s*([a-zA-Z_]\w*)\s*(?:\|[^}]*)?}}")
        self.jinja_set_def = re.compile(r'{%\s*-?\s*set\s+([a-zA-Z_]\w*)\s*=')
        self.jinja_for_def = re.compile(r'{%\s*-?\s*for\s+([a-zA-Z_]\w*)(?:\s*,\s*([a-zA-Z_]\w*))?\s+in')
        self.ansible_set_fact = re.compile(r'^(?:\s*[-]\s*)?set_fact\s*:\s*$')
        self.ansible_vars_block = re.compile(r'^(?:\s*[-]\s*)?vars\s*:\s*$')
        self.ansible_loop_var = re.compile(r'^\s*loop_var\s*:\s*([a-zA-Z_]\w*)')
        self.mapping_key = re.compile(r'^\s*([a-zA-Z_]\w*)\s*:\s*')

        # Initialize defined set from var files
        self.defined = set()
        for vf in self.var_files:
            try:
                with open(vf, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                if isinstance(data, dict):
                    self.defined.update(data.keys())
            except Exception:
                pass

        # Phase 1: scan all files to collect inline definitions
        for root, _, files in os.walk(self.project_root):
            for fn in files:
                ext = os.path.splitext(fn)[1]
                if ext not in self.scan_extensions:
                    continue

                path = os.path.join(root, fn)
                in_set_fact = False
                set_fact_indent = 0
                in_vars_block = False
                vars_block_indent = 0
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        stripped = line.lstrip()
                        indent = len(line) - len(stripped)
                        # set_fact keys
                        if self.ansible_set_fact.match(stripped):
                            in_set_fact = True
                            set_fact_indent = indent
                            continue
                        if in_set_fact:
                            if indent > set_fact_indent and stripped.strip():
                                m = self.mapping_key.match(stripped)
                                if m:
                                    self.defined.add(m.group(1))
                                continue
                            else:
                                in_set_fact = False
                        # vars block keys
                        if self.ansible_vars_block.match(stripped):
                            in_vars_block = True
                            vars_block_indent = indent
                            continue
                        if in_vars_block:
                            # skip blank lines within vars block
                            if not stripped.strip():
                                continue
                            if indent > vars_block_indent:
                                m = self.mapping_key.match(stripped)
                                if m:
                                    self.defined.add(m.group(1))
                                continue
                            else:
                                in_vars_block = False
                        # loop_var
                        m_loop = self.ansible_loop_var.match(stripped)
                        if m_loop:
                            self.defined.add(m_loop.group(1))

                        # register
                        m_reg = re.match(r'^\s*register\s*:\s*([a-zA-Z_]\w*)', stripped)
                        if m_reg:
                            self.defined.add(m_reg.group(1))
                        # jinja set
                        for m in self.jinja_set_def.finditer(line):
                            self.defined.add(m.group(1))
                        # jinja for
                        for m in self.jinja_for_def.finditer(line):
                            self.defined.add(m.group(1))
                            if m.group(2):
                                self.defined.add(m.group(2))

    def test_all_used_vars_are_defined(self):
        undefined_uses = []
        # Phase 2: scan all files for usages
        for root, _, files in os.walk(self.project_root):
            for fn in files:
                ext = os.path.splitext(fn)[1]
                if ext not in self.scan_extensions:
                    continue
                path = os.path.join(root, fn)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for lineno, line in enumerate(f, 1):
                        for m in self.simple_var_pattern.finditer(line):
                            var = m.group(1)
                            # skip builtins and whitelisted names
                            if var in ('lookup', 'role_name', 'domains', 'item', 'host_type',
                                       'inventory_hostname', 'role_path', 'playbook_dir',
                                       'ansible_become_password', 'inventory_dir', 'ansible_memtotal_mb'):
                                continue
                            # skip defaults_var fallback
                            if var not in self.defined and \
                               f"default_{var}" not in self.defined and \
                               f"defaults_{var}" not in self.defined:
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