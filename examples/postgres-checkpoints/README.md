## Postgres Dockerfile

Based on: 
https://github.com/jupyterhub/jupyterhub/tree/master/examples/postgres
https://github.com/quantopian/pgcontents

This example shows how you can connect Jupyterhub to a Postgres database
instead of the default SQLite backend. In addition PGContents is used as 
the File- and Checkpoints-Manager. This enables multiple checkpoints, 
saved in the postgres container. 

Note, that the timezone is set to Europe/Berlin for both docker files. Change accordingly.

## Versions

v0.5 based on From jupyterhub/jupyterhub, has only basic python installed, dockerfiles is in examples/postgres/hub

v0.6 extends the above with the full anaconda3 installation, includes pandas,scipy,scikit etc, gives user access to conda package manager through dashboard, allows to create virtualenvs. dockerfile and configs for hub are now in root of jupyterhub, replaces the dockerfile there. requieres change in .dockerignore (comment out jupyter_config.py)

### TODO

Hardcoding the passwords in the dockerfile is a bad idea. Needs to be changed. Best practise not yet established.
Possibly using docker-compose and env file. 

<!---
Same problem applies to the jupyter_notebook_config.py file. Here, 
I do not yet know how to pass env variables from host -> docker -> singleusernotebook

Solved: setting c.Spawner.env_keep!
-->

Include ldapauthenticator plugin (or openID connect ?): 
`https://github.com/jupyterhub/ldapauthenticator`

Change spawner to dockerspawner: 

Would allow to prebuild special singleuser containers with extended standard packages and included extensions 
`https://github.com/jupyterhub/dockerspawner`
<!---
Alternative: 
Install full conda env for all users. see v0.6
-->

Change filesystem to Owncloud:
Google Drive:   `https://github.com/jupyter/jupyter-drive`
Amazon S3:      `https://github.com/stitchfix/s3drive`
Owncloud(Beta): `https://github.com/mrow4a/deiccontents`

Full fletched implementation at CERN:
`https://swan.web.cern.ch/`

### Security and Portability

Change from hardcoded to env variables or other solutions. 

`ENV JPY_PSQL_PASSWORD`
`ENV CheckP_PSQL_PASSWORD`

`IP` of postgres container is hardcoded in:
`postgres/db/initdb.sh`, `postgres/hub/jupyter_notebook_config.py`, `/postgres/hub/Dockerfile`

Communication to postgres container is not encrypted ?! Change! 


### Running PGContents Checkpoints with Containerized Postgres and Jupyterhub.

0. Replace `ENV JPY_PSQL_PASSWORD` and `ENV CheckP_PSQL_PASSWORD` with your own
   passwords in the Dockerfile for `/postgres/db` and use the same database password in 
    `/postgres/hub/jupyter_notebook_config.py` and `/postgres/hub/Dockerfile`.

   `JPY_PSQL_PASSWORD` sets the password for the Jupyter backend, used for writing information
    on the state  of the notebook server. `CheckP_PSQL_PASSWORD` is the password for pgcontents, 
    used for managing checkpoints and files.

    Actually, passing with -e `JPY_PSQL_PASSWORD=<password1>` -e `CheckP_PSQL_PASSWORD=<password2>` 
    would be better, but the env variables are not passed on to the user, see above. 

1. `cd` to `/postgres`.

2. Build the postgres image with `docker build -t jupyterhub-postgres-db /db`.
    This may take a minute or two the first time it's run.

3. Run the database image: `docker run -d --name jpy-db jupyterhub-postgres-db` Startup logs can be 
    retrieved with `docker logs jpy-db`. To change the log level, edit `initdb.sh` and rebuild. 
    Logs are saved in `$PGDATA/pg_log/`, copy full logs to local directory with 
    `docker cp jpy-db:/var/lib/postgresql/data/pg_log/ ~/logs/`

   !NOTE!: The container needs to be up and running during build to initialize postgres for pgcontens. To automate this 
   use docker-compose.

4. Build the hub image with `docker build -t jupyterhub-postgres-hub /hub`.
    This may take a minute or two the first time. To change the log level of the HUB edit 
    `/postgres/hub/jupyterhub_config.py`

5. Run the containerized hub with `docker run -it --link jpy-db:postgres jupyterhub-postgres-hub`.
   This instructs docker to run the hub container
   with a link to the already-running db container, which will forward
   environment and connection information from the DB to the hub.

6. Log in at `https://172.17.0.3:8000`(get IP of docker with `docker inspect jpy-hub` or
    check logs) as one of the users defined in `/postgres/hub/Dockerfile`.
    By default `rhea` is the server's admin user, `io` and
   `ganymede` are non-admin users, and all users' passwords are their
   usernames.
   
