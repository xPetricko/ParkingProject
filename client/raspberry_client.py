
from getpass import getpass
from os import fdopen

import requests
from requests.auth import HTTPBasicAuth



server_ip = input("Insert server IP: ")

login = input("Login: ")
password = getpass()
auth = HTTPBasicAuth(login, password)

del login,password


port = '8000' #input('Enter server API port: ')
server_url = 'http://'+server_ip+':'+port+'/api/'
