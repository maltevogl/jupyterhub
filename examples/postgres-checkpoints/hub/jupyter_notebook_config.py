import subprocess
import os

from pgcontents import PostgresCheckpoints

#######
# Mounting owncloud webdav
# and link to ~/Notebooks for every user.
#######

nbpath = os.path.expanduser('~') + '/Notebooks'
pidpath = '/var/run/mount.davfs/' + '-'.join(nbpath.split('/')[1:]) + '.pid'

pidpathexists = os.path.exists(pidpath)

files = subprocess.check_output(['find',nbpath,'-type','f','-print','-quit'])
file1 = files.decode().split('\n')[0]

if file1:
    content = subprocess.check_output(['head','-c','10',file1])
    if content: 
        pass
elif pidpathexists:
    pidfile = subprocess.check_output(['cat',pidpath])
    pidtop  = subprocess.check_output(['pgrep','-U',str(os.getuid()),'mount.davfs'])
    if pidfile == pidtop:
        pass
    else: 
        subprocess.call(['rm',pidpath])
else:
    pass    

subprocess.call(['mount',nbpath])

c = get_config()

# Use Postgres for Checkpoints
c.ContentsManager.checkpoints_class = PostgresCheckpoints

pg_pass2 = os.getenv('CHECKPOINTS_PASSWORD')


# Setup database URL for checkpoints
c.PostgresCheckpoints.db_url = 'postgresql://pgcontent:{0}@jupyter-db:5432/checkpoints'.format(
    pg_pass2
)

#Default user to associate with running notebook:
#c.PostgresContentsManager.user_id = 'rhea'
# Is taken care of with getuser()!

# Maximum file size for database (might be useful ?!)
#c.PostgresContentsManager.max_file_size_bytes = 100000000 # 100MB File cap
