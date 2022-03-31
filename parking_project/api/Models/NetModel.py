
from cmath import log
from selectors import SelectSelector
from django.db import models

from parking_project.settings import DEVICE, DEVICE_CPU

from .parkingLot import ParkingLot

import torch
import torch.nn as nn
import torch.functional as F
import torch.optim as optim

import torchvision

import os

from parking_project.api.utils import PatchesDataLoader

last_loaded_netmodel = None


class NetModel(models.Model):
    path=models.CharField(max_length=250,null=True)
    type = models.CharField(max_length=20,choices=[("object_detection","object_detection"),( "clasification", "clasification")])
    parking_lot = models.ForeignKey(ParkingLot,on_delete=models.PROTECT)
    trained = models.BooleanField(default=False)
    trained_date = models.DateField(null=True)


    def __init__(self, *args, **kwargs):
        super(NetModel, self).__init__(*args, **kwargs)
        self.model = None

    def loadNetModel(self):
        global last_loaded_netmodel
        if last_loaded_netmodel and last_loaded_netmodel.id == self.id:
            self.model = last_loaded_netmodel.model
        else:
            self.model = torch.load(self.path)
            last_loaded_netmodel = self

    def createNewNetModel(self):
        if self.model or self.path:
            return None

        if self.type == "object_detection":
            self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained_backbone=True,num_classes=2)
        if self.type == "clasification":
            self.model = torch.hub.load('pytorch/vision:v0.10.0', 'alexnet', pretrained=True)
            self.model.classifier[4] = nn.Linear(4096,1024)
            self.model.classifier[6] = nn.Linear(1024,2)
        self.saveModel()

    def saveModel(self):
        self.model.to(DEVICE_CPU)
        if not self.path:
            self.path = './data/parkinglot/'+str(self.parking_lot.id)+'/netmodels/model'+str(self.id)
        torch.save(self.model, self.path)
        self.save()

    def predict(self):
        pass

    #The images have to be loaded in to a range of [0, 1] and then normalized using mean = [0.485, 0.456, 0.406] and std = [0.229, 0.224, 0.225].
    
    def train(self,csv_file,filter=None,filter_exclude=False, batch_size=1):
        if self.trained:
            return

        if self.type == "object_detection":
            pass

        if self.type == "clasification":
            root_dir='./data/parkinglot/'+str(self.parking_lot.id)+'/data/PATCHES/'
            dataloader = PatchesDataLoader(
                csv_file=csv_file,
                root_dir=root_dir,
                filter=filter,
                filter_exclude=filter_exclude,
                batch_size=batch_size
                )
            return self.train_clasification(dataloader)
            

            

            
    
     

    def train_clasification(self,dataloader):
        log = ''
        #Loss
        criterion = nn.CrossEntropyLoss()
        self.model.to(DEVICE)
        torch.autograd.set_detect_anomaly(True)
        #Optimizer(SGD)
        optimizer = optim.SGD(self.model.parameters(), lr=0.001, momentum=0.9)

        for epoch in range(1):  # loop over the dataset multiple times
            running_loss = 0.0
            for i, data in enumerate(dataloader, 0):
            # get the inputs; data is a list of [inputs, labels]
                inputs, labels = data[0].to(DEVICE), data[1].to(DEVICE)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward + backward + optimize
                output = self.model(inputs)
                loss = criterion(output, labels)
                loss.backward()
                optimizer.step()

                # print statistics
                running_loss += loss.item()
                if i % 2:    # print evforery 2000 mini-batches
                    log = log + '[%d, %5d] loss: %.3f\n' % (epoch + 1, i + 1, running_loss / 2000)
                    running_loss = 0.0
        log = log + 'Training finished'
    
        return log


    def train_object_detection(self,trainloader):
        pass

    def test(self,testloader):

        correct = 0
        total = 0
        with torch.no_grad():
            for data in testloader:
                images, labels = data[0].to(DEVICE), data[1].to(DEVICE)
                outputs = self.model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        print('Accuracy of the network on the %d test images: %d %%' % (total,100 * correct / total))

    def predict(self,image):
        with torch.no_grad():
            self.loadNet()
            self.model(image)