# Let's Encrypt Certificate Role

This Ansible role uses Certbot to obtain Let's Encrypt SSL/TLS certificates. It supports both dedicated and wildcard certificate requests based on domain conditions. It can also clean up (delete) dedicated certificates when cleanup mode is enabled.

## Features

- **Dedicated Certificate Request:**  
  Requests a certificate for a given domain using Certbot's `certonly` command with the webroot plugin.

- **Wildcard Certificate Request:**  
  When enabled, obtains a wildcard certificate for the primary domain (including both the primary domain and all its direct subdomains).

- **Certificate Cleanup:**  
  Provides an option to delete dedicated certificates if cleanup mode is active.

- **Run Once for Wildcard:**  
  Ensures that the wildcard certificate task runs only once to prevent duplicate requests.

## Tasks Overview

- **Receive Dedicated Certificate:**  
  Executes Certbot to request a dedicated certificate for `{{ domain }}` when a wildcard certificate is not applicable.

- **Receive Wildcard Certificate:**  
  Executes Certbot to request a wildcard certificate for `*{{ primary_domain }}` under the appropriate conditions.

- **Cleanup Dedicated Certificate:**  
  Runs Certbot's delete command to remove the dedicated certificate if cleanup mode is active.

- **Run Once Flag:**  
  Sets a fact to ensure that the wildcard certificate task is executed only once per playbook run.

## Author

This role is authored by [Kevin Veen-Birkenbach](https://www.veen.world).

---

Feel free to contribute or open issues if you have suggestions or encounter any problems with the role. Enjoy secure connections with Let's Encrypt and Ansible!