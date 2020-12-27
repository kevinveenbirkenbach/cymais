# role docker-mailu

Keep in mind to change the conflicting ports manual.
Execute

```bash
  netstat -tulpn
```

to verify that there aren't port conflicts

# admin account

Before you can use Mailu, you must create the primary administrator user account. This should be admin@{{hostname}}. Use the following command, changing PASSWORD to your liking:

```bash
  docker-compose -p mailu exec admin flask mailu admin admin {{hostname}} PASSWORD
```

## See
- https://gist.github.com/marienfressinaud/f284a59b18aad395eb0de2d22836ae6b
- https://mailu.io/1.7/compose/setup.html
