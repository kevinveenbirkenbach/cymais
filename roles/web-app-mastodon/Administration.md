# Administration

## 🗑️ Cleanup (Remove Instance & Volumes)
```bash
cd {{path_docker_compose_instances}}mastodon/
docker-compose down
docker volume rm mastodon_data mastodon_database mastodon_redis
cd {{path_docker_compose_instances}} &&
rm -vR {{path_docker_compose_instances}}mastodon
```

## 🔍 Access Mastodon Terminal
```bash
docker-compose exec -it web /bin/bash
```

## 🛠️ Set File Permissions
After setting up Mastodon, apply the correct file permissions:
```bash
docker-compose exec -it -u root web chown -R 991:991 public
```

# 📦 Database Management

## 🏗️ Running Database Migrations
Ensure all required database structures are up to date:
```bash
docker compose exec -it web bash -c "RAILS_ENV=production bin/rails db:migrate"
```

# 🚀 Performance Optimization

## 🗑️ Delete Cache & Recompile Assets
```bash
docker-compose exec web bundle exec rails assets:precompile
docker-compose restart
```

This ensures your Mastodon instance is loading the latest assets after updates.
