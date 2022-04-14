

from ..models import SpaceOccupancyHistory

def occupancyLogger(result,request_timestamp):
    SpaceOccupancyHistory.objects.bulk_create(
        [ 
            SpaceOccupancyHistory(
                parking_space_id=row['parking_space_id'],
                timestamp=request_timestamp,
                occupied=row["occupied"]
            ) for row in result
        ]
    )
