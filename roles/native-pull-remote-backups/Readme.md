# role native-pull-remote-backups

## goal
This script allows to pull backups from a remote server.

## scheme
It is part of the following scheme:
![backup scheme](https://www.veen.world/wp-content/uploads/2020/12/server-backup-768x567.jpg) <br />
Further information you will find [in this blog post](https://www.veen.world/2020/12/26/how-i-backup-dedicated-root-servers/).

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
