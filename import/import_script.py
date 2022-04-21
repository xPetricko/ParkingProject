import csv
from getpass import getpass

import requests
from requests.auth import HTTPBasicAuth
import os




selected_dataset = input("Which dataset (custom,cnr):" )
if selected_dataset not in ("cnr","custom"):
    print("Selected wrong dataset")
    exit


X_RATIO = 1000/2592 if selected_dataset == "cnr" else 1
Y_RATIO = 750/1944 if selected_dataset == "cnr" else 1

names = {"cnr":"CNR Test Parking Lot", "custom": "Custom Parking Lot"}
resolutions = {"cnr":[1000,750], "custom": [1280,720]}
server_ip = input("Insert server IP: ")

login = input("Login: ")
password = getpass()
auth = HTTPBasicAuth(login, password)

del login,password


port = '8000' #input('Enter server API port: ')
server_url = 'http://'+server_ip+':'+port+'/api/'

print('Getting acces token')

res = requests.post(url=server_url+'parkinglot', auth=auth)



print('Starting script Dataset Import')
print('-'*20)


print('Creating Parking Lot')
headers = {'Content-type':'application/json'}
data = {
    'address' : 'Test Address '+selected_dataset,
    'name' : names[selected_dataset],
}
res = requests.post(url=server_url+'parkinglot',headers=headers,json=data, auth=auth)

if res.status_code==200:
    print('Parking Lot Created.')
else:
    print('Error. Something went wrong.')
    exit()

parking_lot_data = res.json()['data']
number_of_cameras = len(os.listdir("./data/"+selected_dataset+"/"))
print('Creating Cameras')
data = [ {
    'parking_lot': parking_lot_data['id'],
    'camera_number': i,
    'resolution_x': resolutions[selected_dataset][0],
    'resolution_y': resolutions[selected_dataset][1]
    } for i in range(1,number_of_cameras+1)
    ]

res = requests.post(url=server_url+'camera',headers=headers,json=data, auth=auth)
if res.status_code==200:
    print('Cameras created.')
else:
    print('Error. Something went wrong.')
    print(res.text)
    exit()

camera_data = {row['camera_number']:row for row in res.json()['data']}

boundingbox_data = []
parking_spaces_ids = []

print('Preparing Parking Space data')
for i in range(1,number_of_cameras+1):
    with open("./data/"+selected_dataset+"/camera"+str(i)+".csv","r") as file:
        csvreader = csv.reader(file)        
        header = next(csvreader)
        for row in csvreader:
            boundingbox_data.append({
                'camera_number': i,
                'parking_space_number': row[0],
                'x_pos': round(int(row[1])*X_RATIO),
                'y_pos': round(int(row[2])*X_RATIO),
                'width': round(int(row[3])*Y_RATIO),
                'height': round(int(row[4])*Y_RATIO)
            })
            if row[0] not in parking_spaces_ids:
                parking_spaces_ids.append(row[0])
parking_spaces_ids.sort()

print('Preparation done.')
print('Number of parking spaces: ', len(parking_spaces_ids))
print('Number of bounding boxes: ', len(boundingbox_data))

print('Creating parking spaces.')

data = [{
        'parking_number': parking_space_id,
        'parking_lot': parking_lot_data['id']
    } for parking_space_id in parking_spaces_ids
    ]

res = requests.post(url=server_url+'parkingspace',headers=headers,json=data, auth=auth)

if res.status_code==200:
    print('Parking Spaces created.')
else:
    print('Error. Something went wrong.')
    print(res.text)
    exit() 

print('Creating bounding boxes.')

parking_space_data = { row['parking_number']:row for row in res.json()['data']}

data = [
    {
        'x_pos': row['x_pos'],
        'y_pos': row['y_pos'],
        'width': row['width'],
        'height': row['height'],
        'camera': camera_data[row['camera_number']]['id'],
        'parking_space': parking_space_data[row['parking_space_number']]['id']
    } for row in boundingbox_data
]

res = requests.post(url=server_url+'boundingbox',headers=headers,json=data, auth=auth)

if res.status_code==200:
    print('Bounding boxes created.')
else:
    print('Error. Something went wrong.')
    print(res.text)
    exit 

print('Import completed!')
print("Parking lot ID:",parking_lot_data['id'])
print('-'*20)
