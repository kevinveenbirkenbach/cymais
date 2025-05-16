from ansible.errors import AnsibleFilterError

class FilterModule(object):
    """
    Custom filters for conditional domain assignments
    """

    def filters(self):
        return {
            "add_domain_if_group": self.add_domain_if_group,
        }

    @staticmethod
    def add_domain_if_group(domains_dict, domain_key, domain_value, group_names):
        """
        Add {domain_key: domain_value} to domains_dict
        only if domain_key is in group_names.

        Usage in Jinja:
          {{ {} 
               | add_domain_if_group('akaunting', 'akaunting.' ~ primary_domain, group_names) }}
        """
        try:
            result = dict(domains_dict)
            if domain_key in group_names:
                result[domain_key] = domain_value
            return result
        except Exception as exc:
            raise AnsibleFilterError(f"add_domain_if_group failed: {exc}")
