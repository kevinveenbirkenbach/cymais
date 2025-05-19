def is_feature_enabled(applications: dict, feature: str, application_id: str) -> bool:
    """
    Return True if applications[application_id].features[feature] is truthy.
    """
    app = applications.get(application_id, {})
    return bool(app.get('features', {}).get(feature, False))

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
            'get_docker_compose':   get_docker_compose,
        }
