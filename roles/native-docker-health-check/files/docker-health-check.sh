#!/bin/sh
docker_ps_grep_unhealthy="$(docker ps | grep unhealthy)"
docker_ps_grep_exited="$(docker ps -a | grep Exited)"
exitcode=0
if [ ! -z "$docker_ps_grep_unhealthy" ]
then 
   echo "Some docker containers are unhealthy: $docker_ps_grep_unhealthy"
   exitcode=1
fi
if [ ! -z "$docker_ps_grep_exited" ]
then 
   echo "Some docker containers exited: $docker_ps_grep_exited"
   exitcode=2
fi
if [ "$exitcode" -ne "0" ]
then 
   exit $exitcode
fi
echo "All docker containers are healthy."
exit