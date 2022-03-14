from django.contrib import admin
from django.db import models


from .models import *
# Register your models here.

admin.site.register(Camera)
admin.site.register(LotOccupationHistory)
admin.site.register(NetModel)
admin.site.register(ParkingLot)
admin.site.register(ParkingSpace)
admin.site.register(SpaceOccupationHistory)
admin.site.register(BoundingBox)
