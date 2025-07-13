class FilterModule(object):
    ''' Custom filter to safely check if a docker service is enabled for an application_id '''

    def filters(self):
        return {
            'is_docker_service_enabled': self.is_docker_service_enabled
        }

    @staticmethod
    def is_docker_service_enabled(applications, application_id, service_name):
        """
        Returns True if applications[application_id].docker.services[service_name].enabled is truthy,
        otherwise returns False (even if intermediate keys are missing).
        """
        try:
            return bool(
                applications
                and application_id in applications
                and applications[application_id].get('docker', {})
                .get('services', {})
                .get(service_name, {})
                .get('enabled', False)
            )
        except Exception:
            return False
