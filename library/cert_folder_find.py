#!/usr/bin/python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.cert_utils import CertUtils

def cert_folder_find(module):
    domain = module.params['domain']
    cert_base_path = module.params['cert_base_path']
    debug = module.params['debug']

    cert_files = CertUtils.list_cert_files(cert_base_path)

    if debug:
        print(f"Found {len(cert_files)} cert.pem files under {cert_base_path}")

    matching_folders = []

    for cert_path in cert_files:
        cert_text = CertUtils.run_openssl(cert_path)
        if not cert_text:
            continue
        sans = CertUtils.extract_sans(cert_text)
        if debug:
            print(f"Checking {cert_path}: {sans}")
        for entry in sans:
            if CertUtils.matches(domain, entry):
                folder = os.path.basename(os.path.dirname(cert_path))
                matching_folders.append(folder)
                if debug:
                    print(f"Match found in folder: {folder}")
                break  # No need to check further SANs for this cert

    if not matching_folders:
        # No matching cert found
        module.exit_json(folder=None)

    # Prefer shortest and least-dashed folder name (SAN bundles often have more dashes)
    matching_folders = sorted(matching_folders, key=lambda f: (f.count('-'), len(f)))

    module.exit_json(folder=matching_folders[0])

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

    cert_folder_find(module)

if __name__ == '__main__':
    main()