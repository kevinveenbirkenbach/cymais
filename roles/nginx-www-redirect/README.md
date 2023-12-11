# README.md for nginx-www-redirect Role

## Overview
The `nginx-www-redirect` role is designed to automate the process of setting up redirects from `www.domain.tld` to `domain.tld` for all domains and subdomains configured within the `/etc/nginx/conf.d/` directory. This role dynamically identifies configuration files following the pattern `*domain.tld.conf` and creates corresponding redirection rules.

## Role Description
This role performs several key tasks:
1. **Find Configuration Files**: Locates all `.conf` files in the `/etc/nginx/conf.d/` directory that match the `*.*.conf` pattern, ensuring that only domain and subdomain configurations are selected.
   
2. **Filter Domain Names**: Processes each configuration file, extracting the domain names and removing both the `.conf` extension and the `/etc/nginx/conf.d/` path.

3. **Prepare Redirect Domain Mappings**: Transforms the filtered domain names into a source-target mapping format, where `source` is `www.domain.tld` and `target` is `domain.tld`.

4. **Include nginx-domain-redirect Role**: Applies the redirection configuration using the `nginx-domain-redirect` role with the dynamically generated domain mappings.

## Usage
To use this role, include it in your playbook and ensure that the `nginx-domain-redirect` role is available in your Ansible environment. No additional configuration is required as the role is designed to dynamically identify and process the domain configurations.

Example playbook:
```yaml
- hosts: web-servers
  roles:
    - nginx-www-redirect
```

## Requirements
- Ansible environment set up and configured to run roles.
- Access to the `/etc/nginx/conf.d/` directory on the target hosts.
- The `nginx-domain-redirect` role must be present and properly configured to handle the redirection mappings.

## Notes
- This role is designed to work in environments where domain and subdomain configurations follow the naming pattern `*domain.tld.conf`.
- It automatically excludes any configurations that begin with `www.`, preventing duplicate redirects.

---

This `nginx-www-redirect` role was crafted with insights and guidance provided by ChatGPT, an advanced AI language model from OpenAI. The development process, including the discussions with ChatGPT that shaped this role, can be [here](https://chat.openai.com/share/a68e3574-f543-467d-aea7-0895f0e00bbb) explored in detail.