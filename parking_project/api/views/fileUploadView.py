import os
import shutil
from fileinput import filename
from zipfile import ZipFile

from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ParkingLotFilesUploadView(APIView):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]
    
    
    def post(self, request,format=None,net_model_id=None):
        file = request.data['data']
        dir_path = './data/netmodel/model'+str(net_model_id)+'/'
        with ZipFile(file, 'r') as zipObj:
            default_folder = zipObj.namelist()[0]
            # Extract all the contents of zip file in current directory
            zipObj.extractall(path=dir_path)
        
        if os.path.exists(dir_path+'__MACOSX'):
            shutil.rmtree(dir_path+'__MACOSX')

        os.rename(dir_path+default_folder, dir_path+"data/")

        

        return Response({"status": "success", "data": "File uploaded."}, status=status.HTTP_200_OK)

