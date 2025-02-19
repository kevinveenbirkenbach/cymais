# Docker-Matrix Role README

## Overview

This document serves as the README for the `docker-matrix` role, a part of the `CyMaIS` project. This role automates the deployment of a Matrix server using Docker. This role was developed by [Kevin Veen-Birkenbach](https://www.veen.world/)

Matrix is an open-source project that provides a protocol for secure, decentralized, real-time communication. It offers features like end-to-end encrypted chat, VoIP, and file sharing, catering to both individual and enterprise users. With a focus on interoperability, Matrix can bridge with other communication systems, offering a unified platform for messaging and collaboration.

## Cleanup 
```
# Cleanup Database
for db in matrix mautrix_whatsapp_bridge mautrix_telegram_bridge mautrix_signal_bridge mautrix_slack_bridge; do python reset-database-in-central-postgres.py $db; done
# Cleanup Docker and Volumes
docker compose down -v
```

## Bridges

### Mautrix 
Contact one of the following bots for more information:

- @signalbot:yourdomain.tld
- @telegrambot:yourdomain.tld
- @whatsappbot:yourdomain.tld
- @slackbot:yourdomain.tld

#### Slack
For login with Token checkout [this guide](https://docs.mau.fi/bridges/go/slack/authentication.html).

### ChatGPT
- Create API Token: https://platform.openai.com/api-keys
- Set ``matrix_chatgpt_bridge_access_token`` 

## Debug:
- https://federationtester.matrix.org/

## Sources

### Guides
- https://matrix-org.github.io/synapse/latest/usage/configuration/config_documentation.html
- https://cyberhost.uk/element-matrix-setup/
- https://www.linode.com/docs/guides/how-to-install-the-element-chat-app/
- https://hub.docker.com/r/vectorim/element-web
- https://github.com/matrix-org/matrix-synapse-ldap3

## Links to ChatGPT Conversations

- https://chat.openai.com/share/d4485223-3750-4b0b-9733-45776c55d7cf
- https://chat.openai.com/share/f68873d9-aae9-4a1e-83b6-c3f23705a4ad
- https://chat.openai.com/share/11690964-9997-4e44-b63f-3c384a5ddc1d
- https://chat.openai.com/share/6f537c30-7337-47ed-8c85-19306e0eb74b
- https://chat.openai.com/share/31974492-2950-4dbc-8a83-edd7e1569bec

##  Alternativ Matrix Setup Role
An alternativ role to deploy Matrix you will find [here](../docker-matrix-ansible/).