# filter_plugins/get_app_conf.py

import re
from ansible.errors import AnsibleFilterError

class AppConfigKeyError(AnsibleFilterError, ValueError):
    """
    Raised when a required application config key is missing (strict mode).
    Compatible with Ansible error handling and Python ValueError.
    """
    pass

def get_app_conf(applications, application_id, config_path, strict=True):
    def access(obj, key, path_trace):
        m = re.match(r"^([a-zA-Z0-9_]+)(?:\[(\d+)\])?$", key)
        if not m:
            raise AppConfigKeyError(
                f"Invalid key format in config_path: '{key}'\n"
                f"Full path so far: {'.'.join(path_trace)}\n"
                f"application_id: {application_id}\n"
                f"config_path: {config_path}"
            )
        k, idx = m.group(1), m.group(2)
        if isinstance(obj, dict):
            if k not in obj:
                if strict:
                    raise AppConfigKeyError(
                        f"Key '{k}' not found in dict at '{key}'\n"
                        f"Full path so far: {'.'.join(path_trace)}\n"
                        f"Current object: {repr(obj)}\n"
                        f"application_id: {application_id}\n"
                        f"config_path: {config_path}"
                    )
                return False
            obj = obj[k]
        else:
            if strict:
                raise AppConfigKeyError(
                    f"Expected dict for '{k}', got {type(obj).__name__} at '{key}'\n"
                    f"Full path so far: {'.'.join(path_trace)}\n"
                    f"Current object: {repr(obj)}\n"
                    f"application_id: {application_id}\n"
                    f"config_path: {config_path}"
                )
            return False
        if idx is not None:
            if not isinstance(obj, list):
                if strict:
                    raise AppConfigKeyError(
                        f"Expected list for '{k}[{idx}]', got {type(obj).__name__}\n"
                        f"Full path so far: {'.'.join(path_trace)}\n"
                        f"Current object: {repr(obj)}\n"
                        f"application_id: {application_id}\n"
                        f"config_path: {config_path}"
                    )
                return False
            i = int(idx)
            if i >= len(obj):
                if strict:
                    raise AppConfigKeyError(
                        f"Index {i} out of range for list at '{k}'\n"
                        f"Full path so far: {'.'.join(path_trace)}\n"
                        f"Current object: {repr(obj)}\n"
                        f"application_id: {application_id}\n"
                        f"config_path: {config_path}"
                    )
                return False
            obj = obj[i]
        return obj

    path_trace = [f"applications[{repr(application_id)}]"]
    try:
        obj = applications[application_id]
    except KeyError:
        if strict:
            raise AppConfigKeyError(
                f"Application ID '{application_id}' not found in applications dict.\n"
                f"path_trace: {path_trace}\n"
                f"applications keys: {list(applications.keys())}\n"
                f"config_path: {config_path}"
            )
        return False

    for part in config_path.split("."):
        path_trace.append(part)
        obj = access(obj, part, path_trace)
        if obj is False and not strict:
            return False
    return obj

class FilterModule(object):
    ''' CyMaIS application config extraction filters '''
    def filters(self):
        return {
            'get_app_conf': get_app_conf,
        }
