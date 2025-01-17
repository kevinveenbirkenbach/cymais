# DRAFT role docker-bluesky

## Set variables

### bluesky_pds_jwt_secret
```bash
openssl rand -base64 64 | tr -d '\n'
```
for 

### bluesky_pds_plc_rotation_key_k256_private_key_hex
openssl rand -hex 32

### bluesky_pds_admin_password
openssl rand -base64 16

### bluesky_database_password
openssl rand -base64 32

## create user
```bash
curl -X POST https://your-pds-domain/xrpc/com.atproto.server.createAccount \
  -H "Content-Type: application/json" \
  -d '{
        "email": "user@example.com",
        "handle": "username",
        "password": "securepassword123",
        "inviteCode": "optional-invite-code"
      }'
```

## more information
- https://therobbiedavis.com/selfhosting-bluesky-with-docker-and-swag/
- https://cprimozic.net/notes/posts/notes-on-self-hosting-bluesky-pds-alongside-other-services/
- https://github.com/bluesky-social/pds
- https://chatgpt.com/c/678a2eb6-145c-800f-bf51-ff706981a928