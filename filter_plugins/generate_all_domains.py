import os
from ansible.errors import AnsibleFilterError

class FilterModule(object):
    """
    Custom Ansible filter to generate a flattened, deduplicated,
    and sorted list of domains, with optional 'www.' prefixes.
    """

    def filters(self):
        return {
            'generate_all_domains': self.generate_all_domains,
        }

    @staticmethod
    def generate_all_domains(domains_dict, include_www=True):
        """
        Transform a dict of domains into a flat list of domain strings.
        Values in domains_dict may be strings, lists, or dicts.
        If include_www is True, also generate "www." variants.
        The final list is deduplicated and sorted alphabetically.

        :param domains_dict: dict where each value is str, list, or dict of domains
        :param include_www:  bool indicating if 'www.' prefixes should be added
        :return:              sorted list of unique domain names
        """
        try:
            flat = []
            for val in domains_dict.values():
                if isinstance(val, str):
                    flat.append(val)
                elif isinstance(val, list):
                    flat.extend(val)
                elif isinstance(val, dict):
                    flat.extend(val.values())
                else:
                    # skip unsupported types
                    continue

            if include_www:
                flat.extend(['www.' + d for d in flat])

            # dedupe and sort
            return sorted(set(flat))

        except Exception as exc:
            raise AnsibleFilterError(f"generate_all_domains failed: {exc}")