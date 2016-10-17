#!/bin/bash

printf "Enter username for JupyterHub:"
read username
stty -echo
printf "Enter corresponding password (no echo):"
read password
stty echo
printf "\n"

printf "Building docker container for JupyterHub"

# Root of jupyterhub-fork. Change accordingly
#cd ~/Dokumente/Sources/forks/jupyterhub

docker build -t jupyterhub-oc-db examples/postgres-checkpoints/db

docker build -t jupyterhub-oc \
    --build-arg USER_NAME=$username \
    --build-arg USER_PASSWORD=$password \
    examples/postgres-checkpoints/hub

printf "Finished building.\nTo run containers with fixed names, we need to remove the old instances.\nThis will delete all changes within the container.\n Proceed?(y/n)"
read input
if [ $input == y ]
  then
    printf "Continue.\n"
  else
    printf "Abort.\n"
    exit 1
fi

docker stop jpy-db
docker rm jpy-db
docker run -d --name jpy-db jupyterhub-oc-db

docker stop jpy-oc2
docker rm jpy-oc2

printf "Waiting for database to start.\n"
sleep 7

docker run -it --name jpy-oc2 --link jpy-db:postgres --security-opt apparmor:unconfined --cap-add MKNOD --cap-add SYS_ADMIN --device /dev/fuse jupyterhub-oc
