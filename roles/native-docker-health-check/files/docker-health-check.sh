#!/bin/sh
docker_ps_grep_unhealthy="$(docker ps | grep unhealthy)"
if [ -z "$docker_ps_grep_unhealthy" ]
then 
   echo "All docker containers are healthy."
   exit
else
   echo "Some docker containers are unhealthy: $docker_ps_grep_unhealthy"
   exit 1
fi