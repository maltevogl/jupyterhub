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

ENV LANG C.UTF-8

ENV DASHBOARDS_VERSION 0.6.1
ENV CMS_VERSION 0.6.2

# Requiered packages, nano only for debugging. Consider adding apt-get upgrade
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev nano fuse uuid-runtime curl davfs2 python3-dev gfortran libatlas-base-dev python-dev graphviz libgraphviz-dev libav-tools \
    && apt-get update --fix-missing

RUN pip install pip psycopg2 jupyter nose netifaces python-dateutil pandas pypdf2 scipy matplotlib scikit-learn scikit-image \
        folium spacy cltk textblob pypdf2 graphviz jupyter_contrib_nbextensions jupyter_dashboards==$DASHBOARDS_VERSION  \
        jupyter_cms==$CMS_VERSION beautifulsoup4 mesa Cython hdbscan pyjwt

RUN jupyter dashboards quick-setup --sys-prefix

RUN jupyter cms quick-setup --sys-prefix

RUN jupyter nbextensions_configurator enable --system

RUN python3 -m textblob.download_corpora -d /usr/local/share/nltk_data all && python3 -m spacy.en.download all

RUN pip install git+https://github.com/pygraphviz/pygraphviz.git


############
# Security #
############

# self-signed certs for now
#RUN mkdir -p /etc/certs && touch /etc/certs/ssl.key && touch /etc/certs/ssl.crt

#RUN openssl req -x509 -nodes -days 730 -newkey rsa:2048 \
#                 -subj "/C=DE/ST=BER/L=BER/O=HUB/CN='$JUPYTER_HOST'" \
#                 -keyout /etc/certs/ssl.key -out /etc/certs/ssl.crt

#RUN openssl rsa -in /etc/certs/ssl.key -text > /etc/certs/ssl.pem

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

RUN pip install git+https://github.com/maltevogl/oauthenticator.git

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
