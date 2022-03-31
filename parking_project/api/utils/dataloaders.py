import pandas as pd
import torch
from torch.utils.data import Dataset
from torchvision import transforms
import os
from skimage import io
import numpy as np
import math

class PatchesDataLoader(Dataset):
    def __init__(self, csv_file, root_dir, transform=None, filter=None, filter_exclude = False, batch_size = 1):
        self.data = pd.read_csv(root_dir+csv_file, sep=' ',names=['path','label'], header=None)
        if filter:
            if filter_exclude:
                self.data = self.data[~self.data.path.str.contains(filter)]
            else:
                self.data = self.data[self.data.path.str.contains(filter)]

        if transform:
            self.transform = self.transform = transforms.Compose([
                                transforms.ToPILImage(),
                                transforms.Resize(256),
                                transforms.CenterCrop(224),
                                transforms.ToTensor(),
                                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                            ]) 
        else:
            self.transform = transforms.Compose([
                                transforms.ToPILImage(),
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
        if idx < 0 or idx >= len(self):
            raise IndexError

        if torch.is_tensor(idx):
            idx = idx.tolist()

        values_idx = [x+idx*self.batch_size for x in range(0,self.batch_size) if x+idx*self.batch_size < len(self.data)]
        
        images = []
        labels = torch.tensor(self.data.label[values_idx].values)
        
        for img_path in self.data.path[values_idx]:

            image = io.imread(
                os.path.join(self.root_dir,img_path)
            )

            if self.transform:
                image = self.transform(image)

            images.append(image)

        images = np.stack(images)
        images_shape = images.shape

        images = torch.from_numpy(images.flatten()).reshape(images_shape)

        return images,labels