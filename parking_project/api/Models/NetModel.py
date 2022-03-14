from importlib.resources import path
from nis import match
from unittest import case
from django.db import models

from .parkingLot import ParkingLot

import torch
import torch.nn as nn
import torch.functional as F


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

    def createNewNet(self):
        if not self.net or self.path:
            return None

        if self.type == "object_detection":
            self.net = torch.cuda_is_available()  
        if self.type == "clasification":
            self.net = torch.cuda_is_available()  


    def predict(self):
        pass
    
    def train(self):
        pass
    
     

    