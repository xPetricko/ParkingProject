import json
from os import fdopen
import requests
import csv


X_RATIO = 1000/2592
Y_RATIO = 750/1944


print('Starting script CNR Park Dataset Import')
print('-'*20)
ip = 'localhost' #input('Enter server API ip: ')
port = '8000' #input('Enter server API port: ')

server_url = 'http://'+ip+':'+port+'/api/'

print('Creating Parking Lot')
headers = {'Content-type':'application/json'}
data = {
    'address' : 'Test Address',
    'name' : 'CNR ParkLot',
}
res = requests.post(url=server_url+'parkinglot/',headers=headers,json=data)

if res.status_code==200:
    print('Parking Lot Created.')
else:
    print('Error. Something went wrong.')
    exit()

parking_lot_data = res.json()['data']

print('Creating Cameras')
data = [ {
    'parkingLot': parking_lot_data['id'],
    'camera_number': i,
    'resolution_x': 1000,
    'resolution_y':750
    } for i in range(1,10)
    ]

res = requests.post(url=server_url+'camera/',headers=headers,json=data)
if res.status_code==200:
    print('Cameras created.')
else:
    print('Error. Something went wrong.')
    exit()

camera_data = {row['camera_number']:row for row in res.json()['data']}

boundingbox_data = []
parking_spaces_ids = []

print('Preparing Parking Space data')
for i in range(1,10):
    with open("./data/camera"+str(i)+".csv","r") as file:
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

res = requests.post(url=server_url+'parkingspace/',headers=headers,json=data)

if res.status_code==200:
    print('Parking Spaces created.')
else:
    print('Error. Something went wrong.')
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

res = requests.post(url=server_url+'boundingbox/',headers=headers,json=data)

if res.status_code==200:
    print('Bounding boxes created.')
else:
    print('Error. Something went wrong.')
    exit 

print('Import completed!')
print('-'*20)