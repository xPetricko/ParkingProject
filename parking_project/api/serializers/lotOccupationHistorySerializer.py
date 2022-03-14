from rest_framework import serializers
from ..models import LotOccupationHistory

class LotOccupationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LotOccupationHistory
        fields = ('__all__')