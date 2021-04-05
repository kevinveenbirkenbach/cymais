# role docker-mailu

## setup
### bugs

#### fetchmail
Fetchmail doesn't work with big amounts of data.
For further information see this issue: https://github.com/Mailu/Mailu/issues/1719.

##### deactivation
If you have fetchmail installed and want to deinstall it keep in mind to delete all fetched accounts from the administration panel before you delete fetchmail.

##### security concerns
The [german wikipedia tells that there are some security concern with fetchmail](https://de.wikipedia.org/wiki/Fetchmail). If in the future a customer needs to functions of fetchmail, it could be better to write a docker container for [getmail](https://en.wikipedia.org/wiki/Getmail) instead because it should be more secure.

##### workaround
If you need to receive emails from another account this should help:

- Redirect to your new email account
- Export all data from your original account
- Import all data from your original account to your new account

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

## update
For update instructions follow:
- https://mailu.io/master/maintain.html

## todo
- https://blog.kuepper.nrw/2019/03/30/roundcube-webmail-mit-zwei-faktor-authentifizierung/
- https://mailu.io/master/faq.html#i-want-to-integrate-nextcloud-15-and-newer-with-mailu
- https://docs.nextcloud.com/server/9.0/admin_manual/configuration_user/user_auth_ftp_smb_imap.html

## See
- https://gist.github.com/marienfressinaud/f284a59b18aad395eb0de2d22836ae6b
- https://mailu.io/1.7/compose/setup.html
