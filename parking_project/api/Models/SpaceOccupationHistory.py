from django.db import models

from .parkingSpace import ParkingSpace



class SpaceOccupationHistory(models.Model):
     
    parking_space = models.ForeignKey(ParkingSpace,on_delete=models.CASCADE)
    date = models.DateField()
    occupied = models.BooleanField()
     

    