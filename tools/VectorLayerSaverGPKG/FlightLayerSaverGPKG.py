from PyQt5 import QtWidgets
from PyQt5.QtCore import QVariant
from qgis.core import QgsField, QgsVectorLayer, QgsCoordinateReferenceSystem

from .VectorLayerSaverGPKG import VectorLayerSaverGPKG
from ...tools import constants
from ...GUI.FlightPlanning.FlightPlanFeatureFabric import FlightPlanFeatureFabric


class FlightLayerSaverGPKG(VectorLayerSaverGPKG):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super(VectorLayerSaverGPKG, self).__init__(main_window, )
        self.field_list = FlightPlanFeatureFabric.get_fields()
        layer = QgsVectorLayer(constants.geometry_types['PointZ'], constants.gps_layer_name, "memory")
        layer.setCrs(QgsCoordinateReferenceSystem("EPSG:4326"))
