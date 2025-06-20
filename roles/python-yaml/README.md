# Python-Yaml

## Description

This Ansible role installs the **python-yaml** package on the target system. It ensures that the Python `yaml` library is available for loading and processing YAML files.

## Overview

Optimized for simplicity and idempotency, this role provides:
- Installation of the `python-yaml` package via the Pacman package manager.
- A mechanism to run the installation only once.

## Purpose

The purpose of this role is to reliably provide the Python-YAML package so that Python scripts can work with YAML files.

## Features

- **YAML Support:** Installs the `python-yaml` package, which supplies the `yaml` library for Python.  
- **Idempotency:** Uses a fact to ensure that the installation runs only on the first execution.  