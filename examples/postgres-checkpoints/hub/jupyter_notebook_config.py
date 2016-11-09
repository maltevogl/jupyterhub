import sys
import getpass
import subprocess
import os
import time
import pwd

from pgcontents import PostgresCheckpoints

#######
# Mounting owncloud webdav
# and link to ~/Notebooks for every user.
#######

credpath = os.path.expanduser('~') + '/.davfs2/secrets'
nbpath = os.path.expanduser('~') + '/Notebooks'

if not os.path.exists(nbpath):
    print('Creating mount point.')
    os.mkdir(nbpath)

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

if os.path.exists(credpath) and os.stat(credpath).st_size != 0:
    pass
else:
    os.mkdir(os.path.expanduser('~') + '/.davfs2')
    with open(credpath, 'w+') as out:
        username = get_username()
        print("Nice to meet you " + username + "!")
        password = getpass.getpass("Please enter your owncloud password:")
        out.write(nbpath + ' ' + username + ' ' + password)
    subprocess.call(['chmod', '600', credpath])

subprocess.call(['mount',nbpath])

c = get_config()


# Use Postgres for Checkpoints
c.ContentsManager.checkpoints_class = PostgresCheckpoints

pg_host = os.getenv('POSTGRES_PORT_5432_TCP_ADDR')
pg_pass2 = os.getenv('POSTGRES_ENV_CheckP_PSQL_PASSWORD')


# Setup database URL for checkpoints
c.PostgresCheckpoints.db_url = 'postgresql://pgcontent:{}@{}:5432/checkpoints'.format(
    pg_pass2,
    pg_host
)

#Default user to associate with running notebook:
#c.PostgresContentsManager.user_id = 'rhea'
# Is taken care of with getuser()!

# Maximum file size for database (might be useful ?!)
#c.PostgresContentsManager.max_file_size_bytes = 100000000 # 100MB File cap
