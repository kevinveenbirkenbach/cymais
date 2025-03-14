# Database Setup Role 🚀

This Ansible role provides the necessary tasks, files, templates, and variables to set up databases in your Docker Compose environment. It is essential for configuring your application's database, whether using a local or a central instance of **MariaDB** or **PostgreSQL**.

---

## 📌 Overview 🔍

- **Database Variables**  
  Defined in [./vars/database.yml](./vars/database.yml), these variables include:
  - `database_instance`
  - `database_host`
  - `database_name`
  - `database_username`
  - `database_port`
  - `database_env`

- **Tasks**  
  Located in [./tasks/main.yml](./tasks/main.yml), the tasks perform the following:
  - Include the Docker Compose role.
  - Load database variables.
  - Create the environment file for the chosen database from a template.
  - Optionally create a central database (if enabled).

- **Templates**  
  - **Environment Files:**  
    - [PostgreSQL Environment Template](./templates/env/postgres.env.j2)  
    - [MariaDB Environment Template](./templates/env/mariadb.env.j2)
  - **Service Files:**  
    - [MariaDB Service Template](./templates/services/mariadb.yml.j2)  
    - [PostgreSQL Service Template](./templates/services/postgres.yml.j2)

---

## Usage 📋

To use this role, include it in your playbook as follows:

```yaml
- hosts: all
  roles:
    - your_database_role_name
```

When executed, the role will:

1. Load database configuration variables.
2. Generate the appropriate environment file for the database.
3. Incorporate the Docker Compose routines.
4. Create a central database if `applications[application_id].database.central_storage` is set to `true`.

---

## Author

Developed by [Kevin Veen-Birkenbach](https://www.veen.world/) 💻🌐

---

## Acknowledgments & ChatGPT Conversations 🤖💬

This role was created with the assistance of ChatGPT. The following ChatGPT conversations helped shape the design and implementation of this role:

- https://chatgpt.com/share/67a23d18-fb54-800f-983c-d6d00752b0b4
- https://chatgpt.com/share/67a244bb-11e4-800f-980f-5ef0e8b109d7

Feel free to explore these discussions for insights into design decisions and implementation details.

---

Happy automating! 🎉