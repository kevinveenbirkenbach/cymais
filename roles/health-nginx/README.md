# health-nginx

## Overview
`health-nginx` is an Ansible role designed to send health reports for nginx configurations. It leverages Python scripting to check the status of nginx server configurations and reports back any issues. This role is especially useful for maintaining the health of nginx servers in a dynamic environment.

## Requirements
- Ansible
- Python with the `requests` module
- Access to the nginx configuration files

## Role Variables
- `health_nginx_folder`: The folder where the `health-nginx` script and related files are stored. Defaults to `"{{ path_administrator_scripts }}health-nginx/"`.

## Dependencies
This role depends on:
- `python-pip`: For installing Python packages.
- `systemd-notifier`: For notifying systemd in case of any failures.

## Example Playbook
```yaml
- hosts: servers
  roles:
    - { role: health-nginx }
```

## Usage
1. **Installation of Python Modules**: The role installs the required Python `requests` module.
2. **File and Directory Management**: It creates the necessary directories and files, including the `health-nginx.py` script.
3. **Service and Timer Templates**: Templates for `health-nginx.cymais.service` and `health-nginx.timer` are set up to automate the health checks.
4. **Running the Health Check**: The `health-nginx.py` script is executed to perform the health check. It iterates over nginx configuration files and sends a HEAD request to each domain/subdomain to verify its status. The script considers different expected status codes based on the domain or subdomain.

## Handler Details
- **reload health-nginx.cymais.service**: Reloads the `health-nginx.cymais.service` if there are any changes to the service file.
- **restart health-nginx.timer**: Restarts and enables the `health-nginx.timer` to schedule regular health checks.

## Additional Information
- For more details on nginx configurations, visit [nginx documentation](https://nginx.org/en/docs/).
- Learn more about Ansible's `uri_module` [here](https://docs.ansible.com/ansible/latest/modules/uri_module.html).

## Contributions
This role was created with the assistance of ChatGPT. The conversation can be found [here](https://chat.openai.com/share/4033be29-12a6-40a3-bf3c-fc5d57dba8cb) and [here](https://chat.openai.com/share/7f3766d1-9db7-4976-8fe9-68d1142c0a78).