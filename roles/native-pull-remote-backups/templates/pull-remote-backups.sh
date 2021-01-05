#!/bin/bash
hosts="{{pull_remote_backups_hosts}}";
errors=0
for host in $hosts; do
        bash /usr/local/bin/pull-remote-backup/pull-remote-backup.sh $host || ((errors+=1));
done;
exit $errors;
