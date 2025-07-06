# driver-non-free

## Description

This Ansible role installs non-free GPU drivers on Arch Linux systems by invoking the `mhwd` utility. It ensures that the appropriate proprietary drivers for your PCI graphics hardware are installed and ready for use.

## Overview

- Uses the `ansible.builtin.shell` module to run `mhwd -a pci nonfree 0300`  
- Automatically detects your PCI graphics adapter and installs the recommended non-free driver  
- Designed to be run once per host to provision proprietary GPU support

## Features

- **Automatic Hardware Detection**  
  Leverages `mhwd`’s built-in auto-detect feature (`0300`) to select the correct driver.

- **Proprietary Driver Installation**  
  Installs the latest non-free GPU driver (e.g., NVIDIA, AMD) provided through Arch’s `mhwd` system.

- **Simple Execution**  
  Single-task role with minimal overhead.

## Further Resources

- [Manjaro Hardware Detection (mhwd) Documentation](https://wiki.manjaro.org/index.php/Hardware_Detection)  
- [Arch Linux mhwd Package](https://archlinux.org/packages/community/x86_64/manjaro-tools-mhwd/)  
- [Ansible Shell Module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/shell_module.html)  
