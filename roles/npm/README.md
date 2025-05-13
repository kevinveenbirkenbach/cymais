# npm

## Description

This Ansible role installs npm and optionally runs `npm ci` within a given project directory. It is intended to streamline dependency installation for Node.js applications.

## Overview

Designed for use in Node-based projects, this role installs npm and can execute a clean install (`npm ci`) to ensure consistent dependency trees.

## Features

- **npm Installation:** Ensures the `npm` package manager is installed.
- **Optional Project Setup:** Runs `npm ci` in a specified folder to install exact versions from `package-lock.json`.
- **Idempotent:** Skips `npm ci` if no folder is configured.

## Configuration

Set `npm_project_folder` to a directory containing `package.json` and `package-lock.json`:

```yaml
vars:
  npm_project_folder: /opt/scripts/my-node-project/
```

## License

CyMaIS NonCommercial License (CNCL)
[https://s.veen.world/cncl](https://s.veen.world/cncl)

## Author

Kevin Veen-Birkenbach
Consulting & Coaching Solutions
[https://www.veen.world](https://www.veen.world)