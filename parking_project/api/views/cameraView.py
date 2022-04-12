from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Camera
from ..serializers import CameraSerializer


class CameraView(APIView):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = CameraSerializer(Camera.objects.all(), many=True)
        data = serializer.data
        if data:
            return Response({"status": "Cameras", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "No camera."}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        serializer = CameraSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
