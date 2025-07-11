# sys-hlth-msmtp

## Description

This Ansible role sends periodic health check emails using **msmtp** to verify that your mail transport agent is operational. It deploys a simple script and hooks it into a systemd service and timer, with failure notifications sent via Telegram.

## Overview

Optimized for Archlinux, this role creates the required directory structure, installs and configures the sys-hlth-check script, and integrates with the **sys-alm-telegram** role. It uses the **sys-timer** role to schedule regular checks based on your customizable `OnCalendar` setting.

## Purpose

The **sys-hlth-msmtp** role ensures that your mail transport system stays available by sending a test email at defined intervals. If the email fails, a Telegram alert is triggered, allowing you to detect and address issues before they impact users.

## Features

- **Directory & Script Deployment:** Sets up `sys-hlth-msmtp/` and deploys a templated Bash script to send test emails via msmtp.  
- **Systemd Service & Timer:** Provides `.service` and `.timer` units to run the check and schedule it automatically.  
- **Failure Notifications:** Leverages **sys-alm-telegram** to push alerts when the script exits with an error.  
- **Configurable Schedule:** Define your desired check frequency using the `on_calendar_health_msmtp` variable.  
- **Email Destination:** Specify the recipient via the `users.administrator.email` variable.