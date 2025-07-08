## delete all data
```bash
docker stop joomla_application_1;  docker rm -f joomla_application_1; docker volume rm -f joomla-data;
docker stop joomla_database_1;  docker rm -f joomla_database_1; docker volume rm -f joomla-database;
```