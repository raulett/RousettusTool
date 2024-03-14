from PyQt5 import QtWidgets
from qgis.core import QgsVectorLayer, QgsCoordinateReferenceSystem

from tools.VectorLayerSaverGPKG.VectorLayerSaverGPKG import VectorLayerSaverGPKG
from GUI.FlightPlanning.FlightPlanFeatureFabric import FlightPlanFeatureFabric
from tools import constants


class FlightLayerSaverGPKG(VectorLayerSaverGPKG):
    def __init__(self, main_window: QtWidgets.QMainWindow, method_name: str, vector_layer_name: str):
        flights_group_path = constants.get_flight_group_path(method_name)
        flights_file_path = constants.get_flight_file_path(method_name)

        super(VectorLayerSaverGPKG, self).__init__(main_window, flights_group_path, flights_file_path, None)
        self.field_list = FlightPlanFeatureFabric.get_fields()
        layer = QgsVectorLayer(constants.geometry_types['PointZ'], constants.gps_layer_name, "memory")
        layer.setCrs(QgsCoordinateReferenceSystem("EPSG:4326"))
