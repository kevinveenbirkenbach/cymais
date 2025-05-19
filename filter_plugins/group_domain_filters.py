from ansible.errors import AnsibleFilterError
import sys
import os
import yaml

class FilterModule(object):

    def filters(self):
        return {
            "add_domain_if_group": self.add_domain_if_group,
        }

    @staticmethod
    def add_domain_if_group(domains_dict, domain_key, domain_value, group_names):
        """
        Add {domain_key: domain_value} to domains_dict if either:
          1) domain_key is in group_names (direct inclusion), or
          2) domain_key is among collected application_id values of roles
             reachable from any group in group_names via recursive dependencies.

        Parameters:
          domains_dict: existing dict of domains
          domain_key:   name of the application to check
          domain_value: domain or dict/list of domains to assign
          group_names:  list of active group (role/application) names
        """
        try:
            result = dict(domains_dict)

            # Direct group match: if the application name itself is in group_names
            if domain_key in group_names:
                result[domain_key] = domain_value
                return result

            # Determine plugin directory based on filter plugin module if available
            plugin_dir = None
            for module in sys.modules.values():
                fm = getattr(module, 'FilterModule', None)
                if fm is not None:
                    try:
                        # Access staticmethod, compare underlying function
                        if getattr(fm, 'add_domain_if_group') is DomainFilterUtil.add_domain_if_group:
                            plugin_dir = os.path.dirname(module.__file__)
                            break
                    except Exception:
                        continue

            if plugin_dir:
                # The plugin_dir is the filter_plugins directory; project_root is one level up
                project_root = os.path.abspath(os.path.join(plugin_dir, '..'))
            else:
                # Fallback: locate project root relative to this utility file
                plugin_dir = os.path.dirname(__file__)
                project_root = os.path.abspath(os.path.join(plugin_dir, '..'))

            roles_dir = os.path.join(project_root, 'roles')

            # Collect all roles reachable from the active groups
            def collect_roles(role_name, collected):
                if role_name in collected:
                    return
                collected.add(role_name)
                meta_path = os.path.join(roles_dir, role_name, 'meta', 'main.yml')
                if os.path.isfile(meta_path):
                    with open(meta_path) as f:
                        meta = yaml.safe_load(f) or {}
                        for dep in meta.get('dependencies', []):
                            if isinstance(dep, str):
                                dep_name = dep
                            elif isinstance(dep, dict):
                                dep_name = dep.get('role') or dep.get('name')
                            else:
                                continue
                            collect_roles(dep_name, collected)

            included_roles = set()
            for grp in group_names:
                collect_roles(grp, included_roles)

            # Gather application_ids from each included role
            app_ids = set()
            for role in included_roles:
                vars_main = os.path.join(roles_dir, role, 'vars', 'main.yml')
                if os.path.isfile(vars_main):
                    with open(vars_main) as f:
                        vars_data = yaml.safe_load(f) or {}
                        app_id = vars_data.get('application_id')
                        if app_id:
                            app_ids.add(app_id)

            # Indirect inclusion: match by application_id
            if domain_key in app_ids:
                result[domain_key] = domain_value

            return result
        except Exception as exc:
            raise AnsibleFilterError(f"add_domain_if_group failed: {exc}")