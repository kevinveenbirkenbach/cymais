# Administration

## Cleanup 
```
# Cleanup Database
for db in matrix applications[application_id].credentials.mautrix_whatsapp_bridge applications[application_id].credentials.mautrix_telegram_bridge applications[application_id].credentials.mautrix_signal_bridge applications[application_id].credentials.mautrix_slack_bridge; do python reset-database-in-central-postgres.py $db; done
# Cleanup Docker and Volumes
docker compose down -v
```