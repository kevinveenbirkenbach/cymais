#!/usr/bin/env python3

import os
import sys
import unittest

# Add filter_plugins/ to the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..", "filter_plugins")))

from docker_image import FilterModule

class TestGetDockerImage(unittest.TestCase):
    def setUp(self):
        self.get_docker_image = FilterModule().filters()["get_docker_image"]

    def test_version_from_docker_versions(self):
        applications = {
            "akaunting": {
                "version": "1.0.0",
                "docker": {
                    "images": { "akaunting": "docker.io/akaunting/akaunting" },
                    "versions": { "akaunting": "2.0.0" }
                }
            }
        }
        result = self.get_docker_image(applications, "akaunting", "akaunting")
        self.assertEqual(result, "docker.io/akaunting/akaunting:2.0.0")

    def test_fallback_to_application_version(self):
        applications = {
            "akaunting": {
                "version": "1.2.3",
                "docker": {
                    "images": { "akaunting": "ghcr.io/akaunting/akaunting" },
                    "versions": {}
                }
            }
        }
        result = self.get_docker_image(applications, "akaunting", "akaunting")
        self.assertEqual(result, "ghcr.io/akaunting/akaunting:1.2.3")

    def test_missing_image_raises_error(self):
        applications = {
            "akaunting": {
                "version": "1.0.0",
                "docker": {
                    "images": {},
                    "versions": {}
                }
            }
        }
        with self.assertRaises(ValueError):
            self.get_docker_image(applications, "akaunting", "akaunting")

    def test_missing_version_raises_error(self):
        applications = {
            "akaunting": {
                "docker": {
                    "images": { "akaunting": "some/image" },
                    "versions": {}
                }
            }
        }
        with self.assertRaises(ValueError):
            self.get_docker_image(applications, "akaunting", "akaunting")

if __name__ == "__main__":
    unittest.main()
