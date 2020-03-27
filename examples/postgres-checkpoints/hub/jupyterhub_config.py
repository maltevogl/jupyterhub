# Configuration file for jupyterhub (postgres example).
import os
import sys
import netifaces

c = get_config()

# Tell HUB to listen on docker interace IP
# NOTE: Interface name can change depending on docker settings

docker0 = netifaces.ifaddresses('eth0')
docker0_ipv4 = docker0[netifaces.AF_INET][0]

c.JupyterHub.hub_ip = docker0_ipv4['addr']
c.JupyterHub.port = 8000

# Args for Spawner can be defined
#c.Spawner.notebook_dir = 'Notebooks'
#c.Spawner.args = ['--notebook-dir=~/Notebooks']

# Env variables kept by spawner
c.Spawner.env_keep = [
    'PATH',
    'PYTHONPATH',
    'CONDA_ROOT',
    'CONDA_DEFAULT_ENV'
    'VIRTUAL_ENV',
    'LANG',
    'LC_ALL',
    'CHECKPOINTS_PASSWORD']


c.JupyterHub.authenticator_class = 'oauthenticator.openid.OpenIDOAuthenticator'

c.LocalOpenIDOAuthenticator.create_system_users = True

c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set()

pg_pass = os.getenv('JPY_PSQL_PASSWORD')


c.JupyterHub.db_url = 'postgresql://jupyterhub:{}@jupyter-db:5432/jupyterhub'.format(
    pg_pass
)


join = os.path.join

here = os.path.dirname(__file__)
root = os.environ.get('OAUTHENTICATOR_DIR', here)
sys.path.insert(0, root)

with open(join(root, 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)

c.OpenIDOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# Self-signed certs are created while building docker
c.JupyterHub.ssl_key = '/etc/certs/ssl.key'
c.JupyterHub.ssl_cert = '/etc/certs/ssl.crt'

#c.JupyterHub.services = [
#    {
#        'name': 'cull-idle',
#        'admin': True,
#        'command': ['python3', '/srv/oauthenticator/cull-idle.py', '--timeout=7200','--#url=http://127.0.0.1:8081/api/routes']
#    }
#]

# Debugging
c.JupyterHub.debug_proxy = True
c.JupyterHub.log_level = 'DEBUG' or 10
c.Spawner.debug = True
