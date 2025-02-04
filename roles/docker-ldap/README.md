# Docker LDAP Role

This Ansible role provides a streamlined implementation of an LDAP server with TLS support. It leverages Docker Compose to deploy a pre-configured OpenLDAP server and phpLDAPadmin for easy management.

---

## 🚀 **Features**

- **Secure LDAP with TLS**:
  - Automatically configures TLS certificates for secure communication.
  - Provides configurable support for LDAPS on port 636.

- **phpLDAPadmin Integration**:
  - Includes a Dockerized phpLDAPadmin setup for easy user and group management.

- **Healthcheck Support**:
  - Ensures that the LDAP service is healthy and accessible using `ldapsearch`.

---

## 📋 **Requirements**

### Prerequisites
- A valid domain name.
- Ansible installed on the deployment host.
- Docker and Docker Compose installed on the target host.

---

## 🔧 **Role Variables**

### Key Variables
| Variable                      | Description                                              | Default Value                        |
|-------------------------------|----------------------------------------------------------|--------------------------------------|
| `application_id` | Name of the Docker Compose project.                     | `ldap`                               |
| `ldap_root`                   | Base DN for the LDAP directory.                         | `dc={{primary_domain_sld}},dc={{primary_domain_tld}}` |
| `ldap_admin_dn`               | Distinguished Name (DN) for the LDAP administrator.     | `cn={{applications.ldap.administrator_username}},{{ldap_root}}` |
| `cert_mount_directory`        | Directory to mount SSL/TLS certificates.                | `{{docker_compose.directories.instance}}/certs/` |
| `applications.ldap.administrator_username` | Username for the LDAP admin.                            | `admin`                              |
| `applications.ldap.administrator_password` | Password for the LDAP admin.                            | _Required_                           |
| `applications.ldap.phpldapadmin.version`          | Version of phpLDAPadmin Docker image.                   | `latest`                             |
| `applications.ldap.openldap.version`                | Version of OpenLDAP Docker image.                       | `latest`                             |

---

## 📂 **Role Structure**

```
roles/
  docker-ldap/
    README.md
    vars/
      main.yml
    tasks/
      main.yml
    templates/
      docker-compose.yml.j2
      nginx.stream.conf.j2
```

---

## 📖 **Usage**

Here’s an example playbook to use this role:

```yaml
- name: Deploy LDAP
  hosts: ldap_servers
  roles:
    - role: docker-ldap
      vars:
        docker_compose.directories.instance: "/opt/docker/ldap/"
        primary_domain_sld: "veen"
        primary_domain_tld: "world"
        applications.ldap.administrator_username: "administrator"
        applications.ldap.administrator_password: "secure_password_here"
        applications.ldap.phpldapadmin.version: "latest"
        applications.ldap.openldap.version: "latest"
```

### **Steps to Deploy:**
1. Clone your playbook repository to the target server.
2. Run the playbook:
   ```bash
   ansible-playbook -i inventory playbook.yml
   ```
3. Access phpLDAPadmin:
   - URL: `http://localhost:8080` (or your configured port)
   - Login: Use the admin DN and password.

---

## 🛠️ **Technical Details**

### **Services Configured**

1. **OpenLDAP**
   - TLS enabled on port 636.
   - Configuration driven by environment variables.

2. **phpLDAPadmin**
   - Accessible on port 443.
   - Simplifies LDAP management via a web interface.

3. **Healthchecks**
   - Uses `ldapsearch` to validate LDAP functionality.

### **Directory Structure**

The following directories are mounted in the container:
- **LDAP Data:** `data:/bitnami/openldap` for persistent data storage.

---

## 🔒 **Security Recommendations**
- Always use strong passwords for `applications.ldap.administrator_password`.
- Restrict access to phpLDAPadmin by binding it to `127.0.0.1` or using a reverse proxy.

---

## 📜 **References**
- [Bitnami OpenLDAP](https://hub.docker.com/r/bitnami/openldap)
- [phpLDAPadmin Documentation](https://github.com/leenooks/phpLDAPadmin/wiki/Docker-Container)
- [LDAP Account Manager](https://github.com/LDAPAccountManager/docker)
---


## 👨‍💻 **Author**

Kevin Veen-Birkenbach - [veen.world](https://www.veen.world)

Feel free to report issues, suggest features, or contribute to the repository! 😊