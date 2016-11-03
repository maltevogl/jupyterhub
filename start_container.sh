docker start jpy-oauth-db

printf "Waiting for database to start.\n"
sleep 5

docker start jpy-oauth-hub
