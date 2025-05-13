def is_feature_enabled(applications, feature: str, application_id: str) -> bool:
    """
    Check if a generic feature is enabled for the given application.
    """
    app = applications.get(application_id, {})
    return bool(app.get('features', {}).get(feature, False))


def get_csp_whitelist(applications, application_id: str, directive: str) -> list:
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


def get_csp_flags(applications, application_id: str, directive: str) -> list:
    """
    Read 'unsafe_eval' and 'unsafe_inline' flags from csp.flags.<directive>.
    Returns a list of string tokens, e.g. ["'unsafe-eval'", "'unsafe-inline'"].
    """
    app = applications.get(application_id, {})
    flags_config = app.get('csp', {}).get('flags', {}).get(directive, {})
    tokens = []
    if flags_config.get('unsafe_eval', False):
        tokens.append("'unsafe-eval'")
    if flags_config.get('unsafe_inline', False):
        tokens.append("'unsafe-inline'")
    return tokens


class FilterModule(object):
    def filters(self):
        return {
            'is_feature_enabled': is_feature_enabled,
            'get_csp_whitelist':    get_csp_whitelist,
            'get_csp_flags':        get_csp_flags,
        }