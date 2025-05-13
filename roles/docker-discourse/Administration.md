# Administration Notes

## Check configuration

```bash
./launcher enter application
pry(main)> SiteSetting.all.each { |setting| puts "#{setting.name}: #{setting.value}" }
```
---

## Reinitialize Container

To reinitialize the container execute:

```bash
docker network connect discourse_default central-postgres && /opt/docker/discourse/services/discourse_repository/launcher rebuild discourse_application
```