"""
Ansible filter plugin that joins a base string and a tail path safely.
If the base is falsy (None, empty, etc.), returns an empty string.
"""

def safe_join(base, tail):
    """
    Safely join base and tail into a path or URL.

    - base: the base string. If falsy, returns ''.
    - tail: the string to append. Leading/trailing slashes are handled.
    - On any exception, returns ''.
    """
    try:
        if not base:
            return ''
        base_str = str(base).rstrip('/')
        tail_str = str(tail).lstrip('/')
        return f"{base_str}/{tail_str}"
    except Exception:
        return ''


class FilterModule(object):
    def filters(self):
        return {
            'safe_join': safe_join,
        }
