# Change Distinguished Name (DN) in OpenLDAP Docker

This document provides a step-by-step guide on how to rename the Distinguished Name (DN) from `cn=administrator,dc=flock,dc=town` to `cn=administrator,dc=cymais,dc=cloud` in an **OpenLDAP Docker** environment.

**Reference:** [Conversation Link](https://chatgpt.com/share/67d9a2f7-4e04-800f-9a0f-1673194f276c)

---

## 1. Export the Current Entry

Connect to the OpenLDAP container and export the current entry:

```sh
docker exec -it ldap sh -c 'ldapsearch -x -D "$LDAP_ADMIN_DN" -w "$LDAP_ADMIN_PASSWORD" -b "$LDAP_ROOT"' > all_entries.ldif
```

If your ***LDAP_ADMIN_DN*** and ***LDAP_ROOT***  are not accured pass them via ``--env``.

---

## 2. Modify the LDIF File

Open `all_entries.ldif` and update the DN (`dn:` line) and `dc` attributes.

- Open the file in an editor (`nano`, `vim`, `sed`).
- Replace **all occurrences** of `dc=flock,dc=town` with `dc=cymais,dc=cloud`.

**Using `sed` to modify automatically:**
```sh
sed -i 's/dc=flock,dc=town/dc=cymais,dc=cloud/g' all_entries.ldif
```

**Before:**
```ldif
dn: cn=administrator,dc=flock,dc=town
cn: administrator
objectClass: organizationalRole
objectClass: simpleSecurityObject
userPassword: {SSHA}...
```

**After:**
```ldif
dn: cn=administrator,dc=cymais,dc=cloud
cn: administrator
objectClass: organizationalRole
objectClass: simpleSecurityObject
userPassword: {SSHA}...
```

---

## 3. Delete the Old Entry

### Generate a Recursive Delete LDIF
We need an **LDIF file that deletes all objects** under `dc=flock,dc=town`.

Instead of manually writing an LDIF file, you can use `ldapsearch` and `awk` to generate it dynamically:

```sh
docker exec -it ldap sh -c 'ldapsearch -x -D "cn=administrator,dc=flock,dc=town" -w "$LDAP_ADMIN_PASSWORD" -b "dc=flock,dc=town" dn' | awk "/^dn:/ {print \$2}" | tac > delete_all_dns.txt
```

This creates an **ordered delete list**, starting with child objects before deleting `dc=flock,dc=town`.

---

#### Apply the Recursive Delete
Now apply the generated `delete_all.ldif` to delete all entries **recursively**:

```sh
docker exec -i ldap sh -c '
while read dn; do
  ldapdelete -x -D "cn=administrator,dc=flock,dc=town" -w "$LDAP_ADMIN_PASSWORD" "$dn"
done' < delete_all_dns.txt
```

---

#### Verify That Everything Is Deleted
After running the delete command, verify that `dc=flock,dc=town` is empty:

```sh
docker exec -it ldap sh -c 'ldapsearch -x -D "cn=administrator,dc=flock,dc=town" -w "$LDAP_ADMIN_PASSWORD" -b "dc=flock,dc=town"'
```
- ✅ If **no results** are returned, the domain has been deleted successfully.
- ❌ If results still exist, some entries were not removed.


#### Create new_database.ldif

docker exec -i ldap ldapadd -Y EXTERNAL -H ldapi:/// -f /dev/stdin < new_database.ldif

## 4. Add the New Entry

Now, upload the modified `all_entries.ldif`:

```sh
cat all_entries.ldif | docker exec -i ldap sh -c 'ldapadd -x -D "cn=admin,dc=cymais,dc=cloud" -w "$LDAP_ADMIN_PASSWORD"'
```

---

## 5. Update Root DN Configuration

If `cn=administrator` is used as `rootdn`, update the OpenLDAP configuration file (`slapd.conf` or `olcDatabase={1}mdb.ldif` under `cn=config`).

Find:
```ldif
olcRootDN: cn=administrator,dc=flock,dc=town
```
Replace with:
```ldif
olcRootDN: cn=administrator,dc=cymais,dc=cloud
```

Save the change and apply it:

```sh
docker exec -it ldap ldapmodify -Y EXTERNAL -H ldapi:/// -f config_update.ldif
```

---

## 6. Restart OpenLDAP

Restart the OpenLDAP container if necessary:

```sh
docker restart ldap
```

Now, `cn=administrator,dc=cymais,dc=cloud` should be active as the new administrator account.