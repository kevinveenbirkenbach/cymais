# Todo 

Implement the following naming conventions.

# Naming Conventions

## Prefix Structure

All roles follow a consistent naming convention using a *primary prefix* and a *secondary prefix*.

### Format

```
<primary prefix>-<secondary prefix>-<role name>
```

### Primary Prefix

| Prefix  | Purpose / Description |
|---------|-----------------------|
| srv-    | Roles that install or configure applications running on servers (services, daemons, infrastructure components) |
| pc- | Roles that install or configure applications running on personal computers or workstations (GUI apps, desktop tools) |
| pkg-    | Roles responsible for installing general-purpose software packages or development tools |
| prs-    | Roles that define personas — collections of roles describing a user-centric environment or system profile |
| drv-    | Roles that install or configure hardware drivers (GPU, printer, kernel modules) |

---

### Secondary Prefix

| Prefix   | Purpose / Description |
|----------|-----------------------|
| backup-  | Roles responsible for backup tasks (data backup, snapshots, remote sync) |
| cleanup- | Roles that clean up the system (temporary files, unused volumes, old backups) |
| docker-  | Roles that manage server applications running in a Dockerized environment (services, infrastructure containers) |
| driver-  | Roles that manage hardware drivers (kernel modules, printers, GPU, peripherals) |
| health-  | Roles for health checks, system monitoring, and metric collection (disk space, containers, service status) |
| heal-    | Roles responsible for auto-repair or healing of system states (service recovery, resource fixes) |
| system-  | Roles for system configuration, hardening, and operating system tuning (security, storage optimization, timers) |
| update-  | Roles managing software update processes (package updates, Docker updates, repository management) |
| user-    | Roles managing system users, accounts, and user-specific configuration (home directories, permissions) |