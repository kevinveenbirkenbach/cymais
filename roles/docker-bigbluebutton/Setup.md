# Setup

## Passwords
```bash
docker run --rm ruby:latest ruby -rsecurerandom -e 'puts SecureRandom.hex(64)'
```