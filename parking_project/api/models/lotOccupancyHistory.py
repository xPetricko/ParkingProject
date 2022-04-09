from django.db import models

from .parkingLot import ParkingLot


class LotOccupancyHistory(models.Model):
     
    parking_lot = models.ForeignKey(ParkingLot,on_delete=models.PROTECT)
    date = models.DateTimeField()
    occupied = models.BooleanField()
     

    