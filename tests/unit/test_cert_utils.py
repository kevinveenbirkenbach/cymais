#!/usr/bin/env python3

import os
import sys

# Add module_utils/ to the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..", "module_utils")))

from module_utils.cert_utils import CertUtils

def test_matches():
    tests = [
        # Exact matches
        ("example.com", "example.com", True),
        ("www.example.com", "www.example.com", True),
        ("api.example.com", "api.example.com", True),

        # Wildcard matches
        ("sub.example.com", "*.example.com", True),
        ("www.example.com", "*.example.com", True),

        # Wildcard non-matches
        ("example.com", "*.example.com", False),  # base domain is not covered
        ("deep.sub.example.com", "*.example.com", False),  # too deep
        ("sub.deep.example.com", "*.deep.example.com", True),  # correct: one level below

        # Special cases
        ("deep.api.example.com", "*.api.example.com", True),
        ("api.example.com", "*.api.example.com", False),  # base not covered by wildcard

        # Completely different domains
        ("test.other.com", "*.example.com", False),
    ]

    passed = 0
    failed = 0

    for domain, san, expected in tests:
        result = CertUtils.matches(domain, san)
        if result == expected:
            print(f"✅ PASS: {domain} vs {san} -> {result}")
            passed += 1
        else:
            print(f"❌ FAIL: {domain} vs {san} -> {result} (expected {expected})")
            failed += 1

    print(f"\nSummary: {passed} passed, {failed} failed")

if __name__ == "__main__":
    test_matches()
