#!/bin/bash
echo -e $USERS_LIST > /srv/oauthenticator/userlist

echo "Adding users:"
cat /srv/oauthenticator/userlist
  # sed doesnt work on files with no line
echo > /etc/fstab

IFS="
"
for line in `cat userlist`; do
  test -z "$line" && continue
  user=`echo $line | cut -f 1 -d' '`
  echo "adding user $user"
  useradd -m -G davfs2,fuse -s /bin/bash $user
  mkdir /home/$user/examples
  chown -R $user /home/$user/examples
  sed -i '$ahttps://oc.rz-berlin.mpg.de/owncloud/remote.php/webdav /home/username/Notebooks davfs username,noauto,uid=username 0 0' /etc/fstab
  # reading variables in '' is also a problem
  sed -i s/username/$user/g /etc/fstab
done

echo "Init database"
#Initializing postgres database with pgcontents
pgcontents init --no-prompt --db-url 'postgresql://pgcontent:pG5ql!_Ch3ck_p0int@172.17.0.2:5432/checkpoints'

#Starting the hub
jupyterhub
