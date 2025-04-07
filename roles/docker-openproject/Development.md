# Development Notes

## Get Settings

## LDAP

```bash
docker compose exec web bash -c 'cd /app && RAILS_ENV=production bundle exec rails runner "puts Setting.all.select { |s| s.name.start_with?(\"ldap\") }.map { |s| \"#{s.name} = #{s.value}\" }"'
```

### All

```bash
docker compose exec web bash -c 'cd /app && RAILS_ENV=production bundle exec rails runner "Setting.all.each { |s| puts \"#{s.name} = #{s.value}\" }"'
```