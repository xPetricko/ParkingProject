
SELECT ps.*, soh.*
FROM api_parkingspace ps
LEFT JOIN api_spaceoccupancyhistory soh ON (ps.id = soh.parking_space_id)
LEFT OUTER JOIN api_spaceoccupancyhistory soh2 ON (ps.id = soh2.parking_space_id AND 
    (soh.timestamp < soh2.timestamp OR (soh.timestamp = soh2.timestamp AND soh.id < soh.id)))
WHERE soh2.id IS NULL and ps.parking_lot_id = 13