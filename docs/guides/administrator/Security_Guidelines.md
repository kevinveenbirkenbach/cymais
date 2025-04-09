# Security Guidelines

CyMaIS is designed with security in mind. However, while following our guidelines can greatly improve your system’s security, no IT system can be 100% secure. Please report any vulnerabilities as soon as possible.

Additional to the user securitry guidelines administrators have additional responsibilities to secure the entire system:

- **Deploy on an Encrypted Server**  
  It is recommended to install CyMaIS on an encrypted server to prevent hosting providers from accessing end-user data. For a practical guide on setting up an encrypted server, refer to the [Hetzner Arch LUKS repository](https://github.com/kevinveenbirkenbach/hetzner-arch-luks) 🔐. (Learn more about [disk encryption](https://en.wikipedia.org/wiki/Disk_encryption) on Wikipedia.)

- **Centralized User Management & SSO**  
  For robust authentication and central user management, set up CyMaIS using Keycloak and LDAP.
  This configuration enables centralized [Single Sign-On (SSO)](https://en.wikipedia.org/wiki/Single_sign-on) (SSO), simplifying user management and boosting security.

- **Enforce 2FA and Use a Password Manager**  
  Administrators should also enforce [2FA](https://en.wikipedia.org/wiki/Multi-factor_authentication) and use a password manager with auto-generated passwords. We again recommend [KeePass](https://keepass.info/). The KeePass database can be stored securely in your Nextcloud instance and synchronized between devices.

- **Avoid Root Logins & Plaintext Passwords**  
  CyMaIS forbids logging in via the root user or using simple passwords. Instead, an SSH key must be generated and transferred during system initialization. When executing commands as root, always use `sudo` (or, if necessary, `sudo su`—but only if you understand the risks). (More information on [SSH](https://en.wikipedia.org/wiki/Secure_Shell) and [sudo](https://en.wikipedia.org/wiki/Sudo) is available on Wikipedia.)

- **Manage Inventories Securely**  
  Your inventories for running CyMaIS should be managed in a separate repository and secured with tools such as [Ansible Vault](https://en.wikipedia.org/wiki/Encryption) 🔒. Sensitive credentials must never be stored in plaintext; use a password file to secure these details.

- **Reporting Vulnerabilities**  
  If you discover a security vulnerability in CyMaIS, please report it immediately. We encourage proactive vulnerability reporting so that issues can be addressed as quickly as possible. Contact our security team at [security@cymais.cloud](mailto:security@cymais.cloud) 
  **DO NOT OPEN AN ISSUE.**

---

By following these guidelines, both end users and administrators can achieve a high degree of security. Stay vigilant, keep your systems updated, and report any suspicious activity. Remember: while we strive for maximum security, no system is completely infallible.
