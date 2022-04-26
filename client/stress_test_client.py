import datetime
from time import sleep, time
import requests
import re
from requests.auth import HTTPBasicAuth
import getpass
import os
import time
import threading
print("Working dir is: "+ os.getcwd())
images_file_path = input("Images paths file: ") 
parking_lot_id = input("Parking lot id: ") 
net_model_id = input("Net model id: ") 
default_camera_number = input("Default camera number (optional): ")
server_ip = input("Server IP: ") or "192.168.0.110"

login = input("Login: ") or "admin"
password = getpass.getpass() 
auth = HTTPBasicAuth(login, password)

del login,password

images_paths = list()
request_times = list()
threads = list()
stop_threads = False

with open(images_file_path,"r") as f:
    images_paths = f.read().splitlines()

input("Pres enter to start.")



def request_function(thread_number, images_paths):
    global server_ip,parking_lot_id,net_model_id,request_times, threads, stop_threads, status_500_counter
    while not stop_threads:
        for image_path in images_paths: 
            camera_number = (re.findall("camera([1-9])", image_path)+[default_camera_number])[0]

            image_file = open(image_path, "rb")

            request_url = "http://"+server_ip+":8000/api/parkinglot/"+parking_lot_id+"/detect_occupancy/"+net_model_id

            data = {"camera_number": camera_number, "skip_looger": True }
            files = {"camera_image": image_file}
            
            start_request_time = time.time()    
            response = requests.post(request_url,files=files, data=data, auth=auth)
            end_request_time = time.time()
            if response.status_code==200:
                request_times.append([time.time(), len(threads), end_request_time-start_request_time])
            else:
                status_500_counter += 1
                stop_threads = True
                print("Thread %d - Request failed with status %d" % (thread_number, response.status_code))
            if stop_threads:
                print("Terminating thread %d." % (thread_number,))
                return 0
        





threshold = 20
last_request_times = 0
last_request_per_second = 0
repeat = 0
status_500_counter = 0

print("Starting thread %d." % len(threads))
x = threading.Thread(target=request_function, args=(len(threads),images_paths))
threads.append(x)
x.start()


split_time = time.time()
while True:
    
    if len(request_times) > last_request_times + len(threads)*threshold:
        time_now = time.time()
        actual_request_per_second = (len(request_times)-last_request_times)/(time_now - split_time)
        print("Checking improvement.")
        print("Last request/s: %.2f - Actual request/s: %.2f" % (last_request_per_second, actual_request_per_second))

        if last_request_per_second < actual_request_per_second or repeat%2:
            repeat += repeat % 2
            last_request_per_second = actual_request_per_second
            last_request_times = len(request_times)
            split_time = time.time()
            

            print("Starting thread %d." % len(threads))
            x = threading.Thread(target=request_function, args=(len(threads),images_paths))
            threads.append(x)
            x.start()
            
            
        else:
            if repeat>10 or status_500_counter > 10:
                print("No improvement after 10 repeating, terminating.")
                stop_threads = True
                break
            else:
                print("No improvement, repeating one more time.")
                last_request_per_second = actual_request_per_second
                last_request_times = len(request_times)
                split_time = time.time()
                repeat += 1

            
for thread in threads:
    thread.join()


save_to_file = ""
while save_to_file != "n" and save_to_file!= "y":
    save_to_file = input("Save log to file? y/n: ")

if save_to_file == "y":
    file_name = input("Log file name: ")
    file_out = open(file_name, "w+")
    
    file_out.write("Timestamp,Threads,Time\n")
    for row in request_times:
        file_out.write("%.2f,%d,%.2f\n" % (row[0], row[1], row[2]))
    file_out.close()

print("Finished")



            
            


        





