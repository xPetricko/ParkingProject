from ipaddress import NetmaskValueError

from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import NetModel
from ..serializers import NetModelSerializer


class NetModelView(APIView):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = NetModelSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            obj.createNewNetModel()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class NetModelOneView(APIView):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    
    def get(self, request, net_model_id=None):

        net_model = NetModel.objects.get(id=net_model_id)
        net_model.loadNetModel()

        serializer = NetModelSerializer(net_model)
        data = serializer.data

        if data:
            return Response({"status": "Parking lots", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "No parking lot"}, status=status.HTTP_400_BAD_REQUEST)

