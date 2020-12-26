#!/bin/bash
hosts="{{pull_remote_backups_hosts}}";
for host in $hosts; do
        bash /usr/local/bin/pull-remote-backup/pull-remote-backup.sh $host;
done;
