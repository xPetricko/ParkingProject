from ipaddress import NetmaskValueError
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from ..models import NetModel
from ..serializers import NetModelSerializer

class NetModelView(APIView):
    
    def post(self, request):
        serializer = NetModelSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            obj.createNewNetModel()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class NetModelOneView(APIView):

      def get(self, request, netmodel_id=None):

        netmodel = NetModel.objects.get(id=netmodel_id)
        netmodel.loadNetModel()

        serializer = NetModelSerializer(netmodel)
        data = serializer.data

        if data:
            return Response({"status": "Parking lots", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "No parking lot"}, status=status.HTTP_400_BAD_REQUEST)

class NetModelTrainView(APIView):

      def get(self, request, netmodel_id=None):

        netmodel = NetModel.objects.get(id=netmodel_id)
        netmodel.loadNetModel()

        csv_file = request.data['csv_file']
        filter = request.data.get('filter') or None
        filter_exclude = request.data.get('filter_exclude') or False
        batch_size = request.data.get('batch_size') or 1
        
        log = netmodel.train(
            csv_file=csv_file,
            filter=filter,
            filter_exclude=filter_exclude,
            batch_size=batch_size
            )

        if log:
            return Response({"status": "Parking lots", "data": log}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "No parking lot"}, status=status.HTTP_400_BAD_REQUEST)