from django.db import models

from .camera import Camera
from .parkingSpace import ParkingSpace



class BoundingBox(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE)
    x_pos = models.PositiveIntegerField()
    y_pos = models.PositiveIntegerField()
    x_width = models.PositiveIntegerField()
    y_width = models.PositiveIntegerField()