### Server

#### Server Health
Addresses server maintenance and health monitoring, ensuring optimal performance and reliability of the server infrastructure.
- **[Health Btrfs](./roles/health-btrfs/)**: Monitors the health of Btrfs filesystems.
- **[Health Disc Space](./roles/health-disc-space/)**: Checks for available disk space.
- **[Health Docker Container](./roles/health-docker-container/)**: Monitors the health of Docker containers.
- **[Health Docker Volumes](./roles/health-docker-volumes/)**: Checks the status of Docker volumes.
- **[Health Journalctl](./roles/health-journalctl/)**: Monitors and manages the system journal.
- **[Health Nginx](./roles/health-nginx/)**: Ensures the Nginx server is running smoothly.
- **[Heal Docker](./roles/heal-docker/)**: Automated healing and maintenance tasks for Docker.

#### Webserver
Focuses on web server roles and applications, covering SSL certificates, Nginx configurations, reverse proxies, and email services.
- **[Letsencrypt](./roles/letsencrypt/)**: Configures Let's Encrypt for SSL certificates.
- **[Nginx](./roles/nginx/)**: Installs and configures Nginx web server.
- **[Nginx-Docker-Reverse-Proxy](./roles/nginx-docker-reverse-proxy/)**: Sets up a reverse proxy for Docker containers.
- **[Nginx-Homepage](./roles/nginx-homepage/)**: Configures a homepage for Nginx.
- **[Nginx-Https](./roles/nginx-https/)**: Enables HTTPS configuration for Nginx.
- **[Nginx-Matomo-Tracking](./roles/nginx-matomo-tracking/)**: Integrates Matomo tracking with Nginx.
- **[Nginx-Redirect](./roles/nginx-domain-redirect/)**: Manages URL redirects in Nginx.
- **[Certbot Nginx](./roles/nginx-certbot/)**: Integrates Certbot with Nginx for SSL certificates.
- **[Postfix](./roles/postfix/)**: Setup for the Postfix mail transfer agent.

#### Docker and Containerization
Dedicated to Docker container setups and application management, offering a wide array of software deployment options.
- **[Docker](./roles/docker/)**: Basic Docker and Docker Compose setup.

##### Financial Management
Facilitating the deployment of finance-related applications.
- **[Docker Akaunting](./roles/docker-akaunting/)**: Deployment of the Akaunting finance software.

##### Developer Tools
Setups for development platforms and version control systems.
- **[Docker Gitea](./roles/docker-gitea/)**: Setup for the Gitea git server.
- **[Docker Jenkins](./roles/docker-jenkins/)**: Jenkins automation server setup.
- **[Docker ELK](./roles/docker-elk/)**: Elasticsearch, Logstash, and Kibana (ELK) stack setup.

##### Content Management
Deployment of various content management systems for web platforms.
- **[Docker Wordpress](./roles/docker-wordpress/)**: Wordpress blog and website platform setup.
- **[Docker Joomla](./roles/docker-joomla/)**: Joomla content management system setup.

##### Fediverse Networks
Implementing federated and decentralized social platforms.
- **[Docker Funkwhale](./roles/docker-funkwhale/)**: Deployment of Funkwhale, a federated music streaming server.
- **[Docker Mastodon](./roles/docker-mastodon/)**: Deployment of the Mastodon social network server.
- **[Docker Peertube](./roles/docker-peertube/)**: Deployment of the PeerTube video platform.
- **[Docker Pixelfed](./roles/docker-pixelfed/)**: Pixelfed, a federated image sharing platform, setup.

##### Analytics Solutions
Tools for web and data analytics.
- **[Docker Matomo](./roles/docker-matomo/)**: Setup for Matomo, an open-source analytics platform.

##### Forum Software
Deployments for community-driven forum platforms.
- **[Docker MyBB](./roles/docker-mybb/)**: Setup for MyBB forum software.
- **[Docker Discourse](./roles/docker-discourse/)**: Setup of Discouse a forum and community platform. 

##### Wiki and Documentation
Setting up platforms for collaborative information sharing.
- **[Docker MediaWiki](./roles/docker-mediawiki/)**: MediaWiki setup for creating wikis.

##### Event and Shop Management
Tools for managing events and online retail.
- **[Docker Attendize](./roles/docker-attendize/)**: Setup for the Attendize event management tool.

##### Data and Cloud Storage
Solutions for data management and cloud-based storage.
- **[Docker Baserow](./roles/docker-baserow/)**: Deployment of Baserow, an open-source no-code database tool.
- **[Docker Nextcloud](./roles/docker-nextcloud/)**: Cloud storage solution setup.

##### Communication and Collaboration
Platforms for enhancing communication and collaborative efforts.
- **[Docker BigBlueButton](./roles/docker-bigbluebutton/)**: Setup for the BigBlueButton video conferencing tool.
- **[Docker Mailu](./roles/docker-mailu/)**: Complete mail server solution.
- **[Docker Matrix](./roles/docker-matrix/)**: Setup and deployment of the Matrix server for secure, decentralized communication.

##### Marketing and Communication Tools
Focusing on tools that assist in communication, marketing, and outreach efforts.
- **[Docker Listmonk](./roles/docker-listmonk/)**: Setup for Listmonk, a self-hosted newsletter and mailing list manager.

##### Web Utilities and Services
Encompassing tools that enhance web functionality or provide essential web services.
- **[Docker YOURLS](./roles/docker-yourls/)**: Setup for YOURLS, a URL shortening service.

##### Miscellaneous
Diverse tools for specific needs and utilities.
- **[Docker Roulette Wheel](./roles/docker-roulette-wheel/)**: Setup for a custom roulette wheel application.