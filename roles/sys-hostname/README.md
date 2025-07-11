# Hostname

This Ansible role ensures that the target host’s system hostname is set to the inventory hostname.

## Description

- Uses the built-in `hostname` module to apply the `inventory_hostname` value  
- Idempotent: only changes the system name if it differs  
- No external dependencies

## Overview

1. **Task**  
   - `set hostname to {{ inventory_hostname }}`  
     Applies the desired hostname.
2. **Module**  
   - Leverages Ansible’s [`hostname`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/hostname_module.html) module.

## Features

* Simple and lightweight
* Automatically adapts to your inventory names
* Safe to run repeatedly