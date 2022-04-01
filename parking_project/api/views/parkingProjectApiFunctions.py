from email.mime import image

from ..models import NetModel, ParkingLot, Camera

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404


from ..serializers import ParkingLotSerializer, CameraSerializer,BoundingBoxSerializer
from ..handlers import imageHandler

from skimage import io

from rest_framework.parsers import MultiPartParser,FormParser
parser_classes = [FormParser, MultiPartParser]

@api_view(['POST'])
def trainNet(request, netmodel_id=None):
    try:
        netmodel = NetModel.objects.get(id=netmodel_id)
        netmodel.loadNetModel()

        train_csv_file = request.data['train_csv_file']
        test_csv_file = request.data['test_csv_file']


        filter = request.data.get('filter') or None
        filter_exclude = request.data.get('filter_exclude') or False
        batch_size = request.data.get('batch_size') or 1
        save_if_better = request.data.get('save_if_better') or False


        train_log = netmodel.train(
            train_csv_file=train_csv_file,
            filter=filter,
            filter_exclude=filter_exclude,
            batch_size=batch_size
            )

        test_log = netmodel.test(
            test_csv_file=test_csv_file,
            filter=filter,
            filter_exclude=filter_exclude,
            batch_size=batch_size,
            save_if_better=save_if_better
            )

        return Response({"status": "Finished", "train_log": train_log, "test_log" : test_log}, status=status.HTTP_200_OK)
    except:
        return Response({"status": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def testNetCsv(request, netmodel_id=None):

    try:
        netmodel = NetModel.objects.get(id=netmodel_id)
        netmodel.loadNetModel()

        test_csv_file = request.data['test_csv_file']


        filter = request.data.get('filter') or None
        filter_exclude = request.data.get('filter_exclude') or False
        batch_size = request.data.get('batch_size') or 1

        test_log = netmodel.test(
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
def detectOcupation(request, parking_lot_id=None, net_model_id=None):


    parking_lot = get_object_or_404(ParkingLot,pk=parking_lot_id)
    camera  = get_object_or_404(parking_lot.camera_set,camera_number=request.data.get('camera_number'))
    net_model = get_object_or_404(NetModel,pk=request.data.get('net_model_id'))

    camera_image = request.data.get("camera_image")

    if not camera_image:
        return Response({"status": "Error ocured.", "error":"camera_image data required"}, status=status.HTTP_400_BAD_REQUEST)
    
    camera_image = io.imread(camera_image)

    #net_model.detectOccupation(camera_image,camera)

    
    parking_places, patches = imageHandler.getPatchesFromImage(camera,camera_image)

    results = net_model.detectOccupation(patches)
    
    test = [[parking_places[index].parking_number, result]for index,result in enumerate(results)]

    


    return Response({"status": "Finished","result":test}, status=status.HTTP_200_OK)
    



