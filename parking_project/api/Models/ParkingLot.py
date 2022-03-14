from django.db import models

class ParkingLot(models.Model):
    name = models.CharField(max_length=200, blank=False)
    address = models.CharField(max_length=200)
    total_spaces = models.PositiveIntegerField(default=0)
    