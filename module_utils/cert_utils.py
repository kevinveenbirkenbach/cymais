#!/usr/bin/python

import os
import subprocess

class CertUtils:
    @staticmethod
    def run_openssl(cert_path):
        try:
            output = subprocess.check_output(
                ['openssl', 'x509', '-in', cert_path, '-noout', '-text'],
                universal_newlines=True
            )
            return output
        except subprocess.CalledProcessError:
            return ""

    @staticmethod
    def extract_sans(cert_text):
        dns_entries = []
        in_san = False
        for line in cert_text.splitlines():
            line = line.strip()
            if 'X509v3 Subject Alternative Name:' in line:
                in_san = True
                continue
            if in_san:
                if not line:
                    break
                dns_entries += [e.strip().replace('DNS:', '') for e in line.split(',') if e.strip()]
        return dns_entries

    @staticmethod
    def list_cert_files(cert_base_path):
        cert_files = []
        for root, dirs, files in os.walk(cert_base_path):
            if 'cert.pem' in files:
                cert_files.append(os.path.join(root, 'cert.pem'))
        return cert_files

    @staticmethod
    def matches(domain, san):
        """Check if the SAN entry matches the domain according to wildcard rules."""
        if san.startswith('*.'):
            base = san[2:]
            # Check if domain is direct subdomain (one label only)
            if domain.count('.') == base.count('.') + 1 and domain.endswith('.' + base):
                return True
            return False
        else:
            return domain == san
