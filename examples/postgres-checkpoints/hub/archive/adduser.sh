#!/bin/sh

IFS="
"
for line in `cat userlist`; do
  test -z "$line" && continue
  user=`echo $line | cut -f 1 -d' '`
  echo "adding user $user"
  useradd -m -s /bin/bash $user
  mkdir /home/$user/examples
  chown -R $user /home/$user/examples
done

echo "Init database"
#Initializing postgres database with pgcontents
#pgcontents init --no-prompt --db-url 'postgresql://pgcontent:...@...:5432/checkpoints'

#Starting the hub
#jupyterhub
