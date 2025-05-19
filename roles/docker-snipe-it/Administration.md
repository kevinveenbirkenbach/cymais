# Administration 🛠️
Clear and restart the application:
```bash
docker-compose exec application php artisan config:clear
docker-compose exec application php artisan cache:clear
docker-compose restart application
```