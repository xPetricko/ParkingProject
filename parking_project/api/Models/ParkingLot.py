from django.db import models
from django.db.models.signals import post_save
import os

class ParkingLot(models.Model):
    name = models.CharField(max_length=200, blank=False)
    address = models.CharField(max_length=200)
    total_spaces = models.PositiveIntegerField(default=0)
    

    @classmethod
    def create_parkinglot_dirs(cls, sender, instance, created, *args, **kwargs):
        if not created:
            return
        
        os.makedirs('./data/parkinglot/'+str(instance.id)+'/data', exist_ok=True)
        os.makedirs('./data/parkinglot/'+str(instance.id)+'/netmodels', exist_ok=True)
        

post_save.connect(ParkingLot.create_parkinglot_dirs, sender=ParkingLot)