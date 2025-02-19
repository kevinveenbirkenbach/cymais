# 🚀 Docker Mastodon with OIDC Support

## 📌 Overview
This project provides a **Docker-based setup for Mastodon**, including full **OIDC (OpenID Connect) authentication support**. It is maintained by **[Kevin Veen-Birkenbach](https://www.veen.world)**.

This README and some parts of the code were created with the assistance of ChatGPT. You can follow the discussion and evolution of this project in [this conversation](https://chatgpt.com/c/67a4e19b-3884-800f-9d45-621dda2a6572).

## ⚙️ Configuration & Setup

### 🔧 Create Credentials
Run the following command to generate a new configuration setup:
```bash
    docker pull ghcr.io/mastodon/mastodon:latest
    docker run --rm ghcr.io/mastodon/mastodon:latest bundle exec rails secret
```

### 🔄 Setup with an Existing Configuration
```bash
docker-compose run --rm web bundle exec rails db:migrate
```

### 🗑️ Cleanup (Remove Instance & Volumes)
```bash
cd {{path_docker_compose_instances}}mastodon/
docker-compose down
docker volume rm mastodon_data mastodon_database mastodon_redis
cd {{path_docker_compose_instances}} &&
rm -vR {{path_docker_compose_instances}}mastodon
```

### 🔍 Access Mastodon Terminal
```bash
docker-compose exec -it web /bin/bash
```

### 🛠️ Set File Permissions
After setting up Mastodon, apply the correct file permissions:
```bash
docker-compose exec -it -u root web chown -R 991:991 public
```

## 📦 Database Management

### 🏗️ Running Database Migrations
Ensure all required database structures are up to date:
```bash
docker compose exec -it web bash -c "RAILS_ENV=production bin/rails db:migrate"
```

## 🚀 Performance Optimization

### 🗑️ Delete Cache & Recompile Assets
```bash
docker-compose exec web bundle exec rails assets:precompile
docker-compose restart
```

This ensures your Mastodon instance is loading the latest assets after updates.

## 🔐 OIDC (OpenID Connect) Authentication Support
This Mastodon role now **fully supports OpenID Connect (OIDC)**, allowing seamless authentication via identity providers like **Keycloak, Auth0, Google, or other OIDC-compliant services**.

## 📚 Further Reading
- [Mastodon with Docker & Traefik](https://goneuland.de/mastodon-mit-docker-und-traefik-installieren/)
- [Mastodon Configuration Guide](https://gist.github.com/TrillCyborg/84939cd4013ace9960031b803a0590c4)
- [Check Website Availability](https://www.2daygeek.com/linux-command-check-website-is-up-down-alive/)
- [Personal Mastodon Setup](https://vitobotta.com/2022/11/07/setting-up-a-personal-mastodon-instance/)
- [Scaling a Mastodon Server](https://www.digitalocean.com/community/tutorials/how-to-scale-your-mastodon-server)
- [Mastodon GitHub Issues](https://github.com/mastodon/mastodon/issues/7958)



