from ansible.errors import AnsibleFilterError

class FilterModule(object):
    """
    Custom filters for Content Security Policy generation and CSP-related utilities.
    """

    def filters(self):
        return {
            'get_csp_whitelist': self.get_csp_whitelist,
            'get_csp_flags': self.get_csp_flags,
            'build_csp_header': self.build_csp_header,
        }

    @staticmethod
    def get_csp_whitelist(applications, application_id, directive):
        """
        Return the list of extra hosts/URLs to whitelist for a given CSP directive.
        """
        app = applications.get(application_id, {})
        wl = app.get('csp', {}).get('whitelist', {}).get(directive, [])
        if isinstance(wl, list):
            return wl
        if wl:
            return [wl]
        return []

    @staticmethod
    def get_csp_flags(applications, application_id, directive):
        """
        Read 'unsafe_eval' and 'unsafe_inline' flags for a given CSP directive.
        Returns a list of string tokens, e.g. ["'unsafe-eval'", "'unsafe-inline'"]
        """
        app = applications.get(application_id, {})
        flags_config = app.get('csp', {}).get('flags', {}).get(directive, {})
        tokens = []
        if flags_config.get('unsafe_eval', False):
            tokens.append("'unsafe-eval'")
        if flags_config.get('unsafe_inline', False):
            tokens.append("'unsafe-inline'")
        return tokens

    @staticmethod
    def is_feature_enabled(applications, feature, application_id):
        """
        Check if a named feature is enabled for the given application.
        """
        app = applications.get(application_id, {})
        return bool(app.get('features', {}).get(feature, False))

    def build_csp_header(self, applications, application_id, domains, web_protocol='https', matomo_feature_name='matomo'):
        """
        Build the Content-Security-Policy header value dynamically based on application settings.

        :param applications: dict of application configurations
        :param application_id: the id of the application
        :param domains: dict mapping names (e.g., 'matomo') to domain strings
        :param web_protocol: protocol prefix for Matomo (default: 'https')
        :param matomo_feature_name: feature flag name for Matomo (default: 'matomo')
        :return: CSP header string, e.g. "default-src 'self'; script-src 'self' 'unsafe-eval' https://example.com; img-src * data: blob:;"
        """
        try:
            directives = [
                'default-src',
                'connect-src',
                'frame-ancestors',
                'frame-src',
                'script-src',
                'style-src',
                'font-src'
            ]
            parts = []

            for directive in directives:
                tokens = ["'self'"]
                # unsafe flags
                tokens += self.get_csp_flags(applications, application_id, directive)
                # Matomo integration
                if self.is_feature_enabled(applications, matomo_feature_name, application_id) \
                   and directive in ['script-src', 'connect-src']:
                    matomo_domain = domains.get('matomo')
                    if matomo_domain:
                        tokens.append(f"{web_protocol}://{matomo_domain}")
                # whitelist
                tokens += self.get_csp_whitelist(applications, application_id, directive)
                parts.append(f"{directive} {' '.join(tokens)};")

            # static img-src
            parts.append("img-src * data: blob:;")

            # join parts with space
            return ' '.join(parts)

        except Exception as exc:
            raise AnsibleFilterError(f"build_csp_header failed: {exc}")
