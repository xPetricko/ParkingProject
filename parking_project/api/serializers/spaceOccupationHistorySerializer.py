from rest_framework import serializers
from ..models import SpaceOccupationHistory

class SpaceOccupationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceOccupationHistory
        fields = ('__all__')