import os
import requests
from requests.auth import HTTPBasicAuth

adminCreds = os.getenv('NXTC_ADMIN_PWD')
users = os.getenv('USERS_LIST')
nxtapi = os.getenv('NXTC_API')

userapi = nxtapi + '/ocs/v1.php/cloud/users'

creds  = HTTPBasicAuth('admin', adminCreds)

userList = [x for x in users.split(' ') if x != 'admin']

for user in userList: 
    

