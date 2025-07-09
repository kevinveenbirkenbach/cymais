# drv-intel

## Description

This Ansible role installs Intel media drivers on systems that use the Pacman package manager (e.g., Arch Linux and derivatives). It ensures the `intel-media-driver` package is present and up-to-date.

## Overview

The `drv-intel` role leverages the `community.general.pacman` module to:

1. Update the package cache.
2. Install (or upgrade) the `intel-media-driver` package.
3. Verify that the driver is correctly installed and ready for use in media pipelines.

## Features

* Idempotent installation of Intel media drivers
* Automatic package cache update before installation
* Supports installation on any Pacman-based distribution

## Further Resources

* [Intel Media Driver upstream documentation](https://01.org/intel-media-sdk)
