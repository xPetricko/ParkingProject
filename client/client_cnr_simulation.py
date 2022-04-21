import datetime
from time import sleep, time
from xml.dom.pulldom import default_bufsize
import requests
import re
from requests.auth import HTTPBasicAuth
import getpass
import os
import time

print("Working dir is: "+ os.getcwd())
images_file_path = input("Images paths file: ")
parking_lot_id = input("Parking lot id: ")
net_model_id = input("Net model id: ")
default_camera_number = input("Default camera number (optional): ")

server_ip = input("Server IP: ")

login = input("Login: ")
password = getpass.getpass()
auth = HTTPBasicAuth(login, password)

del login,password

images_paths = []
simulated_timestamp = datetime.datetime.strptime("2022-04-20", "%Y-%m-%d")
last_timestamp_date = None

while True:

    with open(images_file_path,"r") as f:
        images_paths = f.read().splitlines()

    for image_path in images_paths:
        

        timestamp = image_path.split("/")[-1].replace(".jpg","")
        timestamp = datetime.datetime.strptime(timestamp,"%Y-%m-%d_%H%M")

        if last_timestamp_date != timestamp.date():
            last_timestamp_date = timestamp.date()
            simulated_timestamp = simulated_timestamp+datetime.timedelta(days=1)

        request_timestamp = simulated_timestamp+datetime.timedelta(hours=timestamp.hour,minutes=timestamp.minute)

        while request_timestamp > datetime.datetime.now():
            print("Request timestamp:" ,request_timestamp.strftime("%Y-%m-%d %H:%M:%S"))
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Time reached, waiting.")
            sleep(60*15)
        
        camera_number = (re.findall("camera([1-9])", image_path)+default_camera_number)[0]

        image_file = open(image_path, "rb")


        request_url = "http://"+server_ip+":8000/api/parkinglot/"+parking_lot_id+"/detect_occupancy/"+net_model_id

        data = {"camera_number": camera_number, "timestamp": request_timestamp.strftime("%Y-%m-%d %H:%M") }
        files = {"camera_image": image_file}

        response = requests.post(request_url,files=files, data=data, auth=auth)

        print("Date: "+request_timestamp.strftime("%Y-%m-%d")+" - "+image_path,"-",response.status_code)
        if response.status_code!=200:
            break 


        





