import sys
import getpass
import subprocess
import os
import time

credpath = os.path.expanduser('~') + '/.davcreds'
nbpath = os.path.expanduser('~') + '/Notebooks'
fusepath = os.path.expanduser('~') + '/.dav'
davurl = 'davs://oc.rz-berlin.mpg.de/owncloud/remote.php/webdav/Notebooks'
davpath = os.path.expanduser('~') + '/.dav/dav\:host\=oc.rz-berlin.mpg.de\,ssl\=false\,prefix\=%2Fowncloud%2Fremote.php%2Fwebdav/Notebooks/ '

if os.path.exists(credpath):
    print("Continue")
else:
    with open(credpath, 'w') as out:
        username = input("Please enter the username for owncloud:")
        print("Nice to meet you " + username + "!")
        password = getpass.getpass("Please enter the corresponding password:")
        out.write(username + '\n' + password + '\n')
    subprocess.call(['chmod', '600', credpath])

if not os.path.exists(fusepath):
    os.makedirs(fusepath)
    subprocess.call(['chmod', '711', fusepath])

mountlist = ['/usr/lib/gvfs/gvfsd-fuse ' + fusepath,
             'gvfs-mount ' + davurl + ' <' + credpath,
             'ln -s ' + davpath + nbpath,
             'exit'
            ]

for string in mountlist:
    print('Running: ' + string)
    p = subprocess.Popen(['dbus-launch','bash'],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    p.stdin.write(bytes(string, encoding='utf-8'))
    #print((p.communicate()[0]).decode())
    time.sleep(3)
    p.stdin.close()


#subprocess.call(['/usr/lib/gvfs/gvfsd-fuse', fusepath])
#p = subprocess.Popen(['dbus-launch','bash'],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
#p.stdin.write(bytes('/usr/lib/gvfs/gvfsd-fuse ' + fusepath, encoding='utf-8'))
#print((p.communicate()[0]).decode())
#p.stdin.write(bytes('gvfs-mount ' + davurl + ' <' + credpath, encoding='utf-8'))
#print((p.communicate()[0]).decode())
#p.stdin.write(bytes('ln -s ' + davpath + '/Notebooks/ ' + nbpath, encoding='utf-8'))
#print((p.communicate()[0]).decode())
#p.stdin.close()
#
#p = subprocess.Popen(['dbus-launch','gvfs-mount',davurl],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
#p.stdin.write(bytes(credpath,encoding='utf-8'))
#print(p.communicate()[0])
#p.stdin.close()
#subprocess.call(['gvfs-mount', davurl, '<', credpath],shell=True)

#subprocess.call(['ln -s ' + davpath + '/Notebooks/ ' + nbpath])

#if not os.path.exists(nbpath):
#   os.makedirs(nbpath)

#sys.path.append(os.path.dirname(os.path.realpath(__file__)))
#from deiccontents import DeICContentsManager

from pgcontents import PostgresCheckpoints#, PostgresContentsManager

c = get_config()

# Using owncloud as contentmanager
#c.NotebookApp.contents_manager_class = DeICContentsManager

# Use Postgres for Checkpoints and ContentsManager
# In the future we want to use only the checkpoint part,
# since owncloud will deal with filecontent

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
