from rest_framework import serializers
from ..models import ParkingLot
from .cameraSerializer import CameraSerializer

class ParkingLotOccupacySerializer(serializers.ModelSerializer):
    image = serializers.FileField()
    camera = CameraSerializer(many=False, read_only=True,)
    date = serializers.DateTimeField()

    class Meta:
        model = ParkingLot
        fields = ('image','camera','date')
   