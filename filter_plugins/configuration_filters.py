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

def get_docker_compose(path_docker_compose_instances: str, application_id: str) -> dict:
    """
    Build the docker_compose dict based on
    path_docker_compose_instances and application_id.
    """
    base = f"{path_docker_compose_instances}{application_id}/"

    return {
        'directories': {
            'instance': base,
            'env':      f"{base}.env/",
            'services': f"{base}services/",
            'volumes':  f"{base}volumes/",
            'config':   f"{base}config/",
        },
        'files': {
            'env':            f"{base}.env/env",
            'docker_compose': f"{base}docker-compose.yml",
        }
    }

class FilterModule(object):
    def filters(self):
        return {
            'is_feature_enabled':   is_feature_enabled,
            'get_csp_whitelist':    get_csp_whitelist,
            'get_csp_flags':        get_csp_flags,
            'get_docker_compose':   get_docker_compose,
        }