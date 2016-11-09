#!/bin/bash
printf "Building docker container for JupyterHub"

docker build -t jupyterhub-oauth-db examples/postgres-checkpoints/db
docker build -t jupyterhub-oauth examples/postgres-checkpoints/hub


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
docker run -d --name jpy-oauth-db --env-file=../env jupyterhub-oauth-db

docker stop jpy-oauth-hub
docker rm jpy-oauth-hub

printf "Waiting for database to start.\n"
sleep 3

docker run -it --name jpy-oauth-hub --link jpy-oauth-db:postgres  --security-opt apparmor:unconfined --cap-add MKNOD --cap-add SYS_ADMIN --device /dev/fuse -v /var/run/docker.sock:/var/run/docker.sock --env-file=../env jupyterhub-oauth
