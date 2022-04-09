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

        net_model = NetModel.objects.get(id=netmodel_id)
        net_model.loadNetModel()

        serializer = NetModelSerializer(net_model)
        data = serializer.data

        if data:
            return Response({"status": "Parking lots", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "No parking lot"}, status=status.HTTP_400_BAD_REQUEST)

