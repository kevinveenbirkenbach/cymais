from get_app_conf import get_app_conf

def get_docker_image(applications, application_id, image_key: str = None):
    """
    Wrapper for compatibility: Compose the docker image:version string.
    Raises error if value missing, like before.
    """
    image_key = image_key if image_key else application_id
    image = get_app_conf(applications, application_id, f"docker.images.{image_key}", strict=True)
    version = get_app_conf(applications, application_id, f"docker.versions.{image_key}", strict=True)
    return f"{image}:{version}"

class FilterModule(object):
    def filters(self):
        return {
            'get_docker_image': get_docker_image,
        }
