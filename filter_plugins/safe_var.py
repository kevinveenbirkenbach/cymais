# file: filter_plugins/safe_var.py

from jinja2 import Undefined

def safe_var(value):
    """
    Returns the original value unless it is None or Jinja2‐Undefined.
    Catches all exceptions and returns an empty string on error.
    """
    try:
        # If the value is an Undefined from Jinja2, treat it as missing
        if isinstance(value, Undefined):
            return ''
        # Treat None as missing as well
        if value is None:
            return ''
        # Otherwise return the actual value
        return value
    except Exception:
        # Catch any other errors and return empty string
        return ''

class FilterModule(object):
    def filters(self):
        return {
            'safe_var': safe_var
        }
