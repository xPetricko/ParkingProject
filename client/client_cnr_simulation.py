import datetime
from time import time
import requests
import re
from requests.auth import HTTPBasicAuth
import getpass
import os


print("Working dir is: "+ os.getcwd())
images_file_path = input("Images paths file: ")
parking_lot_id = input("Parking lot id: ")
net_model_id = input("Net model id: ")

server_ip = input("Server IP: ")

login = input("Login: ")
password = getpass.getpass()
auth = HTTPBasicAuth(login, password)

del login,password

images_paths = []

with open(images_file_path,"r") as f:
    images_paths = f.read().splitlines()

for image_path in images_paths:
    timestamp = image_path.split("/")[-1].replace(".jpg","")
    timestamp = datetime.datetime.strptime(timestamp,"%Y-%m-%d_%H%M").strftime("%Y-%m-%d %H:%M")


    camera_number = re.findall("camera([1-9])", image_path)[0]

    image_file = open(image_path, "rb")


    request_url = "http://"+server_ip+":8000/api/parkinglot/"+parking_lot_id+"/detect_occupancy/"+net_model_id

    data = {"camera_number": camera_number, "timestamp": timestamp }
    files = {"camera_image": image_file}

    response = requests.post(request_url,files=files, data=data, auth=auth)

    print(image_path,"-",response.status_code)
    if response.status_code!=200:
        break 


    





