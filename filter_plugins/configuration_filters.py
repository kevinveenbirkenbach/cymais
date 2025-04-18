def get_oauth2_enabled(applications, application_id):
    # Retrieve the application dictionary based on the ID
    app = applications.get(application_id, {})
    # Retrieve the value for oauth2_proxy.enabled, default is False
    enabled = app.get('features', {}).get('oauth2', False)
    return bool(enabled)

def get_oidc_enabled(applications, application_id):
    # Retrieve the application dictionary based on the ID
    app = applications.get(application_id, {})
    # Retrieve the value for oidc.enabled, default is False
    enabled = app.get('features', {}).get('oidc', False)
    return bool(enabled)

def get_features_iframe(applications, application_id):
    app = applications.get(application_id)
    enabled = app.features.iframe
    return bool(enabled)

def get_database_central_storage(applications, application_id):
    """
    Retrieve the type of the database from the application dictionary.
    The expected key structure is: applications[application_id]['database']['central_storage'].
    If not defined, None is returned.
    """
    app = applications.get(application_id, {})
    db_type = app.get('features', {}).get('database', False)
    return db_type

class FilterModule(object):
    def filters(self):
        return {
            'get_oidc_enabled': get_oidc_enabled,
            'get_oauth2_enabled': get_oauth2_enabled,
            'get_database_central_storage': get_database_central_storage,
            'get_features_iframe': get_features_iframe,
        }