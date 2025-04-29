#!/usr/bin/python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.cert_utils import CertUtils

def cert_exists(domain, cert_files, debug=False):
    for cert_path in cert_files:
        cert_text = CertUtils.run_openssl(cert_path)
        if not cert_text:
            continue
        sans = CertUtils.extract_sans(cert_text)
        if debug:
            print(f"Checking {cert_path}: {sans}")
        for entry in sans:
            if CertUtils.matches(domain, entry):
                return True
    return False

def cert_check_exists(module):
    domain = module.params['domain']
    cert_base_path = module.params['cert_base_path']
    debug = module.params['debug']

    cert_files = CertUtils.list_cert_files(cert_base_path)

    exists = cert_exists(domain, cert_files, debug)

    module.exit_json(exists=exists)

def main():
    module_args = dict(
        domain=dict(type='str', required=True),
        cert_base_path=dict(type='str', required=False, default='/etc/letsencrypt/live'),
        debug=dict(type='bool', required=False, default=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    cert_check_exists(module)

if __name__ == '__main__':
    main()
