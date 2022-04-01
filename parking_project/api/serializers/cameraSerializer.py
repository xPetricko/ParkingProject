from rest_framework import serializers
from ..models import Camera

class CameraSerializer(serializers.ModelSerializer):
    parking_spaces = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='parking_number'
    )
    class Meta:
        model = Camera
        fields = ('__all__')