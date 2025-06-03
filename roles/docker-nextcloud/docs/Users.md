# User Administration 

### List Users
```bash
docker compose exec -it -u www-data application php occ user:list
```

### Get User Info
```bash
docker compose exec -u www-data application php occ user:info {{username}}
```

### Sync Users
```bash
docker compose exec -it -u www-data application php occ user:sync
```

### Create user via CLI
```bash
docker compose exec -it -u www-data application php occ user:add {{username}}
```

### Make user admin via cli
```bash
docker compose exec -it -u www-data application php occ group:adduser admin {{username}}
```

### Delete user via CLI
```bash
docker compose exec -it -u www-data application php occ user:delete {{username}}
```

### Delete all User (if no ldap is used)
```bash 
for user in $(docker compose exec -u www-data application php occ user:list --output=json | jq -r 'keys[]'); do
    docker compose exec -u www-data application php occ user:delete "$user"
done
```

### Identify users which exist still in nextcloud but not in LDAP anymore
```bash 
occ ldap:show-remnants
```