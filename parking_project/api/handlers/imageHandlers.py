
from ..models import Camera, BoundingBox, ParkingSpace
import numpy

def getPatchesFromImage(camera, camera_image):
    x_size, y_size, _ = camera_image.size
    x_koef, y_koef = x_size/camera.resolution_x, y_size/camera.resolution_y

    patches = []
    parking_spaces = []
    bboxes = []

    image_arr = numpy.array(camera_image)

    for bounding_box in camera.boundingbox_set.all():
        patches.append(
            image_arr[
                int(bounding_box.y_pos*y_koef): int((bounding_box.y_pos+bounding_box.height)*y_koef),
                int(bounding_box.x_pos*x_koef): int((bounding_box.x_pos+bounding_box.width)*x_koef)
            ]
        )
        parking_spaces.append(bounding_box.parking_space)
        bboxes.append(bounding_box.getCoordinates())

    return parking_spaces, patches, bboxes
