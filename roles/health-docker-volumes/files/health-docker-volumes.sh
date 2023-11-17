#!/bin/bash

anonymous_volumes=$(docker volume ls --format "{{.Name}}" | grep -E '^[a-f0-9]{64}$')

if [ -z "$anonymous_volumes" ]; then
    echo "No anonymous volumes found."
    exit 0
fi

echo "Anonymous volumes found:"

for volume in $anonymous_volumes; do
    container_ids=$(docker ps -aq --filter volume=$volume)

    if [ -z "$container_ids" ]; then
        echo "Volume $volume is not used by any running containers."
        continue
    fi

    for container_id in $container_ids; do
        container_name=$(docker inspect --format '{{ .Name }}' $container_id | sed 's#^/##')
        mount_path=$(docker inspect --format "{{ range .Mounts }}{{ if eq .Name \"$volume\" }}{{ .Destination }}{{ end }}{{ end }}" $container_id)
        
        if [ -n "$mount_path" ]; then
            echo "Volume $volume is used by container $container_name at mount path $mount_path"
        else
            echo "Volume $volume is used by container $container_name, but mount path could not be determined."
        fi
    done
done

exit 1
