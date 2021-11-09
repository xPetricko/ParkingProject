from rest_framework import serializers
from .Models.ParkingLot import ParkingLot

class ParkingLotSerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length=200)
   
    class Meta:
        model = ParkingLot
        fields = ('__all__')