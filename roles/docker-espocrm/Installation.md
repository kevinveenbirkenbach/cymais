# ⚙️ Configuration & Setup

## 🔧 Create credentials & pull image
```bash
# Pull the latest EspoCRM image
docker pull espocrm/espocrm:latest

# If you need to pre‑create a config file, copy the default
# (the container will generate one automatically on first start)
```

## 🏗️ Initial deployment with Docker Compose
```bash
# Change into the instance directory created by the role
cd {{path_docker_compose_instances}}espocrm/

# Launch the stack
docker compose up -d
```
The first start can take a minute while EspoCRM initialises the database schema.

## 🔐 LDAP & OIDC authentication
Both mechanisms are supported out of the box:
- **LDAP:** Configure under *Administration → Authentication → LDAP* after the first login.
- **OIDC:** Configure under *Administration → Authentication → OpenID Connect* and paste the Issuer URL, Client ID and Client Secret from your IdP (Keycloak, Authentik, Entra ID, …).