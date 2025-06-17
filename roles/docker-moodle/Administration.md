# Administration

# Radical Erase of Setup
To manually erase the full moodle setup inkluding all data execute:

**CLI:**

```bash 
cd /opt/docker/moodle && \
docker compose down -v || {
  echo "docker compose down failed, cleaning up manually"
  rm -rv /mnt/hdd/data/docker/volumes/moodle_*
  docker compose down -v
} && \
rm -rv /opt/docker/moodle
``` 

Afterwards login to the database and execute

**MariaDB:**
```sql
DROP DATABASE IF EXISTS moodle;
```

to delete all data in the database related to this role. 

# Virgin Setup
After the installation you can rerun this role to create a fresh setup of Moodle. 