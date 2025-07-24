# srv-web-7-7-inj-logout

This role injects a catcher that intercepts all logout elements in HTML pages served by Nginx and redirects them to a centralized logout endpoint via JavaScript.

## Description

The `srv-web-7-7-inj-logout` Ansible role automatically embeds a lightweight JavaScript snippet into your web application's HTML responses. This script identifies logout links, buttons, forms, and other elements, overrides their target URLs, and ensures users are redirected to a central OIDC logout endpoint, providing a consistent single sign‑out experience.

## Overview

- **Detection**: Scans the DOM for anchors (`<a>`), buttons, inputs, forms, `use` elements and any attributes indicating logout functionality.  
- **Override**: Rewrites logout URLs to point at your OIDC provider’s logout endpoint, including a redirect back to the application.  
- **Dynamic content support**: Uses a `MutationObserver` to handle AJAX‑loaded or dynamically injected logout elements.  
- **CSP integration**: Automatically appends the required script hash into your CSP policy via the role’s CSP helper.

## Features

- Seamless injection via Nginx `sub_filter` on `</head>`.  
- Automatic detection of various logout mechanisms (links, buttons, forms).  
- Centralized logout redirection for a unified user experience.  
- No changes required in application code.  
- Compatible with SPAs and dynamically generated content.  
- CSP‑friendly: manages script hash for you.

## Further Resources

- [OpenID Connect RP-Initiated Logout](https://openid.net/specs/openid-connect-session-1_0.html#RPLogout)  
- [Nginx `sub_filter` Module](http://nginx.org/en/docs/http/ngx_http_sub_module.html)  
- [Ansible Role Directory Structure](https://docs.ansible.com/ansible/latest/user_guide/playbooks_roles.html#role-directory-structure)
