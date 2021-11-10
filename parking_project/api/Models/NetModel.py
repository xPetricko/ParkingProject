from django.db import models
from Models.ParkingLot import ParkingLot

class NetModel(models.Model):
    path=models.CharField(max_length=250)
    type = (
        "object_detection", "clasification"
    ) 
    
    parkingLot = models.ForeignKey(ParkingLot,on_delete=models.PROTECT)
    trained = models.BooleanField()
    trained_date = models.DateField()

    def loadNet(self):
        #TODO Load net
        net = None
        self.net = net

     

    