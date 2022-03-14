from django.db import models

from .parkingLot import ParkingLot


class LotOccupationHistory(models.Model):
     
    parkingLot = models.ForeignKey(ParkingLot,on_delete=models.PROTECT)
    date = models.DateField()
    occupied = models.BooleanField()
     

    