# Running docker

To run the iamge after building use:

    docker run -d --name=jpy-db jupyterhub-postgres-db

and

    docker run -it --name=jpy-hub --link jpy-db:postgres -v ~/selfsigned/jupyterHUBlocal.crt:/srv/jupyterhub/selfcerts/jupyterHUBlocal.crt:ro -v ~/selfsigned/jupyterHUBlocal.key:/srv/jupyterhub/selfcerts/jupyterHUBlocal.key:ro jupyterhub-postgres-hub

PGContents has to be initialized by

    pgcontents init --no-prompt --db-url 'postgresql://pgcontent:pG5ql!_Ch3ck_p0int@172.17.0.2:5432/checkpoints'


UPDATE: 

    docker runs without -v since ssl crts are build inside container:

 docker run -it --name=jpy-hub --link jpy-db:postgres jupyterhub-postgres-hub

TODO: 

    Copy jupyter_notebook_config.py for all users automatically
    use env variables to set postgres keys...

