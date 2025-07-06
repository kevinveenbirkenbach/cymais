#!/usr/bin/python
import os
import sys
from ansible.errors import AnsibleFilterError

class FilterModule(object):
    def filters(self):
        return {'get_url': self.get_url}

    def get_url(self, domains, application_id, protocol):
        # 1) module_utils-Verzeichnis in den Pfad aufnehmen
        plugin_dir   = os.path.dirname(__file__)
        project_root = os.path.dirname(plugin_dir)
        module_utils = os.path.join(project_root, 'module_utils')
        if module_utils not in sys.path:
            sys.path.append(module_utils)

        # 2) jetzt domain_utils importieren
        try:
            from domain_utils import get_domain
        except ImportError as e:
            raise AnsibleFilterError(f"could not import domain_utils: {e}")

        # 3) Validierung und Aufruf
        if not isinstance(protocol, str):
            raise AnsibleFilterError("Protocol must be a string")
        return f"{protocol}://{ get_domain(domains, application_id) }"
