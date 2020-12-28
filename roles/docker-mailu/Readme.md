# role docker-mailu

## setup

### delete data
To delete all volumes and data execute:

```bash
  rm -vr /etc/mailu/; docker volume rm $(docker volume ls -q | grep mailu_)
```
Be careful!

### ports
Keep in mind to change the conflicting ports manual.
Execute

```bash
  netstat -tulpn
```

to verify that there aren't port conflicts

### admin account

Before you can use Mailu, you must create the primary administrator user account. This should be admin@{{hostname}}. Use the following command, changing PASSWORD to your liking:

```bash
  docker-compose -p mailu exec admin flask mailu admin {{admin}} {{hostname}} PASSWORD
```

### cli user management
How to manage users is described here: https://mailu.io/master/cli.html

### Up

```bash
  docker-compose -p mailu up -d
```

## todo
- https://blog.kuepper.nrw/2019/03/30/roundcube-webmail-mit-zwei-faktor-authentifizierung/
- https://mailu.io/master/faq.html#i-want-to-integrate-nextcloud-15-and-newer-with-mailu
- https://docs.nextcloud.com/server/9.0/admin_manual/configuration_user/user_auth_ftp_smb_imap.html

## See
- https://gist.github.com/marienfressinaud/f284a59b18aad395eb0de2d22836ae6b
- https://mailu.io/1.7/compose/setup.html
