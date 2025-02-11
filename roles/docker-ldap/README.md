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

--
## Maintanance
### Show all Entires
```bash 
docker exec --env LDAP_ADMIN_PASSWORD="$LDAP_ADMIN_PASSWORD" -it openldap bash -c "ldapsearch -LLL -o ldif-wrap=no -x -D 'cn=administrator,dc=veen,dc=world' -w \"\$LDAP_ADMIN_PASSWORD\" -b 'dc=veen,dc=world'
```

### Delete Groups and Subgroup
To delete the group inclusive all subgroups use:
```bash
docker exec --env LDAP_ADMIN_PASSWORD="$LDAP_ADMIN_PASSWORD" -it openldap bash -c "ldapsearch -LLL -o ldif-wrap=no -x -D 'cn=administrator,dc=veen,dc=world' -w \"\$LDAP_ADMIN_PASSWORD\" -b 'ou=applications,ou=groups,dc=veen,dc=world' dn | sed -n 's/^dn: //p' | tac | while read -r dn; do echo \"Deleting \$dn\"; ldapdelete -x -D 'cn=administrator,dc=veen,dc=world' -w \"\$LDAP_ADMIN_PASSWORD\" \"\$dn\"; done"

```

--

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