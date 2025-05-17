import re
from ansible.errors import AnsibleFilterError

class FilterModule(object):
    """
    Custom Ansible filter plugin:
      - generate_all_domains: Flatten, dedupe, sort domains with optional www prefixes
      - generate_base_sld_domains: Extract unique sld.tld domains from values and redirect sources
    """

    def filters(self):
        return {
            'generate_all_domains': self.generate_all_domains,
            'generate_base_sld_domains': self.generate_base_sld_domains,
        }

    @staticmethod
    def generate_all_domains(domains_dict, include_www=True):
        """
        Transform a dict of domains (values: str, list, dict) into a flat list,
        optionally add 'www.' prefixes, dedupe and sort alphabetically.

        Avoids infinite loops by snapshotting initial domain list for www prefixes.
        """
        try:
            flat = FilterModule._flatten_domain_values(domains_dict)
            if include_www:
                # Snapshot original list to avoid extending while iterating
                original = list(flat)
                flat.extend([f"www.{d}" for d in original])
            return sorted(set(flat))
        except Exception as exc:
            raise AnsibleFilterError(f"generate_all_domains failed: {exc}")

    @staticmethod
    def generate_base_sld_domains(domains_dict, redirect_mappings):
        """
        Flatten domains_dict and redirect_mappings, extract second-level + top-level domains.
        redirect_mappings: list of dicts with key 'source'
        """
        try:
            flat = FilterModule._flatten_domain_values(domains_dict)
            for mapping in redirect_mappings or []:
                src = mapping.get('source')
                if isinstance(src, str):
                    flat.append(src)
                elif isinstance(src, list):
                    flat.extend(src)

            pattern = re.compile(r'^(?:.*\.)?([^.]+\.[^.]+)$')
            slds = {m.group(1) for d in flat if (m := pattern.match(d))}
            return sorted(slds)
        except Exception as exc:
            raise AnsibleFilterError(f"generate_base_sld_domains failed: {exc}")

    @staticmethod
    def _flatten_domain_values(domains_dict):
        """
        Helper to extract domain strings from dict values (str, list, dict).
        """
        flat = []
        for val in (domains_dict or {}).values():
            if isinstance(val, str):
                flat.append(val)
            elif isinstance(val, list):
                flat.extend(val)
            elif isinstance(val, dict):
                flat.extend(val.values())
        return flat
