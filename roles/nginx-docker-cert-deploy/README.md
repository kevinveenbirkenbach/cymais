# Nginx Docker Cert Deploy Role

🎉 **Author**: [Kevin Veen-Birkenbach](https://www.veen.world)

This Ansible role simplifies the deployment of **Let's Encrypt certificates** into **Docker Compose** setups with Nginx. It supports both **individual certificates per subdomain** and a **single wildcard certificate** for all subdomains.

---

## 🚀 **Features**
- Automatically deploys **Let's Encrypt certificates** to Docker Compose setups.
- Supports both **single-domain certificates** and **one wildcard certificate** for all subdomains.
- **Copies certificates** to the target directory inside the container.
- Automatically **reloads or restarts Nginx services** when certificates are updated.
- **Configures and manages a `systemd` service** for automated certificate deployment.
- **Includes a `systemd` timer** for scheduled renewals.
- **Handles dependent services** like `systemd-notifier`.

---

## 📋 **Configuration Options**

### 🔹 **One Wildcard Certificate for All Subdomains**
By default, each subdomain gets its own certificate. You can **enable a wildcard certificate** by setting:

```yaml
enable_wildcard_certificate: true
```

📌 **Pros & Cons of a Wildcard Certificate:**
✅ **Improves performance** by reducing TLS handshakes.  
✅ **Simplifies certificate management** (one cert for all subdomains).  
⚠ **Requires manual DNS challenge setup** for Let's Encrypt.  
⚠ **Needs additional configuration for automation** (see below).  

If enabled, update your inventory file and follow the **manual wildcard certificate setup** below.

---

## 🔧 **Tasks Overview**

### **1️⃣ Main Tasks**
1. **Add Deployment Script**  
   - Copies `nginx-docker-cert-deploy.sh` to the administrator scripts directory.
   
2. **Create Certificate Directory**  
   - Ensures `cert_mount_directory` exists with proper permissions.
   
3. **Configure `systemd` Service**  
   - Deploys a `systemd` service file for the deployment process.
   
4. **Include `systemd-timer` Role**  
   - Schedules automatic certificate deployment using a `systemd` timer.

### **2️⃣ Handlers**
- **Restart Nginx Service**  
  - Restarts `nginx-docker-cert-deploy` whenever a certificate update occurs.

---

## **🔐 Wildcard Certificate Setup with Let's Encrypt**
If you enabled `enable_wildcard_certificate`, follow these steps to manually request a **wildcard certificate**.

### **1️⃣ Run the Certbot Command 🖥️**
```sh
certbot certonly --manual --preferred-challenges=dns --agree-tos \
--email administrator@primary_domain -d primary_domain -d "*.primary_domain"
```

### **2️⃣ Add DNS TXT Record for Validation 📜**
Certbot will prompt you to add a DNS TXT record:
```
Please create a TXT record under the name:
_acme-challenge.primary_domain.

with the following value:
9oVizYIYVGlZ3VtWQIKRS5UghyXiqGoUNlCtIE7LiA
```
➡ **Go to your DNS provider** and create a new **TXT record**:  
   - **Host:** `_acme-challenge.primary_domain`  
   - **Value:** `"9oVizYIYVGlZ3VtWQIKRS5UghyXiqGoUNlCtIE7LiA"`  
   - **TTL:** Set to **300 seconds (or lowest possible)**  

✅ **Verify the DNS record** before continuing:  
```sh
dig TXT _acme-challenge.primary_domain @8.8.8.8
```

### **3️⃣ Complete the Certificate Request ✅**
Once the DNS changes have propagated, **press Enter** in the Certbot terminal.  
If successful, Certbot will save the certificates under:  
```
/etc/letsencrypt/live/primary_domain/
```
- **fullchain.pem** → The certificate  
- **privkey.pem** → The private key  

---

## **📂 File & Directory Structure**
```sh
roles/nginx-docker-cert-deploy/
├── files/
│   ├── nginx-docker-cert-deploy.sh  # Deployment script
├── handlers/
│   ├── main.yml  # Restart Nginx handler
├── meta/
│   ├── main.yml  # Dependencies
├── tasks/
│   ├── main.yml  # Main Ansible tasks
├── templates/
│   ├── nginx-docker-cert-deploy.service.j2  # Systemd service template
├── vars/
│   ├── main.yml  # Variable definitions
```

---

## **🔧 Deploying Certificates into Docker Containers**
The role **automates copying certificates** into Docker Compose setups.

### **1️⃣ Deployment Script (`nginx-docker-cert-deploy.sh`)**
This script:
- **Copies certificates** to the correct container directory.
- **Reloads Nginx** inside all running containers.
- **Restarts containers if needed**.

**Usage:**
```sh
sh nginx-docker-cert-deploy.sh primary_domain /path/to/docker/compose
```

### **2️⃣ Systemd Service & Timer**
The role includes a **`systemd` service** that runs the deployment script whenever certificates are updated.

Example `nginx-docker-cert-deploy.service.j2`:
```ini
[Unit]
Description=Let's Encrypt deploy to {{docker_compose_instance_directory}}
OnFailure=systemd-notifier.cymais@%n.service

[Service]
Type=oneshot
ExecStart=/usr/bin/bash {{path_administrator_scripts}}/nginx-docker-cert-deploy.sh {{primary_domain}} {{docker_compose_instance_directory}}
```

---

## 🎯 **Summary**
| Feature | Description |
|---------|------------|
| **Single-domain & wildcard support** | Use individual certs or a wildcard certificate |
| **Automated renewal** | Cronjob or systemd timer ensures auto-renewals |
| **Docker-ready** | Deploys certificates directly into Docker containers |
| **Supports Nginx & Mailu** | Compatible with multiple services |
| **Systemd integration** | Automates deployment via `systemd` |

🚀 **Now your Nginx setup is fully automated and secured with Let's Encrypt!** 🎉
```