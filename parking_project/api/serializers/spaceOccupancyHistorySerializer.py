from rest_framework import serializers
from ..models import SpaceOccupancyHistory

class SpaceOccupancyHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceOccupancyHistory
        fields = ('__all__')