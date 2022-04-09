from sqlite3 import Timestamp
from django.db import models

from .parkingSpace import ParkingSpace



class SpaceOccupancyHistory(models.Model):
     
    parking_space = models.ForeignKey(ParkingSpace,on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    occupied = models.BooleanField()
     

    