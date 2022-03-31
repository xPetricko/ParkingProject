from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser,FormParser
from zipfile import ZipFile
import os
import shutil

class ParkingLotFilesUploadView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    def post(self, request,format=None,parking_lot_id=None):
        file = request.data['data']

        with ZipFile(file, 'r') as zipObj:
            # Extract all the contents of zip file in current directory
            zipObj.extractall(path='./data/parkinglot/'+str(parking_lot_id)+'/')
        
        if os.path.exists('./data/parkinglot/'+str(parking_lot_id)+'/__MACOSX'):
            shutil.rmtree('./data/parkinglot/'+str(parking_lot_id)+'/__MACOSX')

        

        return Response({"status": "success", "data": "SUUPER"}, status=status.HTTP_200_OK)

