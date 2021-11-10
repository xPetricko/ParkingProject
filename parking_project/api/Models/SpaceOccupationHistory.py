from django.db import models
from parking_project.api.Models.ParkingSpace import ParkingSpace

class SpaceOccupationHistory(models.Model):
     
    parking_space = models.ForeignKey(ParkingSpace)
    date = models.DateField()
    occupied = models.BooleanField()
     

    