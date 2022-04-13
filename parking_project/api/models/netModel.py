

from django.db.models.signals import post_save
from django.db import models

from parking_project.settings import DEVICE, DEVICE_CPU

import torch
import torch.nn as nn
import torch.functional as F
import torch.optim as optim

import torchvision
from torchvision import transforms

import numpy as np

from datetime import datetime
import os

from parking_project.api.utils.dataloaders import PatchesFromCsvDataLoader, ObjectDetectionDataLoader

from ..utils.torchUtils import move_to

last_loaded_net_model = None


class NetModel(models.Model):
    path=models.CharField(max_length=250,null=True)
    type = models.CharField(max_length=20,choices=[("object_detection","object_detection"),( "classification", "classification")])
    trained = models.BooleanField(default=False)
    trained_date = models.DateField(null=True)
    accuracy = models.FloatField(default=0.0)


    def __init__(self, *args, **kwargs):
        super(NetModel, self).__init__(*args, **kwargs)
        self.model = None

    def loadNetModel(self):
        global last_loaded_net_model
        if last_loaded_net_model and last_loaded_net_model.id == self.id:
            self.model = last_loaded_net_model.model
        else:
            self.model = torch.load(self.path)
            last_loaded_net_model = self

    def createNewNetModel(self):
        if self.model or self.path:
            return None

        if self.type == "object_detection":
            self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained_backbone=True,num_classes=2)
        elif self.type == "classification":
            self.model = torch.hub.load('pytorch/vision:v0.10.0', 'alexnet', pretrained=True)
            self.model.classifier[4] = nn.Linear(4096,1024)
            self.model.classifier[6] = nn.Linear(1024,2)
        else:
            return False
        self.saveModel()

    def saveModel(self):
        self.model.to(DEVICE_CPU)
        if not self.path:
            self.path = './data/netmodel/model'+str(self.id)+"/model_parameters"
            self.trained=True
        torch.save(self.model, self.path)
        self.save()

    def predict(self):
        pass

    #The images have to be loaded in to a range of [0, 1] and then normalized using mean = [0.485, 0.456, 0.406] and std = [0.229, 0.224, 0.225].
    
    def train(self,train_file,filter=None,filter_exclude=False, batch_size=1):
        
        root_dir='./data/netmodel/model'+str(self.id)+'/data/'
        
        if self.type == "object_detection":
            
            dataloader = ObjectDetectionDataLoader(
                labels_file_path=train_file,
                root_dir=root_dir,
                batch_size=batch_size
            )

            return self.train_object_detection(dataloader)
            

        if self.type == "clasification":
            dataloader = PatchesFromCsvDataLoader(
                csv_file=train_file,
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

        for epoch in range(10):  # loop over the dataset multiple times
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
                if i % 500 == 0:    # print evforery 2000 mini-batches
                    log = log + '[%d, %5d] loss: %.4f\n' % (epoch + 1, i + 1, running_loss/500)
                    running_loss = 0.0
        log = log + 'Training finished'
    
        return log


    def train_object_detection(self,trainloader):
        self.model.to(DEVICE)
        self.model.double()
        train_log = "Start training: \n"
        for epoch in range(10):  # loop over the dataset multiple times

            for i, data in enumerate(trainloader, 0):
                images,targets = data[0].to(DEVICE), move_to(data[1],DEVICE) 
            
                output = self.model(images, targets)
                train_log = train_log + '[%d, %5d] classification_loss: %.4f detection_loss: %.4f\n' % (epoch + 1, i + 1, output['loss_classifier'], output['loss_objectness'])

                images.to(DEVICE_CPU),move_to(targets,DEVICE_CPU)
        return train_log

    def test(self,test_file,filter=None,filter_exclude=False, batch_size=1,save_if_better=False):
        if self.type == "object_detection":
            pass

        if self.type == "classification":
            root_dir='./data/netmodel/model'+str(self.id)+'/data/'
            test_data_loader = PatchesFromCsvDataLoader(
                csv_file=test_csv_file,
                root_dir=root_dir,
                filter=filter,
                filter_exclude=filter_exclude,
                batch_size=batch_size
                )
            return self.test_clasification(test_data_loader,save_if_better=save_if_better)

    def test_clasification(self,test_data_loader,save_if_better):

        correct = 0
        total = 0

        self.model.to(DEVICE)

        with torch.no_grad():
            for data in test_data_loader:
                images, labels = data[0].to(DEVICE), data[1].to(DEVICE)
                outputs = self.model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        log = 'Accuracy of the network on the %d test images: %d %%\n' % (total,100 * correct / total)
        if save_if_better and self.accuracy < 100 * correct / total:
            log += 'Saved. Old accuracy: %d, new accuracy: %d' % (self.accuracy, 100 * correct / total) 
            self.accuracy = 100 * correct / total
            self.save(update_fields=["accuracy"]) 
            self.saveModel()
            

        return log


    def detectOccupancyObjectDetection(self,image):

        self.model.to(DEVICE)
        image = torch.from_numpy(np.stack(image)).to(DEVICE)

        prediction = self.model([image])

        return prediction[0]

    def detectOccupancyClassification(self,patches):
        
        transform = transforms.Compose([
                                transforms.ToPILImage(),
                                transforms.Resize(256),
                                transforms.CenterCrop(224),
                                transforms.ToTensor(),
                                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                            ])

        
        transformed_patches = []

        for patch in patches:
            
            transformed_patches.append(transform(patch))


        transformed_patches = np.stack(transformed_patches)
        patches_shape = transformed_patches.shape

        transformed_patches = torch.from_numpy(transformed_patches.flatten()).reshape(patches_shape)

        if not self.model:
            self.loadNetModel()

        self.model.to(DEVICE)
        transformed_patches.to(DEVICE)


        result = self.model(transformed_patches).detach().numpy()

        return np.argmax(result, axis=1)





    @classmethod
    def createNetModelDir(cls, sender, instance, created, *args, **kwargs):
        if not created:
            return
        os.makedirs('./data/netmodel/model'+str(instance.id)+'/data', exist_ok=True)
            


post_save.connect(NetModel.createNetModelDir, sender=NetModel)