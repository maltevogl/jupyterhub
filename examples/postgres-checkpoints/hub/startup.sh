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
  useruuid = $(uuidgen)
  useradd -m -G davfs2,fuse -s /bin/bash $user
  mkdir /home/$user/LocalData
  mkdir /home/$user/Notebooks
  mkdir /home/$user/.davfs2
  echo "/home/$user/Notebooks openidconnect__$user $useruuid" > /home/$user/.davfs2/secrets
  curl --user admin:$NXTC_ADMIN_PWD $NXTC_API/users/ -d "userid=openidconnect__$user&password=$useruuid"
  sed -i "\$a$WEBDAV_HOST /home/$user/Notebooks davfs user,rw,noauto 0 0" /etc/fstab
  chown -R $user /home/$user
done

echo "Init database"
sleep 5
#Initializing postgres database with pgcontents
pgcontents init --no-prompt --db-url "postgresql://pgcontent:$CHECKPOINTS_PASSWORD@172.18.0.4:5432/checkpoints"

#Starting the hub
jupyterhub
