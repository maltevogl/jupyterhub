#!/bin/bash

if [ -z "$1" ]
  then
    echo "No parameter supplied."
    exit
fi

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters."
    exit
fi

userlist=$1

echo "Adding users:"
echo $userlist

IFS="
"
for line in `cat ./$userlist`; do
  test -z "$line" && continue
  user=`echo $line | cut -f 1 -d' '`
  # generate random password
  if id -u $user &>/dev/null; then
    echo "User exists locally, skip creation."
    continue
  else
    echo "User $user does not exist. Starting creation."
    useradd -m -G davfs2,fuse -s /bin/bash $user && mkdir -p /home/$user/{LocalData,Notebooks,.davfs2}
    # write credetials to davfs2 secrets file
    useruuid=`uuidgen`
    echo "/home/$user/Notebooks $user $useruuid" > /home/$user/.davfs2/secrets
    chown $user /home/$user/.davfs2/secrets
    chmod 600 /home/$user/.davfs2/secrets

    # test if user exists in nextcloud db.
    testUser=$(/usr/bin/curl --cacert certificate.pem -H "OCS-APIRequest: true" -u $ADMIN_USER:$ADMIN_PASSWORD $NXTC_API/users/$user | grep -P -o '(?<=.status\>)[a-z]{2}(?=\<\/status\>)')
    testResult="ok"
    printf "'$testUser'\n"
    printf "'$testResult'\n"

    if [ "$testUser" == "$testResult" ]; then
      # user exists, change password to new random one
      echo "User '$user' exists, skipping..."
      #/usr/bin/curl --cacert certificate.pem -X PUT -H "OCS-APIRequest: true" -u $ADMIN_USER:$ADMIN_PASSWORD $NXTC_API/users/$user -d key="password" -d value="$useruuid" > /dev/null
    else
      # user does not exist, add user with fixed pattern of username and random passoword
      echo "Adding user $user to database..."
      /usr/bin/curl --cacert certificate.pem -H "OCS-APIRequest: true" -u $ADMIN_USER:$ADMIN_PASSWORD --data "userid=$user&password=$useruuid"  $NXTC_API/users > /dev/null
    fi
    # Allow user to mount with davfs into the home folder
    sed -i "\$a$WEBDAV_HOST /home/$user/Notebooks davfs user,noauto,uid=$user,file_mode=600,dir_mode=700 0 1" /etc/fstab
    chown -R $user /home/$user
  fi
done
