# Administration

## Configuration

## Load env 

To use the following commands firs load the env:
```bash
export $(grep -v '^[[:space:]]*#' ./.env/env \
         | sed -E 's/#.*$//; /^[[:space:]]*$/d; s/^[[:space:]]*//; s/[[:space:]]*$//; s/[[:space:]]*=[[:space:]]*/=/' \
         | xargs)
```

### Show Configuration
```bash
docker exec -it ldap bash -c "ldapsearch -LLL -Y EXTERNAL -H ldapi:/// -b 'cn=config'"
```

```bash
docker exec -it ldap bash -c "ldapsearch -LLL -Y EXTERNAL -H ldapi:/// -b 'cn=config' -s base '(objectClass=*)'"
```

```bash
docker exec -it ldap bash -c "ldapsearch -LLL -Y EXTERNAL -H ldapi:/// -b 'cn=config' -s base '(objectClass=olcModuleList)'"
```

### Databases Overview
```bash
docker exec -it ldap ldapsearch -Y EXTERNAL -H ldapi:/// -b "cn=config" "(olcDatabase=*)"
```

## Data

### Set Credentials
To execute the following commands set the credentials via:

```bash
export $(grep -Ev '^(#|$)' .env/env | xargs)
```

### Show all Entries
```bash 
docker exec -it ldap bash -c "ldapsearch -LLL -o ldif-wrap=no -x -D \"\$LDAP_ADMIN_DN\" -w \"\$LDAP_ADMIN_PASSWORD\" -b \"\$LDAP_ROOT\"";
```

### Delete Groups and Subgroup
To delete the group inclusive all subgroups use:
```bash
docker exec -it ldap bash -c "ldapsearch -LLL -o ldif-wrap=no -x -D \"\$LDAP_ADMIN_DN\" -w \"\$LDAP_ADMIN_PASSWORD\" -b \"ou=applications,ou=groups,\$LDAP_ROOT\" dn | sed -n 's/^dn: //p' | tac | while read -r dn; do echo \"Deleting \$dn\"; ldapdelete -x -D \"\$LDAP_ADMIN_DN\" -w \"\$LDAP_ADMIN_PASSWORD\" \"\$dn\"; done"

# Works
docker exec -it ldap \
  ldapdelete -x \
    -D "$LDAP_ADMIN_DN" \
    -w "$LDAP_ADMIN_PASSWORD" \
    -r \
    "ou=groups,$LDAP_ROOT"
```

## Import RBAC
```bash
docker exec -i ldap \
  ldapadd -x \
    -D "$LDAP_ADMIN_DN" \
    -w "$LDAP_ADMIN_PASSWORD" \
    -c \
    -f "/tmp/ldif/data/01_rbac_roles.ldif"
```