# Administration

## cleanup

```bash
docker-compose down && docker volume rm funkwhale_data
```

## create admin account
```bash
docker compose exec -T api funkwhale-manage fw users create --superuser
```

## ldap debugging
```bash
docker compose exec -T api funkwhale-manage shell

import logging
logging.basicConfig(level=logging.DEBUG)


from django.contrib.auth import authenticate
user = authenticate(username="kevinveenbirkenbach", password="DEINPASSWORT")
print(user)


#######
from django_auth_ldap.backend import LDAPBackend
from django_auth_ldap.config import LDAPSearch
from ldap import initialize

# Zugriff auf deine Funkwhale-Einstellungen
import django.conf
settings = django.conf.settings

# Verbindung aufbauen
conn = initialize(settings.AUTH_LDAP_SERVER_URI)
conn.simple_bind_s(settings.AUTH_LDAP_BIND_DN, settings.AUTH_LDAP_BIND_PASSWORD)

# Benutzername einsetzen
username = "kevinveenbirkenbach"

# Search-Filter einsetzen
search_filter = settings.AUTH_LDAP_USER_SEARCH.search_filter.format(username)
base_dn = settings.AUTH_LDAP_USER_SEARCH.base_dn
scope = settings.AUTH_LDAP_USER_SEARCH.scope

# Suche durchführen
results = conn.search_s(base_dn, scope, search_filter)

print(results)

##########

from django.conf import settings

print("LDAP Server URI:", settings.AUTH_LDAP_SERVER_URI)
print("Bind DN:", settings.AUTH_LDAP_BIND_DN)
print("Bind Password:", settings.AUTH_LDAP_BIND_PASSWORD)
print("Search Base:", settings.AUTH_LDAP_USER_SEARCH.base_dn)
print("Search Filter:", settings.AUTH_LDAP_USER_SEARCH.search_filter)
print("User Attr Map:", settings.AUTH_LDAP_USER_ATTR_MAP)

```
