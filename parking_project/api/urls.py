from django.urls import path

from .views import *

urlpatterns = [
    path('parkinglot/', ParkingLotView.as_view()),
    path('camera/', CameraView.as_view()),
    path('parkingspace/', ParkingSpaceView.as_view()),
    path('boundingbox/', BoundingBoxView.as_view()),
    path('parkinglot/<int:parking_lot_id>/upload_data', ParkingLotFilesUploadView.as_view()),
    #path('parkinglot/<int:parking_lot_id>/process_image', ParkingLotOccupacyView.as_view()),
    path('netmodel/', NetModelView.as_view()),
    path('netmodel/<int:netmodel_id>', NetModelOneView.as_view()),
    path('netmodel/<int:netmodel_id>/train', NetModelTrainView.as_view())    
]
