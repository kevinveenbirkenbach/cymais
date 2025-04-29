#!/usr/bin/python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import subprocess
import time

class CertUtils:
    _domain_cert_mapping = None
    _cert_snapshot = None

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
        """RFC compliant SAN matching."""
        if san.startswith('*.'):
            base = san[2:]
            # Wildcard matches ONLY one additional label
            if domain == base:
                return False
            if domain.endswith('.' + base) and domain.count('.') == base.count('.') + 1:
                return True
            return False
        else:
            return domain == san


    @classmethod
    def build_snapshot(cls, cert_base_path):
        snapshot = []
        for cert_file in cls.list_cert_files(cert_base_path):
            try:
                stat = os.stat(cert_file)
                snapshot.append((cert_file, stat.st_mtime, stat.st_size))
            except FileNotFoundError:
                continue
        snapshot.sort()
        return snapshot

    @classmethod
    def snapshot_changed(cls, cert_base_path):
        current_snapshot = cls.build_snapshot(cert_base_path)
        if cls._cert_snapshot != current_snapshot:
            cls._cert_snapshot = current_snapshot
            return True
        return False

    @classmethod
    def refresh_cert_mapping(cls, cert_base_path, debug=False):
        cert_files = cls.list_cert_files(cert_base_path)
        mapping = {}
        for cert_path in cert_files:
            cert_text = cls.run_openssl(cert_path)
            if not cert_text:
                continue
            sans = cls.extract_sans(cert_text)
            folder = os.path.basename(os.path.dirname(cert_path))
            for san in sans:
                if san not in mapping:
                    mapping[san] = folder
        cls._domain_cert_mapping = mapping
        if debug:
            print(f"[DEBUG] Refreshed domain-to-cert mapping: {mapping}")

    @classmethod
    def ensure_cert_mapping(cls, cert_base_path, debug=False):
        if cls._domain_cert_mapping is None or cls.snapshot_changed(cert_base_path):
            cls.refresh_cert_mapping(cert_base_path, debug)

    @classmethod
    def find_cert_for_domain(cls, domain, cert_base_path, debug=False):
        cls.ensure_cert_mapping(cert_base_path, debug)

        exact_match = None
        wildcard_match = None

        for san, folder in cls._domain_cert_mapping.items():
            if san == domain:
                exact_match = folder
                break
            if san.startswith('*.'):
                base = san[2:]
                if domain.count('.') == base.count('.') + 1 and domain.endswith('.' + base):
                    wildcard_match = folder

        if exact_match:
            if debug:
                print(f"[DEBUG] Exact match for {domain} found in {exact_match}")
            return exact_match

        if wildcard_match:
            if debug:
                print(f"[DEBUG] Wildcard match for {domain} found in {wildcard_match}")
            return wildcard_match

        if debug:
            print(f"[DEBUG] No certificate folder found for {domain}")

        return None

