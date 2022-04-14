import torch

from ..models import Camera,NetModel


def objectDetectionOccupancy(camera: Camera,net_model: NetModel,image,intersection_threshold=0.6):
    net_model.loadNetModel()
    prediction_result = net_model.detectOccupancyObjectDetection(image)

    results = []

    for bounding_box in camera.boundingbox_set.all():
        occupied = False

        bounding_box_coordinates = bounding_box.getCoordinates()

        for prediction_box in prediction_result['boxes']:
            
            if occupied:
                break
            

            x_left = max(bounding_box_coordinates[0], prediction_box[0])
            y_top = max(bounding_box_coordinates[1], prediction_box[1])
            x_right = min(bounding_box_coordinates[2], prediction_box[2])
            y_bottom = min(bounding_box_coordinates[3], prediction_box[3])

            if x_right < x_left or y_bottom < y_top:
                continue

            intersection_area = (x_right - x_left) * (y_bottom - y_top)
            
            if intersection_area/bounding_box.getArea() > intersection_threshold:
                occupied = True

        results.append({
            'parking_space_id': bounding_box.parking_space.id, 
            'pakring_space_number': bounding_box.parking_space.parking_number,
            'bbox': bounding_box_coordinates,
            'occupied':occupied
            })    
            
    return results


            


    



def classficationOccupancy(parking_places, patches, net_model: NetModel):

    results = net_model.detectOccupancyClassification(patches)
    
    return [{ 'parking_space_id':parking_places[index].id, 'parking_space_number':parking_places[index].parking_number, 'result':result} for index,result in enumerate(results)]