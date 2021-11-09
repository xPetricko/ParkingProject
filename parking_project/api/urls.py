from django.urls import path
from .views import ParkingLotViews

urlpatterns = [
    path('parkinglot/', ParkingLotViews.as_view())
]