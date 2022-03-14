from rest_framework import serializers
from ..models import ParkingSpace

class ParkingSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpace
        fields = ('__all__')