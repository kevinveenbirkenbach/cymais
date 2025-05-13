# Health CSP Crawler

## Description

This Ansible role automates the validation of [Content Security Policy (CSP)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP) enforcement for all configured domains by crawling them using a Puppeteer-based Node.js script.

## Overview

Designed for Archlinux systems, this role periodically checks whether web resources (JavaScript, fonts, images, etc.) are blocked by CSP headers. It integrates Python and Node.js tooling and installs a systemd service with timer support.

## Features

- **CSP Resource Validation:** Uses Puppeteer to simulate browser requests and detect blocked resources.
- **Domain Extraction:** Parses all `.conf` files in the NGINX config folder to determine the list of domains to check.
- **Automated Execution:** Registers a systemd service and timer for recurring health checks.
- **Error Notification:** Integrates with `systemd-notifier` for alerting on failure.

## Dependencies

This role depends on the following:

- [`nodejs`](../nodejs/)
- [`npm`](../npm/)
- [`systemd-notifier`](../systemd-notifier/)
- [`systemd-timer`](../systemd-timer/)

## Configuration

Set the following variables to customize behavior:

```yaml
health_csp_crawler_folder: "{{ path_administrator_scripts }}health-csp/"
on_calendar_health_csp_crawler: "daily"
````

## License

CyMaIS NonCommercial License (CNCL)
[https://s.veen.world/cncl](https://s.veen.world/cncl)

## Author

Kevin Veen-Birkenbach
Consulting & Coaching Solutions
[https://www.veen.world](https://www.veen.world)