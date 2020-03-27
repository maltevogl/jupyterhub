# Dockerizing JupyterHub with Postgres Checkpoints

## Jupyter HUB


    docker run -p 8000:8000 jupyter/jupyterhub jupyterhub --no-ssl
    docker exec -it <containerID> bash # containerID is what you get as the output of docker ps
    useradd -m <username> # some new user -m is important to create home folder , prevents server error 500
    su username 
    passwd PASSWORD
    pip install jupyter
    Visit http://localhost:8000 and log in with the username and password in step 3

## PostGreSQL

Still in Container  do 

    apt-get update && apt-get upgrade
    apt-get install postgresql
    apt-get install nano
    export TERM=xterm
    nano /etc/postgresql/9.4/main/pg_hba.conf

Change end of line for local connections over unix sockets from "peer" to "md5" and restart service.

    service postgresql restart

Now we need to add a password for the database "postgres" (change as requiered),

    su postgres
    psql postgres

In psql the prompt should change to something like "postgres=#". Now change the password

    \password postgres

and quit by "\q".

## PGContent

To install the checkpoint manager we need libpq.

    apt-get install libpq-dev
    pip install pgcontents[ipy4]

Note: the pip package is not yet configured to allow ipython 5, this was recently updated on the repository of pgcontents. Workaround is to add version number 5 manually.

Run init like this 

    pgcontents init
    
General URL for database is 

    postgresql://USER:SECRET@localhost:PORT/DATABASE_NAME

Choosing the standards and setting passwd to postgres we get:

    postgresql://postgres:postgres@localhost:5432/postgres



