#!/bin/bash
# Checks the healt of all btrfs volumes
for path in $(btrfs filesystem show | awk '/ path /{print $NF}')
do
  btrfs device stats $path
done
