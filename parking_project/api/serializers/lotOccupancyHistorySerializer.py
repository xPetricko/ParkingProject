from rest_framework import serializers
from ..models import LotOccupancyHistory

class LotOccupancyHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LotOccupancyHistory
        fields = ('__all__')