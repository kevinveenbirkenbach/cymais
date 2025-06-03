# Update Nextcloud (manuel)

To perform a manuel Nexcloud update execute:

```bash
docker-compose exec -T -u www-data application /var/www/html/occ upgrade
docker-compose exec -T -u www-data application /var/www/html/occ maintenance:repair --include-expensive
docker-compose exec -T -u www-data application /var/www/html/occ app:update --all
docker-compose exec -T -u www-data application /var/www/html/occ db:add-missing-columns
docker-compose exec -T -u www-data application /var/www/html/occ db:add-missing-indices
docker-compose exec -T -u www-data application /var/www/html/occ db:add-missing-primary-keys
docker-compose exec -T -u www-data application /var/www/html/occ maintenance:mode --off
```