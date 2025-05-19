from ansible.errors import AnsibleFilterError

class FilterModule(object):
    def filters(self):
        return {'canonical_domains_map': self.canonical_domains_map}

    def canonical_domains_map(self, apps, primary_domain):
        def parse_entry(domains_cfg, key, app_id):
            if key not in domains_cfg:
                return None
            entry = domains_cfg[key]
            if isinstance(entry, dict):
                values = list(entry.values())
            elif isinstance(entry, list):
                values = entry
            else:
                raise AnsibleFilterError(
                    f"Unexpected type for 'domains.{key}' in application '{app_id}': {type(entry).__name__}"
                )
            for d in values:
                if not isinstance(d, str) or not d.strip():
                    raise AnsibleFilterError(
                        f"Invalid domain entry in '{key}' for application '{app_id}': {d!r}"
                    )
            return values

        result = {}
        seen = {}

        for app_id, cfg in apps.items():
            domains_cfg = cfg.get('domains')
            if not domains_cfg or 'canonical' not in domains_cfg:
                default = f"{app_id}.{primary_domain}"
                if default in seen:
                    raise AnsibleFilterError(
                        f"Domain '{default}' is already configured for '{seen[default]}' and '{app_id}'"
                    )
                seen[default] = app_id
                result[app_id] = [default]
                continue

            entry = domains_cfg['canonical']

            if isinstance(entry, dict):
                for name, domain in entry.items():
                    if not isinstance(domain, str) or not domain.strip():
                        raise AnsibleFilterError(
                            f"Invalid domain entry in 'canonical' for application '{app_id}': {domain!r}"
                        )
                    if domain in seen:
                        raise AnsibleFilterError(
                            f"Domain '{domain}' is already configured for '{seen[domain]}' and '{app_id}'"
                        )
                    seen[domain] = app_id
                result[app_id] = entry.copy()

            elif isinstance(entry, list):
                for domain in entry:
                    if not isinstance(domain, str) or not domain.strip():
                        raise AnsibleFilterError(
                            f"Invalid domain entry in 'canonical' for application '{app_id}': {domain!r}"
                        )
                    if domain in seen:
                        raise AnsibleFilterError(
                            f"Domain '{domain}' is already configured for '{seen[domain]}' and '{app_id}'"
                        )
                    seen[domain] = app_id
                result[app_id] = list(entry)

            else:
                raise AnsibleFilterError(
                    f"Unexpected type for 'domains.canonical' in application '{app_id}': {type(entry).__name__}"
                )

        return result
