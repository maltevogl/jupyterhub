#!/bin/bash

#printf "Enter username for JupyterHub:"
#read username
#stty -echo
#printf "Enter corresponding password (no echo):"
#read password
#stty echo
#printf "\n"

printf "Building docker container for JupyterHub"

docker build -t mvogl/jupyterhub-oauth-db examples/postgres-checkpoints/db

docker build -t mvogl/jupyterhub-oauth examples/postgres-checkpoints/hub
#    --build-arg USER_NAME=$username \
#    --build-arg USER_PASSWORD=$password \


printf "Finished building.\nTo run containers with fixed names, we need to remove the old instances.\nThis will delete all changes within the container.\n Proceed?(y/n)"
read input
if [ $input == y ]
  then
    printf "Continue.\n"
  else
    printf "Abort.\n"
    exit 1
fi

docker stop jpy-oauth-db
docker rm jpy-oauth-db
docker run -d --name jpy-oauth-db mvogl/jupyterhub-oauth-db

docker stop jpy-oauth-hub
docker rm jpy-oauth-hub

printf "Waiting for database to start.\n"
sleep 7

docker run -it --name jpy-oauth-hub --link jpy-oauth-db:postgres  --security-opt apparmor:unconfined --cap-add MKNOD --cap-add SYS_ADMIN --device /dev/fuse -v /var/run/docker.sock:/var/run/docker.sock --env-file=../env mvogl/jupyterhub-oauth # --security-opt apparmor:unconfined --cap-add MKNOD --cap-add SYS_ADMIN --device /dev/fuse 
