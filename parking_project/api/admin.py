from django.contrib import admin
from django.db import models

import os

from .parking_project.api.models import *
# Register your models here.



admin.site.register(Camera)
admin.site.register(LotOccupancyHistory)
admin.site.register(NetModel)
admin.site.register(ParkingLot)
admin.site.register(ParkingSpace)
admin.site.register(SpaceOccupancyHistory)
admin.site.register(BoundingBox)
