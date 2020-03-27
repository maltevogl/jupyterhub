#!/bin/bash

printf "Enter username for owncloud:"
read username
stty -echo
printf "Enter corresponding password (no echo): "
read password
stty echo
printf "\n"

cd ~/Dokumente/Sources/Githubs/jupyterhub

echo "Building docker container for Postgres Database"

docker build -t mvogl/jupyterhub-postgres-db examples/postgres/db

echo "Building docker container for JupyterHub"

docker build -t mvogl/jupyterhub-postgres-oc-hub \
    --build-arg USER_NAME=$username \
    --build-arg USER_PASSWORD=$password \
    examples/postgres/hub

printf "Docker images have been build.\nTo start containers, we need to delete the old instances of the same name.\nProceed? (y/n)"
read input

if [ $input == 'y' ]
  then
    printf "Running docker images...\n"
  else
    printf "Abborting..."
    exit 1
fi

docker stop jpy-db

docker rm jpy-db

docker run -d --name jpy-db mvogl/jupyterhub-postgres-db

docker stop jpy-oc-hub

docker rm jpy-oc-hub

printf "Waiting for database container.\n"

sleep 7

docker run -it --name jpy-oc-hub --link jpy-db:postgres --cap-add mknod --cap-add SYS_ADMIN --device /dev/fuse --security-opt apparmor:unconfined mvogl/jupyterhub-postgres-oc-hub
