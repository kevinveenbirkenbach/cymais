import yaml

def get_oauth2_enabled(applications:yaml, application_id:string):
    # Retrieve the application dictionary based on the ID
    app = applications.get(application_id, {})
    # Retrieve the value for oauth2_proxy.enabled, default is False
    enabled = app.get('oauth2_proxy', {}).get('enabled', False)
    return bool(enabled)

def get_oidc_enabled(applications:yaml, application_id:string):
    # Retrieve the application dictionary based on the ID
    app = applications.get(application_id, {})
    # Retrieve the value for oidc.enabled, default is False
    enabled = app.get('oidc', {}).get('enabled', False)
    return bool(enabled)

def get_css_enabled(applications:yaml, application_id:string):
    app = applications.get(application_id)
    enabled = app.get('css_enabled')
    return bool(enabled)

def get_landingpage_iframe_enabled(applications:yaml, application_id:string):
    app = applications.get(application_id)
    enabled = app.get('landingpage_iframe_enabled')
    return bool(enabled)

def get_matomo_tracking_enabled(applications:yaml, application_id:string):
    app = applications.get(application_id)
    enabled = app.get('matomo_tracking_enabled')
    return bool(enabled)

def get_database_central_storage(applications:yaml, application_id:string):
    """
    Retrieve the type of the database from the application dictionary.
    The expected key structure is: applications[application_id]['database']['central_storage'].
    If not defined, None is returned.
    """
    app = applications.get(application_id, {})
    db_type = app.get('database', {}).get('central_storage', False)
    return db_type

class FilterModule(object):
    def filters(self):
        return {
            'get_css_enabled': get_css_enabled,
            'get_oidc_enabled': get_oidc_enabled,
            'get_oauth2_enabled': get_oauth2_enabled,
            'get_database_central_storage': get_database_central_storage,
            'get_landingpage_iframe_enabled': get_landingpage_iframe_enabled,
            'get_matomo_tracking_enabled': get_matomo_tracking_enabled,
        }