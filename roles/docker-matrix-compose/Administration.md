# Administration

## Cleanup 
```
# Cleanup Database
for db in matrix mautrix_whatsapp_bridge mautrix_telegram_bridge mautrix_signal_bridge mautrix_slack_bridge; do python reset-database-in-central-postgres.py $db; done
# Cleanup Docker and Volumes
docker compose down -v
```