# Installation

## MemberOf
```bash
# Activate
ldapmodify -Y EXTERNAL -H ldapi:/// <<EOF
dn: cn=module{0},cn=config
changetype: modify
add: olcModuleLoad
olcModuleLoad: /opt/bitnami/openldap/lib/openldap/memberof.so
EOF

# Verify
ldapsearch -Q -Y EXTERNAL -H ldapi:/// -b "cn=module{0},cn=config" olcModuleLoad

ldapadd -Y EXTERNAL -H ldapi:/// <<EOF
dn: olcOverlay=memberof,olcDatabase={2}mdb,cn=config
objectClass: olcOverlayConfig
objectClass: olcMemberOf
olcOverlay: memberof
olcMemberOfRefInt: TRUE
olcMemberOfDangling: ignore
olcMemberOfGroupOC: groupOfNames
olcMemberOfMemberAD: member
olcMemberOfMemberOfAD: memberOf
EOF


```

### Verifiy that MemberOf is activated and loaded
```bash
docker exec -it ldap sh -c 'ls -l /opt/bitnami/openldap/lib/openldap/memberof.*'
docker exec -it openldap ldapsearch -Y EXTERNAL -H ldapi:/// -b cn=config '(&(objectClass=olcOverlayConfig)(olcOverlay=memberof))'
```
