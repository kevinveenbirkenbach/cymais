# Nginx Homepage Role

This Ansible role configures an Nginx server to serve a static homepage. It handles domain configuration, SSL certificate retrieval with Let's Encrypt, and cloning the homepage content from a Git repository.

## Requirements

- Ansible 2.9 or higher
- Nginx installed on the target machine
- Git installed on the target machine (if cloning a repo)
- `nginx-https` and `git` roles available or configured if they are used as dependencies

## Role Variables

- `nginx_homepage_root`: The directory where the homepage content will be stored (default: `/usr/share/nginx/homepage`)
- `domain`: The domain name for the Nginx server configuration
- `administrator_email`: The email used for SSL certificate registration with Let's Encrypt
- `nginx_homepage_repository_address`: The Git repository address containing the homepage content

## Dependencies

- `nginx-https`: A role for setting up an HTTPS server
- `git`: A role for installing Git

## Example Playbook

```yaml
- hosts: servers
  roles:
     - { role: nginx-static-repository, domain: 'example.com', administrator_email: 'admin@example.com' }
```

## Author Information
This role was created in 2023 by Kevin Veen Birkenbach.