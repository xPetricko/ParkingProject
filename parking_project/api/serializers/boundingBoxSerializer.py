from rest_framework import serializers
from ..models import BoundingBox

class BoundingBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoundingBox
        fields = ('__all__')