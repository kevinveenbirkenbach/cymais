# role mybb
## install plugins
Extract the plugins to /mnt.
Execute:
```bash
docker run --rm -v mybb-data:/target/ -v /mnt/:/origin/ "kevinveenbirkenbach/alpine-rsync" sh -c "rsync -avv /origin/inc/plugins/ /target/"
```
