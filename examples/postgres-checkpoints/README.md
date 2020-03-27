## OpenID-authentified, Postgres-checkpointed, owncloud-backend JupyterHUB Dockerfile

Based on:

https://github.com/jupyterhub/jupyterhub/tree/master/examples/postgres
https://github.com/quantopian/pgcontents
and others

This example shows how you can connect Jupyterhub to a Postgres database
where PGContents is used as the Checkpoints-Manager. This enables multiple checkpoints, saved in the
postgres container. To enable file sharing between users of the hub, an owncloud
folder is mounted as the prefered place of storage. Identification is through a OpenID Identity provider using
a modified oauthenticator. 

Note, that the timezone is set to Europe/Berlin for both docker files. Change accordingly.

## Versions

latest: moved to davfs2 to mount the owncloud filesystem, enable oauth2 with openID server, improve password managment during docker cycle

v0.7: To include owncloud, quite a number of gnome packages are added. Thus, conda-minimal is used again, to keep docker image size acceptable

v0.6: Extends the hub with the full anaconda3 installation, includes pandas,scipy,scikit etc, gives user access to conda package manager through dashboard, allows to create virtualenvs. dockerfile and configs for hub are now in root of jupyterhub, replaces the dockerfile there. requieres change in .dockerignore (comment out jupyter_config.py)

v0.5: Based on From jupyterhub/jupyterhub, has only basic python installed, dockerfiles is in examples/postgres/hub

### TODO


<!---
Hardcoded passwords in the db Dockerfile have been changed to env variables supplied at run time
Same problem applies to the jupyter_notebook_config.py file. Here,
I do not yet know how to pass env variables from host -> docker -> singleusernotebook

Solved: setting c.Spawner.env_keep!
-->
<!---
- Include ldapauthenticator plugin (or openID connect ?):
`https://github.com/jupyterhub/ldapauthenticator`

Solved: OAuthenticator from jupyterhub can be changed to accept credentials from mitreID server at mpi
-->

- Change spawner to dockerspawner:
Would allow to prebuild special singleuser containers with extended standard packages and included extensions
`https://github.com/jupyterhub/dockerspawner`
and present the user with options  during starting their server

<!---
Alternative:
Install full conda env for all users. see v0.6
-->

<!---
Change filesystem to Owncloud:

Solved: By mounting with davfs2
-->

### Security and Portability

1. `IP` (-range) of postgres db is hardcoded in:
  - `examples/postgres-checkpoints/db/initdb.sh` to enable access to psql (pg_hba.conf)
  - `examples/postgres-checkpoints/hub/startup.sh` to enable initializing of pgcontents,


2. `Owncloud-Password` is asked for at first start-up of singleuserserver. This dialog
    is only visible in the shell of the build-script. Should be changed! Moreover,
    a solution like gnome-keyring or PAM would be preverable for saving credentials.

3. Communication to postgres container is not encrypted?! Verify and change!

4. Security implications of running with 

### Running PGContents Checkpoints with Containerized Postgres and Jupyterhub.

1. Edit the credentials in env file and copy file one level under the JupyterHub folder.
   Copy build.sh into root of JupyterHub fork.

2. `cd` to root of jupyterhub fork.

3. Build and run the docker images with `./build.sh`
   This may take a minute or two the first time it's run.
   Asks for confirmation before running the newly build images, since fixed names are used and
   old instances deleted!

4. Log in at `https://172.17.0.3:8000`(get IP of docker with `docker inspect jpy-hub` or
   check logs) as one of the users defined in your env variable `USERS_LIST`.
   By default `admin` is the server's admin user, password is set in env file.

5. IMPORTANT: With the first login of the non-admin user, the shell prompts for the owncloud password.
   This is saved in a user-readable-only file and requiered for mounting the owncloud folder at server start.

6. Logging:
    Startup logs for database can be retrieved with `docker logs jpy-db`. To change the log level, edit `initdb.sh` and rebuild.
    Logs are saved in `$PGDATA/pg_log/`, copy full logs to local directory with
    `docker cp jpy-db:/var/lib/postgresql/data/pg_log/ ~/logs/`

    To change the log level of the hub uncomment the corresponding lines in
    `examples/postgres-checkpoints/hub/jupyterhub_config.py`
