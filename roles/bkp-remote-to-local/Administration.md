# Administration Tasks

## Debug Instructions

### Live Monitoring

To track what the service is doing, execute one of the following commands:

#### Using systemctl

```bash
watch -n2 "systemctl status bkp-remote-to-local.cymais.service"
```

#### Using journalctl

```bash
journalctl -fu bkp-remote-to-local.cymais.service
```

### Viewing History

```bash
sudo journalctl -u bkp-remote-to-local.cymais.service
```