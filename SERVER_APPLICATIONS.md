# Server Applications
Server applications encompass a wide array of functionalities designed to enhance the performance, reliability, and usability of server infrastructures. These applications are essential for maintaining server health, managing web services, facilitating containerization, and providing various tools for specific server needs.

## Common Applications
For a detailed overview of the broad spectrum of server applications, including base setup, administration tools, update mechanisms, driver installations, security enhancements, VPN configurations, notifier services, backup solutions, and other essential tools and systems, please refer to the **[COMMON_APPLICATIONS.md](./COMMON_APPLICATIONS.md)**. This document provides insights into categories and specific roles catered to both server and end-user environments, ensuring comprehensive server management and optimization.

## Server Health
Addresses server maintenance and health monitoring, ensuring optimal performance and reliability of the server infrastructure.
- **[Health Btrfs](./roles/health-btrfs/)**: Monitors the health of Btrfs filesystems.
- **[Health Disc Space](./roles/health-disc-space/)**: Checks for available disk space.
- **[Health Docker Container](./roles/health-docker-container/)**: Monitors the health of Docker containers.
- **[Health Docker Volumes](./roles/health-docker-volumes/)**: Checks the status of Docker volumes.
- **[Health Journalctl](./roles/health-journalctl/)**: Monitors and manages the system journal.
- **[Health Nginx](./roles/health-nginx/)**: Ensures the Nginx server is running smoothly.
- **[Heal Docker](./roles/heal-docker/)**: Automated healing and maintenance tasks for Docker.

## Webserver
Focuses on web server roles and applications, covering SSL certificates, Nginx configurations, reverse proxies, and email services.
- **[Letsencrypt](./roles/letsencrypt/)**: Configures Let's Encrypt for SSL certificates.
- **[Nginx](./roles/nginx/)**: Installs and configures Nginx web server.
- **[Nginx-Docker-Reverse-Proxy](./roles/nginx-docker-reverse-proxy/)**: Sets up a reverse proxy for Docker containers.
- **[nginx-static-repository](./roles/nginx-static-repository/)**: Configures a homepage for Nginx.
- **[Nginx-Https](./roles/nginx-https/)**: Enables HTTPS configuration for Nginx.
- **[nginx-global-matomo](./roles/nginx-global-matomo/)**: Integrates Matomo tracking with Nginx.
- **[Nginx-Domain-Redirect](./roles/nginx-domain-redirect/)**: Manages URL redirects in Nginx.
- **[nginx-global-www](./roles/nginx-global-www/)**: Redirects all domains with the prefix www. from www.domain.tld to domain.tld
- **[Nginx-Certbot](./roles/nginx-certbot/)**: Integrates Certbot with Nginx for SSL certificates.
- **[Postfix](./roles/postfix/)**: Setup for the Postfix mail transfer agent.

## Docker and Containerization
Dedicated to Docker container setups and application management, offering a wide array of software deployment options.
- **[Docker](./roles/docker/)**: Basic Docker and Docker Compose setup.

### Finance and Project Management
Facilitating the deployment of finance-related and project management applications.
- **[Docker Akaunting](./roles/docker-akaunting/)**: Deployment of the Akaunting finance software.
- **[Open Project](./roles/docker-openproject)**: Project Management Software
- **[Taiga](./roles/docker-taiga)**: Scrum and Kanban Software

### Continues Integration and Continues Delivery 
Setups for development platforms and version control systems.
- **[Gitea](./roles/docker-gitea/)**: Setup for the Gitea git server.
- **[Jenkins](./roles/docker-jenkins/)**: Jenkins automation server setup.
- **[ELK](./roles/docker-elk/)**: Elasticsearch, Logstash, and Kibana (ELK) stack setup.

### Content Management
Deployment of various content management systems for web platforms.
- **[Wordpress](./roles/docker-wordpress/)**: Wordpress blog and website platform setup.
- **[Joomla](./roles/docker-joomla/)**: Joomla content management system setup.

### Fediverse Networks
Implementing federated and decentralized social platforms.
- **[Funkwhale](./roles/docker-funkwhale/)**: Deployment of Funkwhale, a federated music streaming server.
- **[Mastodon](./roles/docker-mastodon/)**: Deployment of the Mastodon social network server.
- **[Peertube](./roles/docker-peertube/)**: Deployment of the PeerTube video platform.
- **[Pixelfed](./roles/docker-pixelfed/)**: Pixelfed, a federated image sharing platform, setup.

### Analytics Solutions
Tools for web and data analytics.
- **[Matomo](./roles/docker-matomo/)**: Setup for Matomo, an open-source analytics platform.

### Forum Software
Deployments for community-driven forum platforms.
- **[MyBB](./roles/docker-mybb/)**: Setup for MyBB forum software.
- **[Discourse](./roles/docker-discourse/)**: Setup of Discouse a forum and community platform. 

### Wiki and Documentation
Setting up platforms for collaborative information sharing.
- **[MediaWiki](./roles/docker-mediawiki/)**: MediaWiki setup for creating wikis.

### Event and Shop Management
Tools for managing events and online retail.
- **[Attendize](./roles/docker-attendize/)**: Setup for the Attendize event management tool.

### Data and Cloud Storage
Solutions for data management and cloud-based storage.
- **[Baserow](./roles/docker-baserow/)**: Deployment of Baserow, an open-source no-code database tool.
- **[Nextcloud](./roles/docker-nextcloud/)**: Cloud storage solution setup.

### Communication and Collaboration
Platffor enhancing communication and collaborative efforts.
- **[BigBlueButton](./roles/docker-bigbluebutton/)**: Setup for the BigBlueButton video conferencing tool.
- **[Mailu](./roles/docker-mailu/)**: Complete mail server solution.
- **[Matrix](./roles/docker-matrix/)**: Setup and deployment of the Matrix server for secure, decentralized communication.

### Marketing and Communication Tools
Focusing on tools that assist in communication, marketing, and outreach efforts.
- **[Listmonk](./roles/docker-listmonk/)**: Setup for Listmonk, a self-hosted newsletter and mailing list manager.

### Web Utilities and Services
Encompassing tools that enhance web functionality or provide essential web services.
- **[YOURLS](./roles/docker-yourls/)**: Setup for YOURLS, a URL shortening service.

### Miscellaneous
Diverse tools for specific needs and utilities.
- **[Roulette Wheel](./roles/docker-roulette-wheel/)**: Setup for a custom roulette wheel application.