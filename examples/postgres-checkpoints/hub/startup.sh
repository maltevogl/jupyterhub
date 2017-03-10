#!/bin/bash
echo -e $USERS_LIST > /srv/oauthenticator/userlist

openssl s_client -connect $NEXTCLOUD_HOST:443 -showcerts </dev/null 2>/dev/null | openssl x509 -outform PEM > certificate.pem
cp certificate.pem /etc/davfs2/certs
cp certificate.pem /srv/jupyterhub
cp /etc/certs/ssl.pem /etc/davfs2/certs
sed -i "\$aservercert certificate.pem\n" /etc/davfs2/davfs2.conf

echo "Adding users:"
cat /srv/oauthenticator/userlist

# adding admin user for docker
groupadd fuse
useradd -m -G shadow,davfs2,fuse -p $(openssl passwd -1 $ADMIN_PASSWORD_HUB) admin
chown admin /srv/jupyterhub

# sed doesnt work on files with no line
echo > /etc/fstab
IFS="
"
for line in `cat /srv/oauthenticator/userlist`; do
  test -z "$line" && continue
  user=`echo $line | cut -f 1 -d' '`
  # generate random password
  useruuid=`uuidgen`
  id -u $user &>/dev/null || useradd -m -G davfs2,fuse -s /bin/bash $user && mkdir -p /home/$user/{LocalData,Notebooks,.davfs2}
  # write credetials to davfs2 secrets file
  echo "/home/$user/Notebooks $user $useruuid" > /home/$user/.davfs2/secrets
  chown $user /home/$user/.davfs2/secrets
  chmod 600 /home/$user/.davfs2/secrets

  # test if user exists in nextcloud db.
  testUser=$(/usr/bin/curl --cacert certificate.pem -H "OCS-APIRequest: true" -u $ADMIN_USER:$ADMIN_PASSWORD $NXTC_API/users/$user | grep -P -o '(?<=.status\>)[a-z]{2}(?=\<\/status\>)')
  testResult="ok"
  printf "'$testUser'\n"
  printf "'$testResult'\n"

  if [ "$testUser" == "$testResult" ]
  then
    # user exists, change password to new random one
    echo "User '$user' exists, skipping..."
    /usr/bin/curl --cacert certificate.pem -X PUT -H "OCS-APIRequest: true" -u $ADMIN_USER:$ADMIN_PASSWORD $NXTC_API/users/$user -d key="password" -d value="$useruuid" > /dev/null
  else
    # user does not exist, add user with fixed pattern of username and random passoword
    echo "Adding user $user to database..."
    /usr/bin/curl --cacert certificate.pem -H "OCS-APIRequest: true" -u $ADMIN_USER:$ADMIN_PASSWORD --data "userid=$user&password=$useruuid"  $NXTC_API/users > /dev/null
  fi

  # Allow user to mount with davfs into the home folder
  sed -i "\$a$WEBDAV_HOST /home/$user/Notebooks davfs user,noauto,uid=$user,file_mode=600,dir_mode=700 0 1" /etc/fstab
  chown -R $user /home/$user
done

echo "Init database"
#sleep 5
#Initializing postgres database with pgcontents
pgcontents init --no-prompt --db-url "postgresql://pgcontent:$CHECKPOINTS_PASSWORD@jupyter-db:5432/checkpoints"

#Starting the hub
jupyterhub
