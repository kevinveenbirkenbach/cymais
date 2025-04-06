# PostgreSQL Docker Upgrade: Major Version Migration

This guide explains how to safely upgrade a PostgreSQL Docker container from one major version to another (e.g., version 12 to 16) using a **dump and restore** method. This is the recommended approach in Docker environments.

---

## ⚠️ Important
PostgreSQL data directories are **not compatible across major versions**. You cannot just point a newer version to the old data volume. You must export and re-import your data.

---

## 💾 Step 1: Start a temporary container with your current PostgreSQL version

Replace `<old-version>` with your current PostgreSQL version (e.g., `12`).

```bash
docker run --rm -d \
  --name pg-old \
  -v pgdata:/var/lib/postgresql/data \
  postgres:<old-version>
```

This container mounts your old data volume and runs the matching PostgreSQL version.

---

## ⬇️ Step 2: Dump all databases

```bash
docker exec pg-old pg_dumpall -U postgres > backup.sql
```

Stop the old container:

```bash
docker stop pg-old
```

---

## 💥 Step 3: Remove the old data volume

```bash
docker volume rm pgdata
```

⚠️ This will permanently delete your old PostgreSQL data files. Make sure you have a successful backup (`backup.sql`) before running this!

---

## 📦 Step 4: Start a new container with your target PostgreSQL version

Replace `<new-version>` with the version you want to upgrade to (e.g., `16`).

```bash
docker run --rm -d \
  --name pg-new \
  -v pgdata:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=secret \
  postgres:<new-version>
```

This creates a clean PostgreSQL instance with a fresh data directory.

---

## ⬆️ Step 5: Restore your data

```bash
cat backup.sql | docker exec -i pg-new psql -U postgres
```

This restores all roles, databases, and data into your new PostgreSQL instance.

---

## ✅ Done!
You now have the target PostgreSQL version running with your old data successfully restored.

---

## 📝 Tips
- Always test this procedure in a staging environment before running it in production.
- You can automate this with Ansible or a custom script.
- For large databases, consider using `pg_dump` per database and `pg_restore` with parallel jobs.

---

## 🔗 References
- [PostgreSQL Backup Documentation](https://www.postgresql.org/docs/current/backup-dump.html)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)

