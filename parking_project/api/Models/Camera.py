from django.db import models
from parking_project.api.Models.ParkingLot import ParkingLot

class Camera(models.Model):
     parkingLot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
     

    