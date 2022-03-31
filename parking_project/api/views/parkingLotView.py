
from django.shortcuts import get_object_or_404
from parking_project.api.models import parkingLot

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from ..models import ParkingLot
from ..serializers import ParkingLotSerializer, ParkingLotOccupacySerializer, CameraSerializer
from rest_framework.parsers import MultiPartParser,FormParser

class ParkingLotView(APIView):
    
    def get(self, request):
        serializer = ParkingLotSerializer(ParkingLot.objects.all(), many=True)
        data = serializer.data
        if data:
            return Response({"status": "Parking lots", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "No parking lot"}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        serializer = ParkingLotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

