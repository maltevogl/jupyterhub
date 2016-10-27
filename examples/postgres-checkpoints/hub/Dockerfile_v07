#################
# Prerequisites #
#################

FROM jupyterhub/jupyterhub

# Sync timezone (for logs)
ENV TZ=Europe/Berlin
RUN echo $TZ | tee /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata

# For debugging in docker
RUN export TERM=xterm

# Requiered packages, nano only for debugging. Consider adding apt-get upgrade
RUN apt-get update \
    && apt-get install -y libpq-dev nano owncloud-client python3-gi \
    && apt-get update --fix-missing

RUN apt-get update && apt-get install -y fuse gvfs-common gvfs-bin gvfs-daemons gvfs-libs gnome-keyring gvfs-backends gvfs-fuse  \
    && apt-get autoremove -y

RUN pip install psycopg2 jupyter nose netifaces

############
# Security #
############

# self-signed certs for now
RUN mkdir -p /etc/certs && touch /etc/certs/ssl.key && touch /etc/certs/ssl.crt

RUN openssl req -x509 -nodes -days 730 -newkey rsa:2048 \
                 -subj "/C=DE/ST=BER/L=BER/O=HUB/CN=jubHUB" \
                 -keyout /etc/certs/ssl.key -out /etc/certs/ssl.crt

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

# Set credentials for JupyterHub
ARG USER_NAME=default
ARG USER_PASSWORD=userpwd
RUN echo $USER_NAME
ENV USER_NAME_ENV=$USER_NAME

RUN useradd -m -G shadow -p $(openssl passwd -1 admin) admin
RUN chown admin /srv/jupyterhub

# Fuse group necessary for mounting owncloud with gvfs-mount and Fuse mountpoint
RUN groupadd fuse
RUN useradd -m -G fuse -p $(openssl passwd -1 $USER_PASSWORD) $USER_NAME

##############
# Add config #
##############

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

RUN mkdir -p /etc/jupyter

COPY jupyter_notebook_config.py /etc/jupyter

#############################
# FilesManager via owncloud #
#############################

# State on Github is "work in progress", the last commit is 5 months ago.
# Basic things are missing. Not working!
#COPY deiccontents /etc/jupyter/deiccontents

#RUN sed -i -e "s/<YOUR_USER>/$USER_NAME/g" /etc/jupyter/deiccontents/deicmanager.py \
#       -e "s/<YOUR_PASSWORD>/$USER_PASSWORD/g" /etc/jupyter/deiccontents/deicmanager.py

###############################
# Get rid of Server Error 500 #
###############################

# Careful; uncommenting prevents opening of singleuser servers.
# On the other hand, now jupyterhub runs as root, which is a security issue
#USER rhea

# Second CMD should override the one defined in jupyterhub/jupyterhub
# Start-up script initializes database, such that postgres container
# can be build independently of jupyterhub container

COPY startup.sh /srv/jupyterhub

RUN chmod +x /srv/jupyterhub/startup.sh

CMD ["/srv/jupyterhub/startup.sh"]
