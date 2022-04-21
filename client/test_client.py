
from getpass import getpass
import os
import cv2
import requests
from requests.auth import HTTPBasicAuth


server_ip = input("Insert server IP: ")

login = input("Login: ")
password = getpass()
auth = HTTPBasicAuth(login, password)

del login,password

port = '8000' #input('Enter server API port: ')
server_url = 'http://'+server_ip+':'+port+'/api/'

print("Working dir is: "+ os.getcwd())
file_path = input("Enter path to file: ")

if not os.path.exists(file_path):
    print("File path not valid, exiting.")
    exit()

camera_image = open(file_path,"rb")

parking_lot_id = input("Enter parking lot id: ")
net_model_id = input("Enter net model id: ")
camera_number = input("Enter camera_number: ")

request_url = server_url+"parkinglot/"+parking_lot_id+"/detect_occupancy/"+net_model_id

data = {
    "camera_number": camera_number
}
files = {"camera_image": camera_image}

response = requests.post(request_url,files=files, data=data, auth=auth)
result = response.json()['result']


img=cv2.imread(file_path)


font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 1
fontColor              = (255,255,255)
thickness              = 1
lineType               = 2

for index,row in enumerate(result):
    bbox = row['bounding_box']
    # instead of creating a new image, I simply modify the old one
    g = int(not row['occupied']) * 255
    r = int(row['occupied']) * 255
    img=cv2.rectangle(img,(bbox[0],bbox[1]),(bbox[2],bbox[3]),(0,g,r),1)
    cv2.putText(img,row['parking_space_number'], 
    (bbox[0],bbox[1]), 
    font, 
    fontScale,
    fontColor,
    thickness,
    lineType)

# show the modified image with all the rectangles at the end.
cv2.imshow("Rectangled",img) 


cv2.waitKey(0)
cv2.destroyAllWindows()