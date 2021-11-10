from django.db import models
from Models.ParkingLot import ParkingLot

class LotOccupationHistory(models.Model):
     
    parkingLot = models.ForeignKey(ParkingLot,on_delete=models.PROTECT)
    date = models.DateField()
    occupied = models.BooleanField()
     

    