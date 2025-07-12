# Administration

## Root Access
To access the database via the root account execute the following on the server:
```bash
docker exec -it "{{ applications['postgres'].hostname }}" psql -U postgres
```