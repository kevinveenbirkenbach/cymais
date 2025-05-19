from ansible.errors import AnsibleFilterError
import os
import sys
import yaml

class FilterModule(object):
    def filters(self):
        return {
            'applications_if_group_and_deps': self.applications_if_group_and_deps,
        }

    def applications_if_group_and_deps(self, applications, group_names):
        """
        Return only those applications whose key is either:
          1) directly in group_names, or
          2) the application_id of any role reachable (recursively)
             from any group in group_names via meta/dependencies.
        Expects:
          - applications: dict mapping application_id → config
          - group_names: list of active role names
        """
        # validate inputs
        if not isinstance(applications, dict):
            raise AnsibleFilterError(f"Expected applications as dict, got {type(applications).__name__}")
        if not isinstance(group_names, (list, tuple)):
            raise AnsibleFilterError(f"Expected group_names as list/tuple, got {type(group_names).__name__}")

        # locate roles directory (assume plugin sits in filter_plugins/)
        plugin_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(plugin_dir, '..'))
        roles_dir = os.path.join(project_root, 'roles')

        # recursively collect all roles reachable from the given groups
        def collect_roles(role, seen):
            if role in seen:
                return
            seen.add(role)
            meta_file = os.path.join(roles_dir, role, 'meta', 'main.yml')
            if not os.path.isfile(meta_file):
                return
            try:
                with open(meta_file) as f:
                    meta = yaml.safe_load(f) or {}
            except Exception:
                return
            for dep in meta.get('dependencies', []):
                if isinstance(dep, str):
                    dep_name = dep
                elif isinstance(dep, dict):
                    dep_name = dep.get('role') or dep.get('name')
                else:
                    continue
                collect_roles(dep_name, seen)

        included_roles = set()
        for grp in group_names:
            collect_roles(grp, included_roles)

        # gather application_ids from those roles
        included_app_ids = set()
        for role in included_roles:
            vars_file = os.path.join(roles_dir, role, 'vars', 'main.yml')
            if not os.path.isfile(vars_file):
                continue
            try:
                with open(vars_file) as f:
                    vars_data = yaml.safe_load(f) or {}
            except Exception:
                continue
            app_id = vars_data.get('application_id')
            if isinstance(app_id, str) and app_id:
                included_app_ids.add(app_id)

        # build filtered result: include any application whose key is in group_names or in included_app_ids
        result = {}
        for app_key, cfg in applications.items():
            if app_key in group_names or app_key in included_app_ids:
                result[app_key] = cfg

        return result