#!/bin/bash
echo -e $USERS_LIST > /srv/oauthenticator/userlist

echo "Adding users:"
cat /srv/oauthenticator/userlist

groupadd fuse
useradd -m -G shadow,davfs2,fuse -p $(openssl passwd -1 $ADMIN_PASSWORD) admin
chown admin /srv/jupyterhub
# sed doesnt work on files with no line
echo > /etc/fstab

IFS="
"
for line in `cat userlist`; do
  test -z "$line" && continue
  user=`echo $line | cut -f 1 -d' '`
  #echo "adding user $user"
  useradd -m -G davfs2,fuse -s /bin/bash $user
  mkdir /home/$user/LocalData
  chown -R $user /home/$user/LocalData
  sed -i "\$ahttps://$WEBDAV_HOST /home/$user/Notebooks davfs user,rw,noauto 0 0" /etc/fstab
  # reading variables in '' is also a problem
  #sed -i s/username/$user/g /etc/fstab
done

echo "Init database"
#Initializing postgres database with pgcontents
pgcontents init --no-prompt --db-url "postgresql://pgcontent:$POSTGRES_ENV_CheckP_PSQL_PASSWORD@$POSTGRES_PORT_5432_TCP_ADDR:5432/checkpoints"

#Starting the hub
jupyterhub
