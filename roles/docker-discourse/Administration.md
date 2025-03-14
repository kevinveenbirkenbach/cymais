# Administration

## Check configuration
```bash
./launcher enter application
pry(main)> SiteSetting.all.each { |setting| puts "#{setting.name}: #{setting.value}" }
```
---