from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from ..models import ParkingSpace
from ..serializers import ParkingSpaceSerializer

# Create your views here.

class ParkingSpaceView(APIView):
    
    def get(self, request):
        serializer = ParkingSpaceSerializer(ParkingSpace.objects.all(), many=True)
        data = serializer.data
        if data:
            return Response({"status": "Parking lots", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "No parking lot"}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        serializer = ParkingSpaceSerializer(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)