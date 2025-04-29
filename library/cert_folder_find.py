#!/usr/bin/python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: cert_folder_find
short_description: Find SSL certificate folder covering a given domain
description:
  - Searches through certificates to find a folder that covers the given domain.
options:
  domain:
    description:
      - Domain name to search for in the certificates.
    required: true
    type: str
  certbot_flavor:
    description:
      - Certificate type. Either 'san', 'wildcard', or 'dedicated'.
    required: true
    type: str
  cert_base_path:
    description:
      - Path where certificates are stored.
    required: false
    type: str
    default: /etc/letsencrypt/live
  debug:
    description:
      - Enable verbose debug output.
    required: false
    type: bool
    default: false
author:
  - Kevin Veen-Birkenbach
'''

EXAMPLES = r'''
- name: Find cert folder for matomo.cymais.cloud
  cert_folder_find:
    domain: "matomo.cymais.cloud"
    certbot_flavor: "san"
    cert_base_path: "/etc/letsencrypt/live"
  register: result
'''

RETURN = r'''
folder:
  description: The name of the folder covering the domain.
  type: str
  returned: always
'''

import os
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.cert_utils import CertUtils  # IMPORT

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
            if entry == domain:
                exact_matches.append(os.path.dirname(cert_path))
            elif entry.startswith('*.'):
                base = entry[2:]
                if domain.endswith('.' + base):
                    wildcard_matches.append(os.path.dirname(cert_path))

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

    if not preferred and certbot_flavor == 'san':
        if debug:
            print("Fallback: searching SAN matches without SAN structure parsing")
        for cert_path in cert_files:
            cert_text = CertUtils.run_openssl(cert_path)
            if f"DNS:{domain}" in cert_text:
                preferred.append(os.path.dirname(cert_path))

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
