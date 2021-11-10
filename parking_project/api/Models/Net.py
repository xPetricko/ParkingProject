from django.db import models
from parking_project.api.Models.ParkingLot import ParkingLot

class LotOccupationHistory(models.Model):
     
    parkingLot = models.ForeignKey(ParkingLot)
    trained = models.BooleanField()
    trained_date = models.DateField()

    path=models.CharField()
    type = (
        "object_detection", "clasification"
    ) 

    