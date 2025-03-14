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

## Show all Entries
```bash 
docker exec --env LDAP_ADMIN_PASSWORD="$LDAP_ADMIN_PASSWORD" LDAP_DN_BASE="$LDAP_DN_BASE" -it openldap bash -c "ldapsearch -LLL -o ldif-wrap=no -x -D \"cn=administrator,\$LDAP_DN_BASE\" -w \"\$LDAP_ADMIN_PASSWORD\" -b \"\$LDAP_DN_BASE\"";
```

### Delete Groups and Subgroup
To delete the group inclusive all subgroups use:
```bash
docker exec --env LDAP_ADMIN_PASSWORD="$LDAP_ADMIN_PASSWORD" -it openldap bash -c "ldapsearch -LLL -o ldif-wrap=no -x -D \"cn=administrator,\$LDAP_DN_BASE\" -w \"\$LDAP_ADMIN_PASSWORD\" -b \"ou=applications,ou=groups,\$LDAP_DN_BASE\" dn | sed -n 's/^dn: //p' | tac | while read -r dn; do echo \"Deleting \$dn\"; ldapdelete -x -D \"cn=administrator,\$LDAP_DN_BASE\" -w \"\$LDAP_ADMIN_PASSWORD\" \"\$dn\"; done"

```