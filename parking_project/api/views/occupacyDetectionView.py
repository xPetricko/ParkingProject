
from django.shortcuts import get_object_or_404
from parking_project.api.models import parkingLot

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from ..models import ParkingLot
from ..serializers import ParkingLotSerializer, ParkingLotOccupacySerializer, CameraSerializer
from rest_framework.parsers import MultiPartParser,FormParser


class trainView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request,parking_lot_id=None):
        
        parking_lot = get_object_or_404(ParkingLot,pk=parking_lot_id)
        camera  = get_object_or_404(parking_lot.camera_set,pk=request.data.get('camera_id') or -1)
        netModel = get_object_or_404(parking_lot.netmodel_set, pk=request.data.get('netmodel') or -1)


        
        return Response({"status": "success", "data": CameraSerializer(camera).data}, status=status.HTTP_200_OK)
        