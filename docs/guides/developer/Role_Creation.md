### *Guide to Create a New Docker Role for CyMaIS

This guide will walk you through the steps to add a new Docker role for a service (in this case, `my_service`) in **CyMaIS**. We will cover where to add the application settings, domain, and other required configuration to ensure that your new service is correctly integrated into the CyMaIS environment.

---

### **1. Define the Application Configuration in `templates/vars/applications.yml.j2`**

First, you'll need to add the default configuration for your new service under the `defaults_applications` section in `templates/vars/applications.yml.j2`.

#### **Steps:**
- Open `templates/vars/applications.yml.j2`
- Add the configuration for `my_service` under the `defaults_applications` section.

```yaml
defaults_applications:

  ## My Service Configuration
  my_service:
    version: "latest"
    features:                               # Version of the service
      matomo:     true                      # Enable Matomo tracking for analytics
      css:        true                      # Enable or disable global CSS styling
      portfolio_iframe:     false                     # Allow embedding the landing page in an iframe (if true)
      database:   true                      # Enable central database integration
      ldap:       true                      # Enable ldap integration
      oauth2:     true                      # Enable oauth2 proxy
      oidc:       true                      # Enable oidc
```

---

### **2. Add the Domain for `my_service` in `group_vars/all/03_domains.yml`**

Next, define the domain for your service in the `group_vars/all/03_domains.yml` file. The domain should be dynamic, using the `{{ primary_domain }}` placeholder, which will automatically resolve to the correct domain based on the primary domain used for your environment.

#### **Steps:**
- Open `group_vars/all/03_domains.yml`
- Add the domain for `my_service`.

```yaml
defaults_domains:
  # Other services...
  my_service:            "slides.{{ primary_domain }}"     # Domain for the new service
```

---

### **3. Set the Application ID in `vars/main.yml`**

In the `vars/main.yml` file, set the `application_id` to `my_service`. This step is essential as it allows CyMaIS to correctly reference and configure the new service when deploying it via Docker.

#### **Steps:**
- Open `vars/main.yml`
- Add the `application_id` for the new service.

```yaml
application_id: "my_service"  # Set the application ID for the service
```

---

### **4. Create the Docker Role for the New Service**

Now that you have defined the application settings, domain, and application ID, you need to create a Docker role that will build and run the containerized version of `my_service`.

#### **Steps:**
- Create a new directory under the `roles` directory, e.g., `roles/web-app-my_service`.
- Inside the `web-app-my_service` role, create the following files:

1. **`README.md`**:
    - Provide documentation on the new service and how it works within CyMaIS.

2. **`tasks/main.yml`**:
    - Define the tasks for building and running the Docker container for `my_service`.

    Example `tasks/main.yml`:
    ```yaml
    ---
    # Docker Routines for my_service
    - name: "include docker-compose role"
      include_role:
        name: docker-compose

    - name: install cymais-my_service
      command:
        cmd: "pkgmgr install cymais-my_service --clone-mode https"
      notify: docker compose project build and setup

    - name: Get path of cymais-my_service using pkgmgr
      command: pkgmgr path cymais-my_service
      register: path_cymais_my_service_output

    - name: "include role webserver-proxy-domain for {{ application_id }}"
      include_role:
        name: webserver-proxy-domain
      vars:
        domain: "{{ domains | get_domain(application_id) }}"
        http_port: "{{ ports.localhost.http[application_id] }}"
    ```

3. **`docker-compose.yml.j2`**:
    - Define the `docker-compose.yml` template for building and running the Docker container for the new service.

    Example `docker-compose.yml.j2`:
    ```yaml
    services:
      my_service:
        build:
          context: {{ path_cymais_my_service_output.stdout }}
          dockerfile: {{ path_cymais_my_service_output.stdout }}/Dockerfile
        ports:
          - "127.0.0.1:{{ ports.localhost.http[application_id] }}:5000"
        volumes:
          - {{ path_cymais_my_service_output.stdout }}:/app
          - {{ path_cymais_output.stdout }}:/source
    ```

4. **`vars/main.yml`**:
    - Define any specific variables for `my_service`.

    Example `vars/main.yml`:
    ```yaml
    application_id: "my_service"
    ```

5. **`meta/main.yml`**:
    - Add metadata for your new role.

    Example `meta/main.yml`:
    ```yaml
    galaxy_info:
      author: "Your Name"
      description: "Docker role to deploy and manage my_service within CyMaIS."
      license: "CyMaIS NonCommercial License (CNCL)"
      company: "Your Company"
      min_ansible_version: "2.9"
      platforms:
        - name: Docker
          versions:
            - all
        - name: Linux
          versions:
            - all
      repository: "https://github.com/yourrepo/my_service"
      documentation: "https://yourdocumentationlink"
    ```

---

### **5. Test the Configuration**

Once you have defined the Docker role, configuration settings, and other necessary files, it is essential to test your changes:

#### **Steps:**
- Run the Ansible playbook for deploying your new service.
- Check if `my_service` is correctly deployed and if the domain is resolving as expected.
- Verify that the application is accessible via the assigned port (e.g., `http://slides.{{ primary_domain }}:5000`).

---

### **6. Additional Steps for Integration**

- You can add additional configurations or adjust existing settings based on the requirements for `my_service`. For instance:
  - Modify the health check settings in the `docker-compose.yml` template.
  - Update Nginx or other web servers to properly route traffic to your new service.

---

### **Conclusion**

By following this guide, you have successfully added a new Dockerized service (`my_service`) to the CyMaIS platform. You have:
- Configured the service settings in `templates/vars/applications.yml.j2`
- Added the domain for the service in `group_vars/all/03_domains.yml`
- Set the `application_id` in `vars/main.yml`
- Created the necessary Docker role for managing `my_service`.

This process allows you to extend the functionality of CyMaIS with new services while maintaining a consistent and reproducible deployment workflow.

---

For any further details or troubleshooting, please consult the official CyMaIS documentation or reach out to the CyMaIS community for assistance.