from jinja2 import Undefined


def safe_placeholders(template: str, mapping: dict = None) -> str:
    """
    Format a template like "{url}/logo.png".
    If mapping is provided (not None) and ANY placeholder is missing or maps to None/empty string, the function will raise KeyError.
    If mapping is None, missing placeholders or invalid templates return empty string.
    Numerical zero or False are considered valid values.
    Any other formatting errors return an empty string.
    """
    # Non-string templates yield empty
    if not isinstance(template, str):
        return ''

    class SafeDict(dict):
        def __getitem__(self, key):
            val = super().get(key, None)
            # Treat None or empty string as missing
            if val is None or (isinstance(val, str) and val == ''):
                raise KeyError(key)
            return val
        def __missing__(self, key):
            raise KeyError(key)

    silent = mapping is None
    data = mapping or {}
    try:
        return template.format_map(SafeDict(data))
    except KeyError:
        if silent:
            return ''
        raise
    except Exception:
        return ''

def safe_var(value):
    """
    Ansible filter: returns the value unchanged unless it's Undefined or None,
    in which case returns an empty string.
    Catches all exceptions and yields ''.
    """
    try:
        if isinstance(value, Undefined) or value is None:
            return ''
        return value
    except Exception:
        return ''

class FilterModule(object):
    def filters(self):
        return {
            'safe_var': safe_var,
            'safe_placeholders': safe_placeholders,
        }
