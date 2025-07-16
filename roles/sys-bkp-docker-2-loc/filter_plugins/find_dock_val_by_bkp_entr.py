from ansible.errors import AnsibleFilterError

def find_dock_val_by_bkp_entr(applications, search_string, mapped_entry):
    """
    Iterates over all applications and their docker.services, finds services where
    .backup[search_string] exists (and is truthy), and returns the value of
    .[mapped_entry] for each.

    :param applications: dict of applications
    :param search_string: string, the backup subkey to search for (e.g., "enabled")
    :param mapped_entry: string, the key to return from the service (e.g., "name")
    :return: list of mapped_entry values
    """
    if not isinstance(applications, dict):
        raise AnsibleFilterError("applications must be a dict")

    results = []

    for app in applications.values():
        docker = app.get("docker", {})
        services = docker.get("services", {})
        if not isinstance(services, dict):
            continue
        for svc in services.values():
            backup = svc.get("backup", {})
            # only match if .backup[search_string] is set and truthy
            if isinstance(backup, dict) and backup.get(search_string):
                mapped_value = svc.get(mapped_entry)
                if mapped_value is not None:
                    results.append(mapped_value)
    return results

class FilterModule(object):
    def filters(self):
        return {
            'find_dock_val_by_bkp_entr': find_dock_val_by_bkp_entr,
        }
