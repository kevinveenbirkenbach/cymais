# role docker-postfix
## delete all data
```bash
docker stop postfix_database_1;  docker rm -f postfix_database_1; docker volume rm -f postfix-database;
```
