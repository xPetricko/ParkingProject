from django.urls import path

from .views import *

urlpatterns = [
    path('parkinglot/', ParkingLotView.as_view()),
    path('camera/', CameraView.as_view()),
    path('parkingSpace/', ParkingSpaceView.as_view())
]