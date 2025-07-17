def get_docker_paths(path_docker_compose_instances: str, application_id: str) -> dict:
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
            'dockerfile':     f"{base}Dockerfile",
        }
    }

class FilterModule(object):
    def filters(self):
        return {
            'get_docker_paths':   get_docker_paths,
        }
