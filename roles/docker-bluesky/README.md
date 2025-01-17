# DRAFT role docker-bluesky


## Setup 
### Set variables

#### bluesky_pds_jwt_secret
```bash
openssl rand -base64 64 | tr -d '\n'
```
for 

#### bluesky_pds_plc_rotation_key_k256_private_key_hex
openssl rand -hex 32

#### bluesky_pds_admin_password
openssl rand -base64 16

### Configure DNS
- https://bsky.social/about/blog/4-28-2023-domain-handle-tutorial

## Administration

### create user via POST
```bash
curl -X POST https://your-pds-domain/xrpc/com.atproto.server.createAccount \
  --user "admin:$admin-password" 
  -H "Content-Type: application/json" \
  -d '{
        "email": "user@example.com",
        "handle": "username",
        "password": "securepassword123",
        "inviteCode": "optional-invite-code"
      }'
```

### Use pdsadmin
docker compose exec -it pds pdsadmin

docker compose exec -it pds pdsadmin account create-invite-code

## Debugging

- Websocket: https://piehost.com/websocket-tester
- Instance: https://bsky-debug.app

https://bluesky.veen.world/.well-known/atproto-did


## more information
- https://therobbiedavis.com/selfhosting-bluesky-with-docker-and-swag/
- Relevant for proxy configuration: https://cprimozic.net/notes/posts/notes-on-self-hosting-bluesky-pds-alongside-other-services/
- https://github.com/bluesky-social/pds
- https://chatgpt.com/c/678a2eb6-145c-800f-bf51-ff706981a928
- https://www.youtube.com/watch?v=7_AG50u7D6c
- https://github.com/bluesky-social/pds/issues/52
- https://github.com/lhaig/pdsadmin
- https://github.com/bluesky-social/pds/issues/147
- 