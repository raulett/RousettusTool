from qgis.core import QgsPointXY, QgsDistanceArea, QgsCoordinateReferenceSystem, QgsUnitTypes, QgsProject


# function usues qgis library
# returns distance between input points in meters
# function argument p1, p2 are sequences (x, y) points, crs is string like "EPSG:XXXX"
def qgs_get_distance(p1, p2, crs: str):
    qgs_point1 = QgsPointXY(p1[0], p1[1])
    qgs_point2 = QgsPointXY(p2[0], p2[1])
    # print('distance points', qgs_point1, ', ', qgs_point2)
    distance_area = QgsDistanceArea()
    crs = QgsCoordinateReferenceSystem(crs)
    distance_area.setSourceCrs(crs, QgsProject.instance().transformContext())
    distance_area.setEllipsoid(crs.ellipsoidAcronym())
    distance_m = distance_area.convertLengthMeasurement(distance_area.measureLine(qgs_point1, qgs_point2),
                                                        QgsUnitTypes.DistanceMeters)

    return distance_m
