
from ..models import Camera, BoundingBox, ParkingSpace


def getPatchesFromImage(camera, camera_image):
    y_size, x_size, _ = camera_image.shape
    x_koef, y_koef = x_size/camera.resolution_x, y_size/camera.resolution_y

    patches = []
    parking_spaces = []

    for bounding_box in camera.boundingbox_set.all():
        patches.append(
            camera_image[
                int(bounding_box.y_pos*y_koef): int((bounding_box.y_pos+bounding_box.height)*y_koef),
                int(bounding_box.x_pos*x_koef): int((bounding_box.x_pos+bounding_box.width)*x_koef)
            ]
        )
        parking_spaces.append(bounding_box.parking_space)

    return parking_spaces,patches
