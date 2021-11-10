from django.db import models
from parking_project.api.Models.ParkingLot import ParkingLot

class LotOccupationHistory(models.Model):
     
    parkingLot = models.ForeignKey(ParkingLot)
    date = models.DateField()
    occupied = models.BooleanField()
     

    