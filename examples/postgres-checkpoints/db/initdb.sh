#!/bin/bash

echo "";
echo "Running initdb.sh.";
if [ -z "$CHECKPOINTS_PASSWORD" ]; then
    echo "Need to set CHECKPOINTS_PASSWORD in env file or via command line.";
    exit 1;
elif [ "$CHECKPOINTS_PASSWORD" == "arglebargle" ]; then
    echo "WARNING: Running with default password!"
    echo "You are STRONGLY ADVISED to use your own password.";
fi
echo "";

# Start a postgres daemon, ignoring log output.
#gosu postgres pg_ctl start -w -l /dev/null

# Create a Jupyterhub user and database.
#gosu postgres psql -c "CREATE DATABASE jupyterhub;"
#gosu postgres psql -c "CREATE USER jupyterhub WITH ENCRYPTED PASSWORD '$JPY_PSQL_PASSWORD';"
#gosu postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE jupyterhub TO jupyterhub;"
# Create a postgres checkpoints database.
#gosu postgres psql -c "CREATE DATABASE checkpoints;"
#gosu postgres psql -c "CREATE USER pgcontent WITH ENCRYPTED PASSWORD '$CHECKPOINTS_PASSWORD';"
#gosu postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE checkpoints TO pgcontent;"

# Alter pg_hba.conf to actually require passwords.  The default image exposes
# allows any user to connect without requiring a password, which is a liability
# if this is run forwarding ports from the host machine.
sed -ri -e '$ahost all all 0.0.0\/0 md5' "$PGDATA"/pg_hba.conf


# Add logging
sed -ri -e '$a\
log\_directory \= '\''pg\_log'\''\
log\_filename \= '\''postgresql\-\%Y\-\%m\-\%d\_\%H\%M\%S\.log'\''\
log\_statement \= '\''all'\''\
logging\_collector \= on\
log\_line\_prefix \= '\''\%t \%c \%u'\''\
log\_destination \= '\''stderr, csvlog'\''\
log\_rotation\_size \= 15MB\
log\_rotation\_age \= 1d\
' "$PGDATA"/postgresql.conf

#sleep 4
# Stop the daemon.  The root Dockerfile will restart the server for us.
#gosu postgres pg_ctl stop
#
#gosu postgres pg_ctl start
