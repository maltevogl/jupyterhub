########
# Prep #
########

FROM postgres

ENV TZ=Europe/Berlin
RUN echo $TZ | tee /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata

RUN mkdir -p /docker-entrypoint-initdb.d

########
# Init #
########

# initdb.sh will be run by the parent container's entrypoint on container
# startup, prior to the the database being started.

COPY initdb.sh /docker-entrypoint-initdb.d/init.sh

RUN chmod +x /docker-entrypoint-initdb.d/init.sh

###############################
# Set passwords for databases #
###############################

# Replace this with your own passwords.

ENV JPY_PSQL_PASSWORD Jup?!er_D4taBa53
ENV CheckP_PSQL_PASSWORD pG5ql!_Ch3ck_p0int
