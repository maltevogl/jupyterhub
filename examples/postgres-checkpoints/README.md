## Postgres Dockerfile

Based on:

https://github.com/jupyterhub/jupyterhub/tree/master/examples/postgres

https://github.com/quantopian/pgcontents

This example shows how you can connect Jupyterhub to a Postgres database
instead of the default SQLite backend. In addition PGContents is used as
the Checkpoints-Manager. This enables multiple checkpoints, saved in the
postgres container. To enable file sharing between users of the hub, an owncloud
folder is mounted as the prefered place of storage.  

Note, that the timezone is set to Europe/Berlin for both docker files. Change accordingly.

## Versions

v0.7: To include owncloud, quite a number of gnome packages are added. Thus, conda-minimal is used again, to keep docker image size acceptable

v0.6: Extends the above with the full anaconda3 installation, includes pandas,scipy,scikit etc, gives user access to conda package manager through dashboard, allows to create virtualenvs. dockerfile and configs for hub are now in root of jupyterhub, replaces the dockerfile there. requieres change in .dockerignore (comment out jupyter_config.py)

v0.5: Based on From jupyterhub/jupyterhub, has only basic python installed, dockerfiles is in examples/postgres/hub

### TODO

- Hardcoding the database passwords in the dockerfile is a bad idea. Needs to be changed. Best practise not yet established.
Possibly using docker-compose and env file, or simply 'ARG' in dockerfile and 'docker run --build-arg'.

<!---
Same problem applies to the jupyter_notebook_config.py file. Here,
I do not yet know how to pass env variables from host -> docker -> singleusernotebook

Solved: setting c.Spawner.env_keep!
-->

- Include ldapauthenticator plugin (or openID connect ?):
`https://github.com/jupyterhub/ldapauthenticator`

- Change spawner to dockerspawner:
Would allow to prebuild special singleuser containers with extended standard packages and included extensions
`https://github.com/jupyterhub/dockerspawner`

<!---
Alternative:
Install full conda env for all users. see v0.6
-->

Change filesystem to Owncloud:

- Google Drive:   `https://github.com/jupyter/jupyter-drive`
- Amazon S3:      `https://github.com/stitchfix/s3drive`
- Owncloud(Beta): `https://github.com/mrow4a/deiccontents`

Full fletched implementation at CERN:
`https://swan.web.cern.ch/`

### Security and Portability

1. Change from hardcoded to env variables or other solutions.
  - `ENV JPY_PSQL_PASSWORD`
  - `ENV CheckP_PSQL_PASSWORD`
  - `Owncloud-URL`

2. `IP` (-range) of postgres db is hardcoded in:
  - `examples/postgres-checkpoints/db/initdb.sh` to enable access to psql (pg_hba.conf)
  - `examples/postgres-checkpoints/hub/startup.sh` to enable initializing of pgcontents,

3. `Password` of postgres db is hardcoded in:
  - `examples/postgres-checkpoints/hub/startup.sh` to enable initializing of pgcontents,

4. `Owncloud-Password` is asked for at first start-up of singleuserserver. This dialog
    is only visible in the shell of the build-script. Should be changed! Moreover,
    a solution like gnome-keyring or PAM would be preverable for saving credentials.

Communication to postgres container is not encrypted?! Verify and change!

### Running PGContents Checkpoints with Containerized Postgres and Jupyterhub.

1. Replace `ENV JPY_PSQL_PASSWORD` and `ENV CheckP_PSQL_PASSWORD` with your own
   passwords in the Dockerfile for `examples/postgres-checkpoints/db`.

   `JPY_PSQL_PASSWORD` sets the password for the Jupyter backend, used for writing information
    on the state  of the notebook server. `CheckP_PSQL_PASSWORD` is the password for pgcontents,
    used for managing checkpoints ( and files if desired).

    Actually, passing with -e `JPY_PSQL_PASSWORD=<password1>` -e `CheckP_PSQL_PASSWORD=<password2>`
    would be better. Needs to be changed in buildHub.sh .

2. `cd` to root of jupyterhub fork.

3. Build and run the docker images with './buildHUB.sh'
   This may take a minute or two the first time it's run.
   Asks for confirmation before running the newly build images, since fixed names are used and
   old instances deleted!

4. Log in at `https://172.17.0.3:8000`(get IP of docker with `docker inspect jpy-hub` or
   check logs) as one of the users defined in `examples/postgres-checkpoints/hub/Dockerfile`.
   By default `admin` is the server's admin user, password is the username. Non-admin username
   is asked for while running the build-script. To add more non-admin users edit `examples/postgres-checkpoints/hub/Dockerfile`.

5. IMPORTANT: With the first login of the non-admin user, the shell prompts for the owncloud password.
   This is saved in a user-readable-only file and requiered for mounting the owncloud folder at server start.

6. Logging:
    Startup logs for database can be retrieved with `docker logs jpy-db`. To change the log level, edit `initdb.sh` and rebuild.
    Logs are saved in `$PGDATA/pg_log/`, copy full logs to local directory with
    `docker cp jpy-db:/var/lib/postgresql/data/pg_log/ ~/logs/`

    To change the log level of the hub uncomment the corresponding lines in
    `examples/postgres-checkpoints/hub/jupyterhub_config.py`
