
import pandas as pd
import torch
from torch.utils.data import Dataset
from torchvision import transforms
import os
from skimage import io
import numpy as np
import math
from skimage.util import img_as_float
from PIL import Image


from ..utils.xmlparsers import xmlBoundingBoxParser

class PatchesFromCsvDataLoader(Dataset):
    def __init__(self, csv_file, root_dir, transform=None, filter=None, filter_exclude = False, batch_size = 1):
        self.data = pd.read_csv(root_dir+csv_file, sep=' ',names=['path','label'], header=None)
        if filter:
            if filter_exclude:
                self.data = self.data[~self.data.path.str.contains(filter)]
            else:
                self.data = self.data[self.data.path.str.contains(filter)]

        if transform:
            self.transform = self.transform = transforms.Compose([
                                transforms.Resize(256),
                                transforms.CenterCrop(224),
                                transforms.ToTensor(),
                                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                            ]) 
        else:
            self.transform = transforms.Compose([
                                transforms.Resize(256),
                                transforms.CenterCrop(224),
                                transforms.ToTensor(),
                                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                            ])

        self.root_dir = root_dir
        self.batch_size = batch_size
    
    def __len__(self):
        return math.ceil(len(self.data)/self.batch_size)
    
    def __getitem__(self, idx):
        if idx < 0 or idx*self.batch_size >= len(self):
            raise IndexError

        if torch.is_tensor(idx):
            idx = idx.tolist()

        values_idx = [x+idx*self.batch_size for x in range(0,self.batch_size) if x+idx*self.batch_size < len(self)]
        
        images = []
        labels = torch.tensor(self.data.label[values_idx].values)
        
        for img_path in self.data.path[values_idx]:

            image = Image.open(
                os.path.join(self.root_dir,img_path)
            ).convert("RGB")

            if self.transform:
                image = self.transform(image)

            images.append(image)

        images = np.stack(images)
        images_shape = images.shape

        images = torch.from_numpy(images.flatten()).reshape(images_shape)

        return images,labels


class ObjectDetectionDataLoader(Dataset):
    def __init__(self, labels_file_path, root_dir, transforms):
        self.data = open(root_dir+labels_file_path).read().splitlines()
        self.root_dir = root_dir


        
    
    
    
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        if idx < 0 or idx >= len(self):
            raise IndexError

            
        image_path, bboxes = xmlBoundingBoxParser(self.root_dir+self.data[idx])
            
        bboxes = torch.as_tensor(bboxes, dtype=torch.float32)

        img = Image.open(
            os.path.join(self.root_dir,image_path)
        ).convert("RGB")
            
        target = {}
        target['boxes'] = torch.as_tensor(bboxes, dtype=torch.float32)
        target['labels'] = torch.ones((len(bboxes),), dtype=torch.int64)
        target['area'] = (bboxes[:, 3] - bboxes[:, 1]) * (bboxes[:, 2] - bboxes[:, 0])
            
        self.transform = transforms.ToTensor()
        img = self.transform(img)
        # img, target = self.transform(img), self.transform(target)
        img = [img]
        target = [target]
        return img, target
