# role native-pull-remote-backups

## debug
### live
To track what the service is doing execute the following command:

```bash
  watch -n2 "systemctl status pull-remote-backups.service"
```

### history
```bash
  sudo journalctl -u pull-remote-backups
```
