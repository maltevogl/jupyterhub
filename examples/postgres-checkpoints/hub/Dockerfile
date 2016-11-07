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
    && apt-get install -y libpq-dev nano fuse davfs2 \
    && apt-get update --fix-missing

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
RUN pip install git+https://github.com/jupyterhub/dockerspawner.git

RUN echo 'Install 11'

RUN pip install git+https://github.com/maltevogl/oauthenticator.git
#RUN pip install git+https://github.com/jupyterhub/oauthenticator.git

# Set credentials for JupyterHub
ARG USER_NAME=default
ARG USER_PASSWORD=userpwd
RUN echo $USER_NAME
ENV USER_NAME_ENV=$USER_NAME

RUN useradd -m -G shadow -p $(openssl passwd -1 admin) admin
RUN chown admin /srv/jupyterhub

# davfs group necessary for mounting owncloud with davfs
RUN groupadd fuse
#RUN useradd -m -G davfs2,fuse -p $(openssl passwd -1 $USER_PASSWORD) $USER_NAME

##############
# Add config #
##############

#COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

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

# Instead of gvfs mount use dafvs2 and edit fstab, and set suid for mount.dafvs2

#RUN sed -i '$a https://oc.rz-berlin.mpg.de/owncloud/remote.php/webdav /home/username/Notebooks davfs user,noauto,uid=username 0 0' /etc/fstab
#RUN bash -c "sed -i 's/username/$USER_NAME/g' /etc/fstab"

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

RUN mkdir /srv/oauthenticator
WORKDIR /srv/oauthenticator

ENV OAUTHENTICATOR_DIR /srv/oauthenticator

COPY jupyterhub_config.py jupyterhub_config.py
#COPY adduser.sh /srv/oauthenticator
#RUN chmod +x /srv/oauthenticator/adduser.sh
COPY userlist /srv/oauthenticator/userlist

RUN chmod 700 /srv/oauthenticator


COPY startup.sh /srv/jupyterhub

RUN chmod +x /srv/jupyterhub/startup.sh

#RUN sh /srv/oauthenticator/adduser.sh

CMD ["/srv/jupyterhub/startup.sh"]
