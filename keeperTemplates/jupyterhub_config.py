## Paths to search for jinja templates, before using the default templates.
c.JupyterHub.template_paths = ['.','/home/mvogl/Dokumente/gwdgGitlab/jupyterhub/keeperTemplates']

## Extra variables to be passed into jinja templates
c.JupyterHub.template_vars = {'announcement_login':'If you use this service for the first time, please provide a KEEPER token.'}
c.Spawner.cmd = ['jupyterhub-singleuser']
## Extra settings overrides to pass to the tornado application.
#c.JupyterHub.tornado_settings = {}
