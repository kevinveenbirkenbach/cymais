def is_feature_enabled(applications, feature:str, application_id:str)->bool:
    app = applications.get(application_id, {})
    enabled = app.get('features', {}).get(feature, False)
    return bool(enabled)

class FilterModule(object):
    def filters(self):
        return {
            'is_feature_enabled': is_feature_enabled,
        }