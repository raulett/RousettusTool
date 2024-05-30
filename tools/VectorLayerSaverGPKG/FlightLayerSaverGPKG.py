# coding=utf-8
import os
import pathlib
import random
from pathlib import Path

from PyQt5.QtGui import QColor
from qgis.core import QgsVectorLayer, QgsRendererCategory, QgsProject, QgsLayerTreeLayer, QgsVectorFileWriter, \
    QgsLayerTreeGroup, \
    QgsMarkerSymbol, QgsCategorizedSymbolRenderer, QgsFeature

from GUI.FlightPlanning.FlightPlanFeatureFabric import FlightPlanFeatureFabric
from tools import constants
from tools.ServiceClasses.RousettusLoggerHandler import RousettusLoggerHandler


class FlightLayerSaverGPKG:
    """

    """

    def __init__(self, method_name: str, temp_flights_layer: QgsVectorLayer, main_window):
        self.layer = temp_flights_layer
        self.main_window = main_window
        self.logger = RousettusLoggerHandler.get_handler().logger
        self.layer_group_path = constants.get_flight_group_path(method_name)
        self.layer_filepath = Path(QgsProject.instance().absolutePath(),
                                   constants.get_flight_file_path(method_name))

        self.logger.debug(f"FlightLayerSaverGPKG, layer_filepath: {self.layer_filepath}, layer: {self.layer.name()}")
        self._init_group_tree()
        self._init_vector_layer()
        self._add_layer_to_group()


    def _init_group_tree(self):
        """
        Initializes the layer group tree by creating the necessary group nodes if they don't already exist.

        :return: None
        """
        current_group_node = QgsProject.instance().layerTreeRoot()
        self.logger.debug(f"VectorLayerSaverGPKG, self.layer_group_path: {self.layer_group_path}")
        for group_name in self.layer_group_path:
            find_node = current_group_node.findGroup(group_name)
            if find_node is not None:
                current_group_node = find_node
            else:
                current_group_node = current_group_node.insertGroup(0, group_name)
        self.group_node = current_group_node

    def renew_features(self, temp_flights_layer: QgsVectorLayer):

        self.layer = temp_flights_layer
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = 'GPKG'
        options.layerName = self.layer.name()
        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
        _writer = QgsVectorFileWriter.writeAsVectorFormatV3(self.layer, str(self.layer_filepath),
                                                            QgsProject.instance().transformContext(), options)
        if _writer[0] != 0:
            raise IOError(_writer)
        self.layer = QgsVectorLayer(f"{str(self.layer_filepath)}|layername={self.layer.name()}", self.layer.name(), 'ogr')
        self._add_layer_to_group()

    def get_group_node(self) -> QgsLayerTreeGroup:
        """
        Get the group node.

        :return: The group node of the vector layer saver.

        :rtype: QgsLayerTreeGroup
        """
        return self.group_node

    
    def _init_vector_layer(self):
        """
        Initialize a gpkg file with vector layer and return it.

        :return: The initialized vector layer.
        """
        self.logger.debug(f"layer_filepath: "
                          f"{self.layer_filepath}, layer: {self.layer.name()}")
        if not os.path.exists(os.path.dirname(self.layer_filepath)):
            os.makedirs(os.path.dirname(self.layer_filepath))
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = 'GPKG'
        options.layerName = self.layer.name()
        if os.path.exists(self.layer_filepath):
            temp_layers = QgsVectorLayer(str(self.layer_filepath), '', 'ogr')
            if any(self.layer.name() in string for string in temp_layers.dataProvider().subLayers()):
                gpkg_layer = QgsVectorLayer(f"{str(self.layer_filepath)}|layername={self.layer.name()}",
                                            self.layer.name(),
                                            'ogr')
                layer_list = QgsProject.instance().mapLayersByName(self.layer.name())
                if layer_list:
                    if gpkg_layer.dataProvider().dataSourceUri() == layer_list[0].dataProvider().dataSourceUri():
                        self.layer = layer_list[0]
                    else:
                        self.layer = gpkg_layer
            else:
                options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
                _writer = QgsVectorFileWriter.writeAsVectorFormatV3(self.layer, str(self.layer_filepath),
                                                                    QgsProject.instance().transformContext(), options)
                if _writer[0] != 0:
                    raise IOError(_writer)
        else:
            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
            _writer = QgsVectorFileWriter.writeAsVectorFormatV3(self.layer, str(self.layer_filepath),
                                                                QgsProject.instance().transformContext(), options)
            if _writer[0] != 0:
                raise IOError(_writer)
            gpkg_layer = QgsVectorLayer(f"{str(self.layer_filepath)}|layername={self.layer.name()}",
                                        self.layer.name(),
                                        'ogr')
            if not gpkg_layer.isValid():
                raise IOError('layer {} failed to load'.format(self.layer.name()))
            self.layer = gpkg_layer

    def _add_layer_to_group(self):
        """
        Adds a layer to a layer group in the QGIS project.

        :param self: The instance of the VectorLayerSaverGPKG class.
        :return: None
        """
        layer_in_group_flag = False
        for child in self.group_node.children():
            if isinstance(child, QgsLayerTreeLayer) and child.name() == self.layer.name():
                if (child.layer() is None) or (child.layer().id() != self.layer.id()):
                    map_layer = child.layer()
                    if map_layer:
                        QgsProject.instance().removeMapLayer(map_layer)
                    break
                layer_in_group_flag = True
                break
        if not layer_in_group_flag:
            QgsProject.instance().addMapLayer(self.layer, False)
            self.group_node.addLayer(self.layer)

    def get_layer(self) -> QgsVectorLayer:
        return self.layer

    def set_style_to_flights_layer(self):
        """
        Служебный метод, чтобы установить стиль для слоя полетов.
        :param layer:
        :param plugin_path:
        :return:
        """
        unique_names = self.layer.dataProvider().uniqueValues(self.layer.dataProvider().fieldNameIndex('name'))

        self.logger.debug(f"layername: {self.layer.name()}, layer type {self.layer.dataProvider().dataSourceUri()}")
        self.logger.debug(f"layer id: {self.layer.id()}")
        self.layer.setRenderer(
            QgsCategorizedSymbolRenderer(
                'name',
                [
                    QgsRendererCategory(
                        name,
                        QgsMarkerSymbol.createSimple({'color': QColor(
                            random.randint(50, 255),
                            random.randint(50, 255),
                            random.randint(50, 255)),
                            "size": 2.6, }
                        ),
                        str(name)
                    )
                    for name in unique_names
                ]
            )
        )
        self.logger.debug(f"renderer: {self.layer.renderer()}, categories: {self.layer.renderer().categories()}")
        self.layer.triggerRepaint()
