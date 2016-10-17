#!/bin/bash
echo "Init database"
#Initializing postgres database with pgcontents
pgcontents init --no-prompt --db-url 'postgresql://pgcontent:pG5ql!_Ch3ck_p0int@172.17.0.2:5432/checkpoints'

#Starting the hub
jupyterhub
