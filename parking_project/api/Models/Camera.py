from django.db import models
from Models.ParkingLot import ParkingLot

class Camera(models.Model):
     parkingLot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
     

    