
from django.db import models

from .parkingLot import ParkingLot


class ParkingSpace(models.Model):
    parking_number = models.CharField(max_length=25)
    
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)

    