# Docker Akaunting Setup Guide

## !!!DANGER!!!

**AKAUNTING CONTAINS VERY MUCH PROPERITARY COMPONENTS. IT IS ALMOST IMPOSSIBLE TO USE THIS SOFTWARE FOR FREE IN A PRODUCTIVE ENVIRONMENT. UPDATES MAY BREAK YOUR INSTALLATION. IN THE PAST UPDATES LEADED TO THE REDUCTION OF FREE FEATURES AND INSTEAD THEY BECOME PAYD FEATURES. THIS LEADED TO THAT USERS COULD NOT MAINTAINE THERE COMPANIES IN AKAUNTING ANYMORE**

I recommend to use instead [Open Project](../docker-openproject/) and/or [GNUCash](../pc-gnucash/).

This role still exist in case, that you want to setup Akaunting and you're willing to pay, but I recommend to don't use akaunting.  

## Introduction
This guide details the process of setting up Akaunting, a free and online accounting software, using Docker. It's tailored to help you deploy and manage an Akaunting instance efficiently using Docker and Docker Compose.

## Prerequisites
- Docker and Docker Compose installed.
- Basic understanding of Docker concepts.
- Access to the command line or terminal.


### Full Backup Routine
Detailed steps for backing up your Akaunting instance, including setting manual and automatic variables, destroying containers, removing volumes, and rebuilding and recovering volumes. (Refer to the full backup routine script in the original README).

### Setting Variables
Variables are crucial in configuring your Akaunting setup. Ensure you set the following variables correctly in your environment:

- `docker_compose.directories.instance`: Set this variable to the path where your Docker Compose files for Akaunting are located.
- `akaunting_db_password`, `applications.akaunting.version`, `applications.akaunting.company_name`, `applications.akaunting.company_email`, `applications.akaunting.setup_admin_email`, and `akaunting_setup_admin_password`: These should be set in your `.env` files as per your requirements.

### Additional Configuration
- **SSL Certificate**: The guide includes steps to receive a certificate for your domain.
- **Nginx Configuration**: Necessary steps to configure Nginx as a reverse proxy for Akaunting.
- **Database and Runtime Environment**: Instructions on how to set up the `db.env` and `run.env` files for database and runtime configurations.

## Other Resources
For more details, visit the [Akaunting Docker Repository](https://github.com/akaunting/docker) and the [Akaunting Forums](https://akaunting.com/forum).

## Contribution and Feedback

Your contributions and feedback are welcome. Please reach out for support or queries at kevin@veen.world.

## Author

This script is developed by Kevin Veen-Birkenbach. You can reach out to him at kevin@veen.world or visit his website at https://www.veen.world.