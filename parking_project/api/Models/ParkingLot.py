from django.db import models

class ParkingLot(models.Model):
    address = models.CharField(max_length=200)