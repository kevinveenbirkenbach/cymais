def get_oauth2_enabled(applications, application_id):
    # Retrieve the application dictionary based on the ID
    app = applications.get(application_id, {})
    # Retrieve the value for oauth2_proxy.enabled, default is False
    enabled = app.get('oauth2_proxy', {}).get('enabled', False)
    return bool(enabled)

def get_oidc_enabled(applications, application_id):
    # Retrieve the application dictionary based on the ID
    app = applications.get(application_id, {})
    # Retrieve the value for oidc.enabled, default is False
    enabled = app.get('oidc', {}).get('enabled', False)
    return bool(enabled)

def get_css_enabled(applications, application_id):
    # Retrieve the application dictionary based on the given application_id.
    app = applications.get(application_id, {})
    # Retrieve the 'enabled' value from the css key, defaulting to True if not present.
    enabled = app.get('css', {}).get('enabled', True)
    return bool(enabled)

class FilterModule(object):
    def filters(self):
        return {
            'get_css_enabled': get_css_enabled,
            'get_oidc_enabled': get_oidc_enabled,
            'get_oauth2_enabled': get_oauth2_enabled
        }