# Development Notes

## Build front container

```bash
docker compose up -d --force-recreate taiga-front
```

## Debug

Verify front configuration:

```bash
docker compose exec -it taiga-front cat /usr/share/nginx/html/conf.json
```

Verify the backend configuration:
```bash
docker compose exec -it taiga-back cat /taiga-back/settings/local.py
```

## Additional Configuration for plugin
```bash
# ENABLE_OPENID Plugin
ENABLE_OPENID = os.getenv('ENABLE_OPENID', 'False') == 'True'
if ENABLE_OPENID:
    INSTALLED_APPS += [
        "taiga_contrib_openid_auth"
    ]
    OPENID_USER_URL = os.getenv('OPENID_USER_URL')
    OPENID_TOKEN_URL = os.getenv('OPENID_TOKEN_URL')
    OPENID_CLIENT_ID = os.getenv('OPENID_CLIENT_ID')
    OPENID_CLIENT_SECRET = os.getenv('OPENID_CLIENT_SECRET')
    OPENID_SCOPE = os.getenv('OPENID_SCOPE')
    OPENID_FILTER = os.getenv('OPENID_FILTER')
    OPENID_FILTER_FIELD = os.getenv('OPENID_FILTER_FIELD')
```