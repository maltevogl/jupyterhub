#################
# Prerequisites #
#################

FROM jupyterhub/jupyterhub:latest

# Sync timezone (for logs)
ENV TZ=Europe/Berlin
RUN echo $TZ | tee /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata

# For debugging in docker
#RUN export TERM=xterm

# Requiered packages, nano only for debugging. Consider adding apt-get upgrade
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev nano fuse davfs2 \
    && apt-get update --fix-missing

RUN pip install psycopg2 jupyter nose netifaces

############
# Security #
############

# self-signed certs for now
RUN mkdir -p /etc/certs && touch /etc/certs/ssl.key && touch /etc/certs/ssl.crt

RUN openssl req -x509 -nodes -days 730 -newkey rsa:2048 \
                 -subj "/C=DE/ST=BER/L=BER/O=HUB/CN='$JUPYTER_HOST'" \
                 -keyout /etc/certs/ssl.key -out /etc/certs/ssl.crt

RUN openssl rsa -in /etc/certs/ssl.key -text > /etc/certs/ssl.pem

# secret for proxy and cookies
RUN export CONFIGPROXY_AUTH_TOKEN=`openssl rand -hex 32`
RUN export JPY_COOKIE_SECRET=`openssl rand -hex 1024`

#################
# Checkpoints   #
#################

RUN pip install -e git+https://github.com/quantopian/pgcontents#egg=pgcontents

#################
# Owncloud   #
#################

RUN pip install git+https://github.com/owncloud/pyocclient.git

##################
# User managment #
##################
#RUN pip install git+https://github.com/jupyterhub/dockerspawner.git

RUN pip install git+https://github.com/maltevogl/oauthenticator.git

RUN pip install pyjwt

# Set credentials for JupyterHub

##############
# Add config #
##############

RUN mkdir -p /etc/jupyter

COPY jupyter_notebook_config.py /etc/jupyter

#############################
# FilesManager via owncloud #
#############################

# Instead of gvfs mount use dafvs2 and edit fstab, and set suid for mount.dafvs2

RUN chmod u+s /usr/sbin/mount.davfs

###############################
# Get rid of Server Error 500 #
###############################

# Careful; uncommenting prevents opening of singleuser servers.
# On the other hand, now jupyterhub runs as root, which is a security issue
#USER rhea

# Second CMD should override the one defined in jupyterhub/jupyterhub
# Start-up script initializes database, such that postgres container
# can be build independently of jupyterhub container

###############################
# Setup OAUTH for sign-in     #
###############################

RUN apt-get install -y uuid-runtime curl

RUN mkdir /srv/oauthenticator
WORKDIR /srv/oauthenticator

ENV OAUTHENTICATOR_DIR /srv/oauthenticator

COPY jupyterhub_config.py jupyterhub_config.py
COPY cull_idle.py cull_idle.py
COPY userlist userlist

RUN chmod 700 /srv/oauthenticator

COPY startup.sh /srv/jupyterhub
RUN chmod +x /srv/jupyterhub/startup.sh
CMD ["/srv/jupyterhub/startup.sh"]
