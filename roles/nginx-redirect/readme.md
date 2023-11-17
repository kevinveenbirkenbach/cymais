# Nginx Redirect Role

This Ansible role configures Nginx to perform 301 redirects from one domain to another. It handles SSL certificate retrieval for the source domains and sets up the Nginx configuration to redirect to the specified target domains.

## Requirements

- Ansible 2.9 or higher
- Nginx installed on the target machine
- Let's Encrypt for SSL certificate management

## Role Variables

- `domain_mappings`: A list of objects with `source` and `target` properties specifying the domains to redirect from and to.
- `administrator_email`: The email used for SSL certificate registration with Let's Encrypt.

## Dependencies

- `nginx-https`: A role for setting up HTTPS for Nginx
- `letsencrypt`: A role for managing SSL certificates with Let's Encrypt

## Example Playbook

```yaml
- hosts: servers
  roles:
    - { role: nginx-redirect, domain_mappings: [ {source: 'example.com', target: 'newdomain.com'} ] }

## Author Information
This role was created in 2023 by Kevin Veen Birkenbach.