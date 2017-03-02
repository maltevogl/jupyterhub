#!/bin/bash

for var in "$@"
  do 
    user=`echo $var | cut -f 1 -d' '`
    useruuid=`uuidgen`
    id -u $user &>/dev/null || useradd -m -G davfs2,fuse -s /bin/bash $user
    mkdir /home/$user/LocalData
    mkdir /home/$user/Notebooks
    mkdir /home/$user/.davfs2
    echo "/home/$user/Notebooks openidconnect__$user $useruuid" > /home/$user/.davfs2/secrets
    chown $user /home/$user/.davfs2/secrets
    chmod 600 /home/$user/.davfs2/secrets
    /usr/bin/curl -H "OCS-APIRequest: true" -u $ADMIN_USER:$ADMIN_PASSWORD --data "userid=openidconnect__$user&password=$useruuid"  $NXTC_API/users
    sed -i "\$a$WEBDAV_HOST /home/$user/Notebooks davfs user,noauto,uid=$user,file_mode=600,dir_mode=700 0 1" /etc/fstab
    chown -R $user /home/$user
done

