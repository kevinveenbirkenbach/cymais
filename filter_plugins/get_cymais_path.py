# filter_plugins/get_cymais_path.py

"""
This plugin provides filters to extract the CyMaIS directory and file identifiers
from a given role name. It assumes the role name is structured as 'dir_file'.
If the structure is invalid (e.g., missing or too many underscores), it raises an error.
These filters are used to support internal processing within CyMaIS.
"""

from ansible.errors import AnsibleFilterError


class CymaisPathExtractor:
    """Extracts directory and file parts from role names in the format 'dir_file'."""

    def __init__(self, value):
        self.value = value
        self._parts = self._split_value()

    def _split_value(self):
        parts = self.value.split("_")
        if len(parts) != 2:
            raise AnsibleFilterError(
                f"Invalid format: '{self.value}' must contain exactly one underscore (_)"
            )
        return parts

    def get_dir(self):
        return self._parts[0]

    def get_file(self):
        return self._parts[1]


def get_cymais_dir(value):
    return CymaisPathExtractor(value).get_dir()


def get_cymais_file(value):
    return CymaisPathExtractor(value).get_file()


class FilterModule(object):
    """Ansible filter plugin for CyMaIS path parsing."""

    def filters(self):
        return {
            "get_cymais_dir": get_cymais_dir,
            "get_cymais_file": get_cymais_file,
        }
