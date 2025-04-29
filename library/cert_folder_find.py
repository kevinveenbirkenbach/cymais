#!/usr/bin/python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.cert_utils import CertUtils

def find_matching_folders(domain, cert_files, flavor, debug):
    exact_matches = []
    wildcard_matches = []

    for cert_path in cert_files:
        cert_text = CertUtils.run_openssl(cert_path)
        if not cert_text:
            continue
        sans = CertUtils.extract_sans(cert_text)
        if debug:
            print(f"Checking {cert_path}: {sans}")
        for entry in sans:
            if CertUtils.matches(domain, entry):
                folder = os.path.dirname(cert_path)
                if entry.startswith('*.'):
                    wildcard_matches.append(folder)
                else:
                    exact_matches.append(folder)

    if flavor in ('san', 'dedicated'):
        return exact_matches or wildcard_matches
    elif flavor == 'wildcard':
        return wildcard_matches or exact_matches
    else:
        return []

def cert_folder_find(module):
    domain = module.params['domain']
    certbot_flavor = module.params['certbot_flavor']
    cert_base_path = module.params['cert_base_path']
    debug = module.params['debug']

    cert_files = CertUtils.list_cert_files(cert_base_path)

    if debug:
        print(f"Found {len(cert_files)} cert.pem files under {cert_base_path}")

    preferred = find_matching_folders(domain, cert_files, certbot_flavor, debug)

    if not preferred:
        module.fail_json(msg=f"No certificate covering domain {domain} found.")

    preferred = sorted(preferred, key=lambda p: (p.count('-'), len(p)))
    folder = os.path.basename(preferred[0])

    module.exit_json(folder=folder)

def main():
    module_args = dict(
        domain=dict(type='str', required=True),
        certbot_flavor=dict(type='str', required=True),
        cert_base_path=dict(type='str', required=False, default='/etc/letsencrypt/live'),
        debug=dict(type='bool', required=False, default=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    cert_folder_find(module)

if __name__ == '__main__':
    main()
