import datetime
from time import sleep, time
from xml.dom.pulldom import default_bufsize
from numpy import average
import requests
import re
from requests.auth import HTTPBasicAuth
import getpass
import os
import time
import threading

print("Working dir is: "+ os.getcwd())
images_file_path = input("Images paths file: ") or "shufled_images_paths.txt"
max_request_count = int(input("Requests number (default: 100): ") or 100)
parking_lot_id = input("Parking lot id: ") or "2"
net_model_id = input("Net model id: ") or "1"
default_camera_number = input("Default camera number (optional): ")
number_of_threads = int(input("Number of threads (default: 1): ") or 1)
server_ip = input("Server IP: ") or "192.168.0.110"

login = input("Login: ") or "admin"
password = getpass.getpass() or "Andrej03601"
auth = HTTPBasicAuth(login, password)

del login,password

images_paths = []
result_request_times = []

with open(images_file_path,"r") as f:
    images_paths = f.read().splitlines()

max_request_count = max_request_count if max_request_count <= len(images_paths) else len(images_paths)

thread_images_count = max_request_count // number_of_threads

input("Pres enter to start.")


def request_function(thread_number, images_paths):
    global server_ip,parking_lot_id,net_model_id,result_request_times
    request_times = []

    perc = 0

    for image_path in images_paths: 
        camera_number = (re.findall("camera([1-9])", image_path)+[default_camera_number])[0]

        image_file = open(image_path, "rb")

        request_url = "http://"+server_ip+":8000/api/parkinglot/"+parking_lot_id+"/detect_occupancy/"+net_model_id

        data = {"camera_number": camera_number, "skip_looger": True }
        files = {"camera_image": image_file}
        
        start_request_time = time.time()    
        response = requests.post(request_url,files=files, data=data, auth=auth)
        end_request_time = time.time()

        request_times.append(end_request_time-start_request_time)

        if (len(request_times)/len(images_paths))// 0.1 > perc:
            print("Thread %d - Completed %.2f%%" % (thread_number, len(request_times)/len(images_paths)*100))
            perc = (len(request_times)/len(images_paths)) // 0.1

        if response.status_code!=200:
            break 

        if len(request_times) >= len(images_paths):
            break
    
    result_request_times += request_times

threads = list()

all_start_time = time.time()

for index in range(number_of_threads):
    print("Starting thread %d." % index)
    x = threading.Thread(target=request_function, args=(index,images_paths[index*thread_images_count:(index+1)*thread_images_count-1]))
    threads.append(x)
    x.start()

for thread in threads:
    thread.join()

elapsed_time = time.time()-all_start_time

print("Finished. Elapesd time %d seconds" % (elapsed_time))
print("Total requests: %d (%.2f requests per second)" %(len(result_request_times), len(result_request_times)/elapsed_time))
print("Maximum time: ", max(result_request_times))
print("Minimum time: ", min(result_request_times))
print("Average time: ", sum(result_request_times)/len(result_request_times))

        





