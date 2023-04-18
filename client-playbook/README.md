# Client Playbook
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

Playbook to setup Manjaro GNOME clients in integration with a server which is configured with the [Server Playbook Software](https://github.com/kevinveenbirkenbach/server-playbook).

## Included Applications
- [Basic Linux Administration Tools](./roles/collection-administrator-base/)
- [Network Analyzes Tools](./roles/collection-administrator-network-analyze/)
- [Designer Tools](./roles/collection-designer/)
- [Arduino Developer Tools](./roles/collection-developer-arduino/)
- [Basic Developer Tools](./roles/collection-developer-base/)
- [Bash Developer Tools](./roles/collection-developer-bash/)
- [Java Developer Tools](./roles/collection-developer-java/)
- [PHP Developer Tools](./roles/collection-developer-php/)
- [Python Developer Tools](./roles/collection-developer-python/)
- [Entertainment Software](./roles/collection-entertainment/)
- [Games](./roles/collection-games/)
- [Office Tools](./roles/collection-office/)
- [Streaming Tools](./roles/collection-streamer/)
- [Torrent Software](./roles/collection-torrent/)
- ...

## Setup

Run:
```bash
ansible-galaxy collection install -r requirements.yml
```


## See
- https://www.middlewareinventory.com/blog/run-ansible-playbook-locally/
- https://stackoverflow.com/questions/30533372/run-an-ansible-task-only-when-the-hostname-contains-a-string
- https://archived.forum.manjaro.org/t/running-android-applications-on-arch-using-anbox/53332
- https://www.reddit.com/r/ManjaroLinux/comments/cbkblb/guide_run_android_apps_on_manjaro_super_simple/ 
