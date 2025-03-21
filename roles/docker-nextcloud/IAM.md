# Identity and Access Management
IAM(Identity and Access Management) is setup via Keycloak and LDAP.

## OpenID Connect (OIDC) Support 🔐

OIDC is supported in this role—for example, via **Keycloak**. OIDC-specific tasks are included when enabled, allowing integration of external authentication providers seamlessly.

### Verify OIDC Configuration

```bash
docker compose exec -u www-data application /var/www/html/occ config:app:get sociallogin custom_providers
```

## LDAP 

More information: https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/user_auth_ldap.html

## Get all relevant entries except password

```sql
SELECT * FROM `oc_appconfig` WHERE appid LIKE "%ldap%" and configkey != "s01ldap_agent_password";
```

## Update User with LDAP values

```bash
docker compose exec -it -u www-data application php occ ldap:check-user --update {{username}}
```

## Federation

If users are just created via Keycloak and not via LDAP, they have a different username. Due to this reaso concider to use LDAP to guaranty that the username is valid. 
