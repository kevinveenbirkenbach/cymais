# Nginx Matomo Tracking Role

This Ansible role automates the integration of Matomo tracking code into Nginx-served websites. It simplifies the process of adding the Matomo analytics tracking script and image tracker to all your web pages served through Nginx.

## Features
- Automated insertion of Matomo tracking script into the `</head>` tag of HTML pages.
- Integration of a noscript image tracker before the `</body>` tag for tracking users with JavaScript disabled.
- Configuration to apply changes on every request, ensuring that dynamic content and single-page applications are also tracked.

## Requirements
- Nginx installed on the target server.
- Matomo analytics platform set up and accessible.

## Role Variables
- `matomo_domain`: The domain of your Matomo installation.
- `domain`: The domain of the website you wish to track.
- `matomo_auth_token`: Matomo auth token

## Dependencies
- None. This role is designed to be included in Nginx server block configurations.

## Example Usage
To enable Matomo tracking on your Nginx website, include the role in your playbook and set the required variables.

```yaml
- hosts: webserver
  roles:
    - { role: nginx-matomo-tracking, matomo_domain: 'matomo.example.com', base_domain: 'example.com', matomo_site_id: '1' }
```

## Customization
You can customize the tracking script and the noscript image tracker by editing the `matomo-tracking.js.j2` and `matomo-tracking.conf.j2` templates.

## Author Information
This role was created in 2023 by Kevin Veen Birkenbach, providing a seamless way to add Matomo analytics to any website served via Nginx.