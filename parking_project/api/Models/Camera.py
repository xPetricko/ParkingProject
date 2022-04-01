from django.db import models



from .parkingLot import ParkingLot
from .parkingSpace import ParkingSpace

class Camera(models.Model):
     
     parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
     camera_number = models.PositiveIntegerField()
     parking_spaces = models.ManyToManyField(ParkingSpace, through="BoundingBox")
     resolution_x = models.PositiveIntegerField()
     resolution_y = models.PositiveIntegerField()

     

               
               
          
          
          

          



    