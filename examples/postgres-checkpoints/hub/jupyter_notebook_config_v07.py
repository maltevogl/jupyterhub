import sys
import getpass
import subprocess
import os
import time
import pwd

#######
# Mounting owncloud webdav
# and link to ~/Notebooks for every user.
#######

credpath = os.path.expanduser('~') + '/.davcreds'
nbpath = os.path.expanduser('~') + '/Notebooks'
davurl = 'davs://oc.rz-berlin.mpg.de/owncloud/remote.php/webdav'
davpath = os.path.expanduser('~') + '/.gvfs/dav:host=oc.rz-berlin.mpg.de,ssl=true,prefix=%2Fowncloud%2Fremote.php%2Fwebdav/Notebooks/ '

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

if os.path.exists(credpath):
    print("Continue")
else:
    with open(credpath, 'w') as out:
        username = get_username()
        print("Nice to meet you " + username + "!")
        password = getpass.getpass("Please enter your owncloud password:")
        out.write(username + '\n' + password + '\n')
    subprocess.call(['chmod', '600', credpath])


mountlist = [
             'gvfs-mount ' + davurl + ' <' + credpath,
             'ln -s ' + davpath + nbpath
            ]

for string in mountlist:
    print('Running: ' + string)
    p = subprocess.Popen(['dbus-launch','bash'],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    p.stdin.write(bytes(string, encoding='utf-8'))
    #print((p.communicate()[0]).decode())
    p.stdin.close()




from pgcontents import PostgresCheckpoints#, PostgresContentsManager

c = get_config()


# Use Postgres for Checkpoints and ContentsManager
# In the future we want to use only the checkpoint part,
# since owncloud will deal with filecontent
# UPDATED: The above mounts dav to local directory notebooks.
#  The jupyter filemanager deals with everything as usual.

c.ContentsManager.checkpoints_class = PostgresCheckpoints
#c.NotebookApp.contents_manager_class = PostgresContentsManager


# Env Var are not defined since singleusernotebook was started.
# workaround hard coded, BAD BAD
# UPDATED: setting c.Spawner.env_keep = List([...]) should help
import os;
pg_host = os.getenv('POSTGRES_PORT_5432_TCP_ADDR')
pg_pass2 = os.getenv('POSTGRES_ENV_CheckP_PSQL_PASSWORD')


# Setup database URL for checkpoints and content
c.PostgresCheckpoints.db_url = 'postgresql://pgcontent:{}@{}:5432/checkpoints'.format(
    pg_pass2,
    pg_host
)

#c.PostgresContentsManager.db_url = 'postgresql://pgcontent:{}@{}:5432/checkpoints'.format(
#    pg_pass2,
#    pg_host,
#)

# Default user to associate with running notebook:
# Is taken care of with getuser()
#c.PostgresContentsManager.user_id = 'rhea'

# Maximum file size for database (might be useful ?!)
#c.PostgresContentsManager.max_file_size_bytes = 100000000 # 100MB File cap
