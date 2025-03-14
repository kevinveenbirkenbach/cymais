# Administration Tasks

## Debug Instructions

### Live Monitoring

To track what the service is doing, execute one of the following commands:

#### Using systemctl

```bash
watch -n2 "systemctl status backup-remote-to-local.cymais.service"
```

#### Using journalctl

```bash
journalctl -fu backup-remote-to-local.cymais.service
```

### Viewing History

```bash
sudo journalctl -u backup-remote-to-local.cymais.service
```