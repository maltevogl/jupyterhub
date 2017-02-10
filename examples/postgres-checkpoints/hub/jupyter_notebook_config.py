import subprocess
import os

from pgcontents import PostgresCheckpoints

#######
# Mounting owncloud webdav
# and link to ~/Notebooks for every user.
#######

nbpath = os.path.expanduser('~') + '/Notebooks'

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
