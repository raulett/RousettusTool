from qgis.core import QgsVectorLayer, QgsCoordinateReferenceSystem, QgsFields, QgsField
from PyQt5.QtCore import QVariant


def generate_takeoff_points_layer():
    tmp_to_points_layer = QgsVectorLayer('point', 'takeoff_points', "memory")
    tmp_to_points_layer.setCrs(QgsCoordinateReferenceSystem("EPSG:4326"))
    point_fields = QgsFields()
    point_fields.append(QgsField('point_name', QVariant.String))
    tmp_to_points_layer.dataProvider().addAttributes(point_fields)
    tmp_to_points_layer.updateFields()
    return tmp_to_points_layer