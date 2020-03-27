## Paths to search for jinja templates, before using the default templates.
c.JupyterHub.template_paths = ['.','/home/mvogl/Dokumente/gwdgGitlab/jupyterhub/keeperTemplates']

## Extra variables to be passed into jinja templates
c.JupyterHub.template_vars = {
    'announcement_login': 'If you use this service for the first time, please provide a Seafile access token in the spawn menu.'
    }
c.Spawner.cmd = ['jupyterhub-singleuser']


"""
Example JupyterHub config allowing users to specify environment variablesrgs
"""

from jupyterhub.spawner import LocalProcessSpawner

class DemoFormSpawner(LocalProcessSpawner):
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


c.JupyterHub.spawner_class = DemoFormSpawner
