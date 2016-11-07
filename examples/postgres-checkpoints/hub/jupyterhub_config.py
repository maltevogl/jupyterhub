# Configuration file for jupyterhub (postgres example).
import os
c = get_config()

# spawn with Docker
#c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
#c.DockerSpawner.container_image = 'jupyterhub/singleuser'
#c.DockerSpawner.remove_containers = True

#network_name = os.environ['DOCKER_NETWORK_NAME']
#c.DockerSpawner.use_internal_ip = True
#c.DockerSpawner.network_name = network_name


# Self-signed certs are created while building docker
c.JupyterHub.ssl_key = '/etc/certs/ssl.key'
c.JupyterHub.ssl_cert = '/etc/certs/ssl.crt'

# Tell HUB to listen on docker interace IP
# NOTE: Interface name can change depending on docker settings
import netifaces
docker0 = netifaces.ifaddresses('eth0')
docker0_ipv4 = docker0[netifaces.AF_INET][0]

c.JupyterHub.hub_ip = docker0_ipv4['addr']


#c.DockerSpawner.hub_ip_connect = docker0_ipv4['addr']
#c.DockerSpawner.container_ip = '0.0.0.0'#docker0_ipv4['addr']
#c.JupyterHub.ip = docker0_ipv4['addr']
#c.JupyterHub.proxy_api_ip = docker0_ipv4['addr']
c.JupyterHub.port = 8000

# These environment variables are automatically supplied by the linked postgres
# container.

pg_pass = os.getenv('POSTGRES_ENV_JPY_PSQL_PASSWORD')
pg_host = os.getenv('POSTGRES_PORT_5432_TCP_ADDR')
oc_user = os.getenv('USER_NAME_ENV')

#c.JupyterHub.db_url = 'postgresql://jupyterhub:{}@{}:5432/jupyterhub'.format(
#    pg_pass,
#    pg_host,
#)


# Add some users.
#user = '{}'.format(oc_user)
#print(user)
#c.Authenticator.admin_users = {'admin'}
#c.Authenticator.whitelist = {user}

# Create users in system if added through webmask
#c.LocalAuthenticator.create_system_users = True

# Debugging
c.JupyterHub.debug_proxy = True

# Set the log level by value or name.
#c.JupyterHub.log_level = 'DEBUG'

# Enable debug-logging of the single-user server
c.Spawner.debug = True

# Env variables kept by spawner
c.Spawner.env_keep = [
    'PATH',
    'PYTHONPATH',
    'CONDA_ROOT',
    'CONDA_DEFAULT_ENV'
    'VIRTUAL_ENV',
    'LANG',
    'LC_ALL',
    'POSTGRES_PORT_5432_TCP_ADDR',
    'POSTGRES_ENV_CheckP_PSQL_PASSWORD']

#c.Spawner.notebook_dir = 'Notebooks'

# Further args possible:
#c.Spawner.args = ['--notebook-dir={path to your dir with Notebooks}/Notebooks']

c.JupyterHub.log_level = 10
c.JupyterHub.authenticator_class = 'oauthenticator.google.GoogleOAuthenticator'

c.LocalGitHubOAuthenticator.create_system_users = True

c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set()

import os
import sys

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

c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

c.JupyterHub.ssl_key = '/etc/certs/ssl.key'
c.JupyterHub.ssl_cert = '/etc/certs/ssl.crt'
