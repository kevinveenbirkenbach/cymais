# Administration

## Cleanup 
```
# Cleanup Database
for db in matrix applications | get_app_conf(application_id, 'credentials.mautrix_whatsapp_bridge', True) applications | get_app_conf(application_id, 'credentials.mautrix_telegram_bridge', True) applications | get_app_conf(application_id, 'credentials.mautrix_signal_bridge', True) applications | get_app_conf(application_id, 'credentials.mautrix_slack_bridge', True); do python reset-database-in-central-postgres.py $db; done
# Cleanup Docker and Volumes
docker compose down -v
```