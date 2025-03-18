# Administration

## Show Configuration
```bash
docker exec -it openldap bash -c "ldapsearch -LLL -Y EXTERNAL -H ldapi:/// -b 'cn=config'"
```

```bash
docker exec -it openldap bash -c "ldapsearch -LLL -Y EXTERNAL -H ldapi:/// -b 'cn=config' -s base '(objectClass=*)'"
```

```bash
docker exec -it openldap bash -c "ldapsearch -LLL -Y EXTERNAL -H ldapi:/// -b 'cn=config' -s base '(objectClass=olcModuleList)'"
```

### Databases Overview
```bash
docker exec -it openldap ldapsearch -Y EXTERNAL -H ldapi:/// -b "cn=config" "(olcDatabase=*)"
```

## Show all Entries
```bash 
docker exec -it openldap bash -c "ldapsearch -LLL -o ldif-wrap=no -x -D \"\$LDAP_ADMIN_DN\" -w \"\$LDAP_ADMIN_PASSWORD\" -b \"\$LDAP_ROOT\"";
```

### Delete Groups and Subgroup
To delete the group inclusive all subgroups use:
```bash
docker exec -it openldap bash -c "ldapsearch -LLL -o ldif-wrap=no -x -D \"\$LDAP_ADMIN_DN\" -w \"\$LDAP_ADMIN_PASSWORD\" -b \"ou=applications,ou=groups,\$LDAP_ROOT\" dn | sed -n 's/^dn: //p' | tac | while read -r dn; do echo \"Deleting \$dn\"; ldapdelete -x -D \"\$LDAP_ADMIN_DN\" -w \"\$LDAP_ADMIN_PASSWORD\" \"\$dn\"; done"

```