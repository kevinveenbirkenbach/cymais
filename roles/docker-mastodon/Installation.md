# ⚙️ Configuration & Setup

## 🔧 Create Credentials
Run the following command to generate a new configuration setup:
```bash
    docker pull ghcr.io/mastodon/mastodon:latest
    # Secret Generation
    docker run --rm ghcr.io/mastodon/mastodon:latest bundle exec rails secret
    docker run --rm ghcr.io/mastodon/mastodon:latest bundle exec rails secret
    # Vapid Key Generation
    docker run --rm ghcr.io/mastodon/mastodon:latest bundle exec rails mastodon:webpush:generate_vapid_key
    # ACTIVE_RECORD_ENCRYPTION Generation
    docker run --rm ghcr.io/mastodon/mastodon:latest bin/rails db:encryption:init
```

## 🔄 Setup with an Existing Configuration
```bash
docker-compose run --rm web bundle exec rails db:migrate
```

## 🔐 OIDC (OpenID Connect) Authentication Support
This Mastodon role now **fully supports OpenID Connect (OIDC)**, allowing seamless authentication via identity providers like **Keycloak, Auth0, Google, or other OIDC-compliant services**.