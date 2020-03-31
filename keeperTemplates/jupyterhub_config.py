import sys
import os
from oauthenticator.generic import GenericOAuthenticator
from jupyterhub.spawner import LocalProcessSpawner

########################
# Spawner to enter Seafile Creds
########################
class EnvFormSpawner(LocalProcessSpawner):
    def _options_form_default(self):
        default_env = "SEAFILE_URL=https://box.hu-berlin.de\nSEAFILE_LIBRARY=notebooks\nSEAFILE_ACCESS_TOKEN="
        return """
        <div class="form-group">
            <label for="env">Environment variables (one per line)</label>
            <textarea rows=3 class="form-control" name="env">{env}</textarea>
        </div>
        """.format(
            env=default_env
        )

    def options_from_form(self, formdata):
        options = {}
        options['env'] = env = {}

        env_lines = formdata.get('env', [''])
        for line in env_lines[0].splitlines():
            if line:
                key, value = line.split('=', 1)
                env[key.strip()] = value.strip()
        return options

    def get_env(self):
        env = super().get_env()
        if self.user_options.get('env'):
            env.update(self.user_options['env'])
        return env

c = get_config()

########################
# TEMPLATES
########################
c.JupyterHub.template_paths = ['.',os.path.dirname(__file__) + '/keeperTemplates']
c.JupyterHub.template_vars = {
    'announcement_login': 'If you use this service for the first time, please provide a Seafile access token in the spawn menu.\
                           </br></br><a target="_blanck" href="https://workspace.mpiwg-berlin.mpg.de/gettoken" class="btn btn-success">Obtain token</a>'
    }

########################
# NETWORKING
########################
c.JupyterHub.ip = '127.0.0.1'
c.JupyterHub.hub_ip = '127.0.0.1'
c.JupyterHub.port = 8000

########################
# SPAWNER
########################
c.JupyterHub.spawner_class = EnvFormSpawner
c.Spawner.debug = True
c.Spawner.http_timeout = 60
c.Spawner.environment = {'JUPYTER_ENABLE_LAB': 'yes'}
c.Spawner.cmd = ['jupyterhub-singleuser']

########################
# HUB
########################
c.JupyterHub.log_level = 'DEBUG' or 10
c.JupyterHub.services = [
    {
        'name': 'cull-idle',
        'admin': True,
        'command': [sys.executable, os.path.dirname(__file__) + '/cull_idle_servers.py', '--timeout=3600']
    },
]

########################
# AUTHENTICATION
########################
c.JupyterHub.authenticator_class = GenericOAuthenticator
c.Authenticator.create_system_users = True
c.Authenticator.admin_users = admin = set(['mvogl'])
c.JupyterHub.authenticator_class.login_handler._OAUTH_AUTHORIZE_URL = "https://id.mpiwg-berlin.mpg.de/openid/authorize"
c.JupyterHub.authenticator_class.login_handler._OAUTH_TOKEN_URL = "https://id.mpiwg-berlin.mpg.de/openid/token"

c.GenericOAuthenticator.login_service = "MPIWG"
c.GenericOAuthenticator.token_url = "https://id.mpiwg-berlin.mpg.de/openid/token"
c.GenericOAuthenticator.userdata_url = "https://id.mpiwg-berlin.mpg.de/openid/userinfo"
c.GenericOAuthenticator.tls_verify = True
c.GenericOAuthenticator.username_key = 'preferred_username'

########################
# Load secrets
########################
try:
    with open(os.path.dirname(__file__) + '/.env_oidc', 'r') as file:
        data = file.readlines()
        callb, cid, secret = [x.strip() for x in data]
    c.GenericOAuthenticator.oauth_callback_url = callb
    c.OAuthenticator.client_id = cid
    c.OAuthenticator.client_secret = secret
except:
    raise ValueError('Please provide callback, client id and client secret for OIDC in file .env_oidc.')
