import re
from ansible.errors import AnsibleFilterError

class FilterModule(object):
    """
    Ansible Filter Plugin for Domain Processing

    This plugin provides filters to manage and transform domain configurations for applications:

    - generate_all_domains(domains_dict, include_www=True):
      Flattens nested domain values (string, list, or dict), optionally adds 'www.' prefixes,
      removes duplicates, and returns a sorted list of unique domains.

    - generate_base_sld_domains(domains_dict, redirect_mappings):
      Flattens domains and redirect mappings, extracts second-level + top-level domains (SLDs),
      deduplicates, and returns a sorted list of base domains.

    - canonical_domains_map(apps, primary_domain):
      Builds a mapping of application IDs to their canonical domains using
      DomainUtils.canonical_list, enforcing uniqueness and detecting conflicts.

    - alias_domains_map(apps, primary_domain):
      Generates alias domains for each application via DomainUtils.alias_list,
      based on their canonical domains and provided configurations.
    """

    def filters(self):
        return {
            'generate_all_domains':         self.generate_all_domains,
            'generate_base_sld_domains':    self.generate_base_sld_domains,
            'canonical_domains_map':        self.canonical_domains_map,
            'alias_domains_map':            self.alias_domains_map,
        }
        
    @staticmethod
    def parse_entry(domains_cfg, key, app_id):
        """
        Extract list of strings from domains_cfg[key], which may be dict or list.
        Returns None if key not in domains_cfg.
        Raises AnsibleFilterError on invalid type or empty/invalid values.
        """
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

    @staticmethod
    def default_domain(app_id, primary_domain):
        """
        Returns the default domain string for an application.
        """
        return f"{app_id}.{primary_domain}"

    @classmethod
    def canonical_list(cls, domains_cfg, app_id, primary_domain):
        """
        Returns the list of canonical domains: parsed entry or default.
        """
        domains = cls.parse_entry(domains_cfg, 'canonical', app_id)
        if domains is None:
            return [cls.default_domain(app_id, primary_domain)]
        return domains

    @classmethod
    def alias_list(cls, domains_cfg, app_id, primary_domain, canonical_domains=None):
        """
        Returns the list of alias domains based on:
          - explicit aliases entry
          - presence of canonical entry and default not in canonical
        Always ensures default domain in aliases when appropriate.
        """
        default = cls.default_domain(app_id, primary_domain)
        aliases = cls.parse_entry(domains_cfg, 'aliases', app_id) or []
        has_aliases = 'aliases' in domains_cfg
        has_canonical = 'canonical' in domains_cfg

        if has_aliases:
            if default not in aliases:
                aliases.append(default)
        elif has_canonical:
            # use provided canonical_domains if given otherwise parse
            canon = canonical_domains if canonical_domains is not None else cls.parse_entry(domains_cfg, 'canonical', app_id)
            if default not in (canon or []):
                aliases.append(default)
        # else: neither defined -> empty list
        return aliases


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

    def canonical_domains_map(self, apps, primary_domain):
        result = {}
        seen = {}
        for app_id, app_cfg in apps.items():
            domains_cfg = app_cfg.get('domains', {}) or {}
            domains = self.canonical_list(domains_cfg, app_id, primary_domain)
            for d in domains:
                if d in seen:
                    raise AnsibleFilterError(
                        f"Domain '{d}' is configured for both '{seen[d]}' and '{app_id}'"
                    )
                seen[d] = app_id
            result[app_id] = domains
        return result

    def alias_domains_map(self, apps, primary_domain):
        result = {}
        # wir können die canonical_map vorab holen…
        canonical_map = self.canonical_domains_map(apps, primary_domain)
        for app_id, app_cfg in apps.items():
            domains_cfg = app_cfg.get('domains', {}) or {}
            aliases = self.alias_list(
                domains_cfg,
                app_id,
                primary_domain,
                canonical_domains=canonical_map.get(app_id),
            )
            result[app_id] = aliases
        return result
