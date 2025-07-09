# vars/

This directory contains variable definition files for the `svc-rdbms-mariadb` Ansible role. It centralizes all configurable values related to MariaDB deployment and can be adjusted without modifying task logic.

---

## files and their purpose

### 1. `config/main.yml`

Contains configuration values that determine which Docker image version to use and what hostname the container will be registered under.

* **`version`** (string):

  * Default: `"latest"`
  * The MariaDB image tag to pull (e.g. `10.6`, `10.11`, or `latest`).

* **`hostname`** (string):

  * Default: `"central-mariadb"`
  * The container name and DNS alias within the `central_mariadb` network. Used by other services (like Moodle) to connect.

> **Tip:** Pin to a specific minor version (e.g., `10.6.12`) in production to avoid breaking changes on rebuilds.

---

### 2. `main.yml`

Minimal file defining the application identifier for the role.

* **`application_id`** (string):

  * Default: `"mariadb"`
  * Logical name used in templates, notifications, or paths when multiple roles/services may coexist.