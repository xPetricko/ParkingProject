from rest_framework import serializers
from ..models import NetModel

class NetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetModel
        fields = ('__all__')