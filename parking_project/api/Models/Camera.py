from django.db import models

from .parkingLot import ParkingLot
from .parkingSpace import ParkingSpace


class Camera(models.Model):
     
     parkingLot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
     camera_number = models.PositiveIntegerField()
     parking_space = models.ManyToManyField(ParkingSpace, through="BoundingBox")
     

    