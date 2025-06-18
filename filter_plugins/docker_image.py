# filter_plugins/docker_image.py

def get_docker_image(applications, application_id, image_key):
    app = applications.get(application_id, {})
    docker = app.get("docker", {})
    images = docker.get("images", {})
    versions = docker.get("versions", {})
    version = versions.get(image_key) or app.get("version")
    image = images.get(image_key)

    if not image or not version:
        raise ValueError(f"Missing image or version for {application_id}:{image_key}")
    
    return f"{image}:{version}"

class FilterModule(object):
    def filters(self):
        return {
            'get_docker_image': get_docker_image,
        }
