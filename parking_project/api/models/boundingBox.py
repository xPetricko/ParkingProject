from django.db import models

from .camera import Camera
from .parkingSpace import ParkingSpace



class BoundingBox(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE)
    x_pos = models.PositiveIntegerField()
    y_pos = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    def getArea(self,size_coef=1):
        return self.height*self.width*(size_coef**2)

    def getCoordinates(self,size_coef=1):
        if size_coef!= 1:
            return (self.x_pos*size_coef, self.y_pos*size_coef,(self.x_pos+self.width)*size_coef, (self.y_pos+self.height)*size_coef)
        else:
            return (self.x_pos, self.y_pos, self.x_pos+self.width, self.y_pos+self.height)