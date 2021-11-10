
from django.db import models
from Models.ParkingLot import ParkingLot
from Models.Camera import Camera

class ParkingSpace(models.Model):
    parking_number = models.CharField(max_length=25)
    
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    cameras = models.ManyToManyField(Camera)
    