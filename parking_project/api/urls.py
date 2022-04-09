from django.urls import path



from .views import *
from .views import parkingProjectApiFunctions as ParkingProjectApiFunctions

urlpatterns = [
    path('parkinglot', ParkingLotView.as_view()),
    path('camera', CameraView.as_view()),
    path('parkingspace', ParkingSpaceView.as_view()),
    path('boundingbox', BoundingBoxView.as_view()),
    path('netmodel', NetModelView.as_view()),
    path('netmodel/<int:net_model_id>', NetModelOneView.as_view()),
    path('netmodel/<int:net_model_id>/upload_data', ParkingLotFilesUploadView.as_view()),
    path('netmodel/<int:net_model_id>/train', ParkingProjectApiFunctions.trainNet),
    path('netmodel/<int:net_model_id>/test/csv', ParkingProjectApiFunctions.testNetCsv),
    path('parkinglot/<int:parking_lot_id>/detect_occupancy', ParkingProjectApiFunctions.detectOccupancy)
]
