import re
from ansible.errors import AnsibleFilterError

class FilterModule(object):
    def filters(self):
        return {'generate_base_sld_domains': self.generate_base_sld_domains}

    def generate_base_sld_domains(self, domains_dict, redirect_mappings):
        """
        Flatten domains_dict und redirect_mappings, extrahiere SLDs (z.B. example.com),
        dedupe und sortiere.
        """
        def _flatten(domains):
            flat = []
            for v in (domains or {}).values():
                if isinstance(v, str):
                    flat.append(v)
                elif isinstance(v, list):
                    flat.extend(v)
                elif isinstance(v, dict):
                    flat.extend(v.values())
            return flat

        try:
            flat = _flatten(domains_dict)
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
