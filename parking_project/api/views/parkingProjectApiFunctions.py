from email.mime import image

from parking_project.api.models import netModel

from ..models import NetModel, ParkingLot, Camera

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404

import datetime

from ..utils import loggers


from ..serializers import ParkingLotSerializer, CameraSerializer,BoundingBoxSerializer
from ..handlers import imageHandlers, occupancyDetectionHandlers

from skimage import io

from rest_framework.parsers import MultiPartParser,FormParser
parser_classes = [FormParser, MultiPartParser]

@api_view(['POST'])
def trainNet(request, net_model_id=None):

    net_model = NetModel.objects.get(id=net_model_id)
    net_model.loadNetModel()

    if net_model.type == "classification":
        train_csv_file = request.data['train_csv_file']
        test_csv_file = request.data['test_csv_file']


        filter = request.data.get('filter') or None
        filter_exclude = request.data.get('filter_exclude') or False
        batch_size = int(request.data.get('batch_size')) or 1
        save_if_better = request.data.get('save_if_better') or False


        train_log = net_model.train(
            train_csv_file=train_csv_file,
            filter=filter,
            filter_exclude=filter_exclude,
            batch_size=batch_size
            )

        test_log = net_model.test(
            test_csv_file=test_csv_file,
            filter=filter,
            filter_exclude=filter_exclude,
            batch_size=batch_size,
            save_if_better=save_if_better
            )

        
    
    elif net_model.type == "object_detection":
        
        train_xml_file = request.data['train_xml_file']
        batch_size = request.data.get('batch_size') or 1
        train_log = net_model.train(
            train_file= train_xml_file,
            batch_size= batch_size
            )
        net_model.saveModel()

    return Response({"status": "Finished", "train_log": train_log}, status=status.HTTP_200_OK)

    return Response({"status": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def testNetCsv(request, net_model_id=None):

    try:
        net_model = NetModel.objects.get(id=net_model_id)
        if net_model.type != "classification":
            return Response({"status": "Unable testo for this net model type.", "netmodel_type": netModel.type}, status=status.HTTP_400_BAD_REQUEST)
        net_model.loadNetModel()

        test_csv_file = request.data['test_csv_file']


        filter = request.data.get('filter') or None
        filter_exclude = request.data.get('filter_exclude') or False
        batch_size = int(request.data.get('batch_size')) or 1

        test_log = net_model.test(
            test_csv_file=test_csv_file,
            filter=filter,
            filter_exclude=filter_exclude,
            batch_size=batch_size,
            save_if_better=False
            )

        return Response({"status": "Finished", "test_log" : test_log}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"status": "Something went wrong.", "exception": str(type(e))+" - "+str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def detectOccupancy(request, parking_lot_id=None):


    parking_lot = get_object_or_404(ParkingLot,pk=parking_lot_id)
    camera  = get_object_or_404(parking_lot.camera_set,camera_number=request.data.get('camera_number'))
    net_model = get_object_or_404(NetModel,pk=request.data.get('net_model_id'))

    request_timestamp = datetime.datetime.now().astimezone()

    camera_image = request.data.get("camera_image")

    
    if not camera_image:
        return Response({"status": "Error ocured.", "error":"camera_image data required"}, status=status.HTTP_400_BAD_REQUEST)
    
    camera_image = io.imread(camera_image)
    

    if net_model.type == 'classification':    
        parking_places, patches = imageHandlers.getPatchesFromImage(camera,camera_image)

        result = occupancyDetectionHandlers.classficationOccupancy(parking_places,patches,net_model)
        
    elif net_model.type == 'object_detection':

        result = occupancyDetectionHandlers.objectDetectionOccupancy(camera_image,net_model)

    
    
    if result:
        loggers.occupancyLogger(result,request_timestamp)


    return Response({"status": "Finished","result":result}, status=status.HTTP_200_OK)
    


