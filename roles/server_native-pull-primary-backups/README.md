# role server_native-pull-primary-backups

## goal
This script allows to pull backups from a remote server.

## scheme
It is part of the following scheme:
![backup scheme](https://www.veen.world/wp-content/uploads/2020/12/server-backup-768x567.jpg) <br />
Further information you will find [in this blog post](https://www.veen.world/2020/12/26/how-i-backup-dedicated-root-servers/).

## debug

### live
To track what the service is doing execute one of the following commands:

#### systemctl
```bash
  watch -n2 "systemctl status pull-remote-backups.service"
```

#### journalctl
```bash
  journalctl -fu pull-remote-backups.service
```  

### history
```bash
  sudo journalctl -u pull-remote-backups
```

## see
- https://superuser.com/questions/363444/how-do-i-get-the-output-and-exit-value-of-a-subshell-when-using-bash-e
- https://gist.github.com/otkrsk/b0ffd4018e8a79b9010c461af298471e
- https://serverfault.com/questions/304125/rsync-seems-incompatible-with-bashrc-causes-is-your-shell-clean