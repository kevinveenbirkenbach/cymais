# Nginx WWW Redirect 🌐

## Description
Automates the creation of Nginx server blocks that redirect all `www.` subdomains to their non-www equivalents. Simple, idempotent, and SEO-friendly! 🚀

## Overview
This role will:
- **Discover** existing `*.conf` vhosts in your Nginx servers directory  
- **Filter** domains with or without your `primary_domain`  
- **Generate** redirect rules via the `web-redirect-domains` role  
- **Optionally** include a wildcard redirect template (experimental) ⭐️  
- **Clean up** leftover configs when running in cleanup mode 🧹  

All tasks are guarded by “run once” facts and `mode_cleanup` flags to avoid unintended re-runs or stale files.

## Purpose
Ensure that any request to `www.example.com` automatically and permanently redirects to `https://example.com`, improving user experience, SEO, and certificate management. 🎯

## Features
- **Auto-Discovery**: Scans your Nginx `servers` directory for `.conf` files. 🔍  
- **Dynamic Redirects**: Builds `source: "www.domain"` → `target: "domain"` mappings on the fly. 🔧  
- **Wildcard Redirect**: Includes a templated wildcard server block for `www.*` domains (toggleable). ✨  
- **Cleanup Mode**: Removes the wildcard config file when `certbot_flavor` is set to `dedicated` and `mode_cleanup` is enabled. 🗑️
- **Debug Output**: Optional `enable_debug` gives detailed variable dumps for troubleshooting. 🐛  
