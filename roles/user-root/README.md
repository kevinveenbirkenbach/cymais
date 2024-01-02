Certainly! Below is a README file in English for an Ansible role that includes the tasks you've provided:
# Root User

## Overview
This Ansible role is designed to manage the generation and handling of an SSH key for the root user on a target system. It ensures that an SSH key is generated if it does not already exist and displays the public key. This role is particularly useful for setting up secure SSH access for root users in automated environments.

## Role Variables
- `run_once_user_root`: A variable to ensure that certain tasks are only run once. This is used for idempotency purposes.

## Tasks
1. **Check if the SSH key for root already exists**: Verifies the existence of an SSH public key for the root user.
2. **Generate a SSH key for root if it does not exist**: Generates a new SSH key pair (RSA 4096 bits) for the root user if it is not already present.
3. **Display the public SSH key**: Outputs the content of the generated public SSH key.
4. **Output the public SSH key**: Debug task to display the SSH public key in the Ansible output.
5. **Run the user_root tasks once**: Sets a fact to ensure that the tasks for generating and displaying the key are executed only once.

## Usage
To use this role, include it in your playbook and set any necessary variables in your playbook's `vars` section. Ensure you have the necessary permissions to execute tasks as the root user.

```yaml
- hosts: servers
  become: yes
  roles:
    - ssh_key_generator_root
```

## Important Notes
- Running this role will affect the root user's SSH configuration on the target system. Ensure you understand the implications of modifying root SSH keys.
- Always test the role in a controlled environment before deploying to production.
