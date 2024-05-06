import os.path
import pathlib
from typing import List

from qgis.core import QgsProject, QgsLayerTreeGroup, QgsVectorLayer, QgsVectorFileWriter, QgsLayerTreeLayer

from tools.ServiceClasses.RousettusLoggerHandler import RousettusLoggerHandler


class VectorLayerSaverGPKG:
    """
    Вспомогательный класс для создания и управления векторным слоем для профилей, маршрутов и полетов.
    A helper class for creating and managing a vector layer for profiles, routes, and flights.
    """
    def __init__(self, main_window, group_path: List[str],
                 relative_filepath: List[str], vector_layer: QgsVectorLayer):
        """
        Constructor for the VectorLayerSaverGPKG class.

        :param main_window: Instance of the RousettusDataMainWindowHandle class.
        :param group_path: List of strings representing the path of the layer group in the layer tree.
        :param relative_filepath: List of strings representing the relative path of the layer file within the project directory.
        :param filename: String representing the filename of the layer file.
        :param vector_layer: Instance of the QgsVectorLayer class representing the vector layer to be saved.
        """
        self.logger = RousettusLoggerHandler.get_handler().logger
        self.group_node = None
        self.layer_group_path = group_path
        self.layer = vector_layer
        self.layer_filepath = os.path.join([main_window.current_project_path, relative_filepath])
        self.logger.debug(f"VectorLayerSaverGPKG, layer_filepath: {self.layer_filepath}")
        self._init_group_tree()
        self._init_vector_layer()
        self._add_layer_to_group()

    def _init_group_tree(self):
        """
        Initializes the layer group tree by creating the necessary group nodes if they don't already exist.

        :return: None
        """
        current_group_node = QgsProject.instance().layerTreeRoot()
        self.logger(f"VectorLayerSaverGPKG, self.layer_group_path: {self.layer_group_path}")
        for group_name in self.layer_group_path:
            find_node = current_group_node.findGroup(group_name)
            if find_node is not None:
                current_group_node = find_node
            else:
                current_group_node = current_group_node.insertGroup(0, group_name)
        self.group_node = current_group_node

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
        if not os.path.exists(os.path.dirname(self.layer_filepath)):
            os.makedirs(os.path.dirname(self.layer_filepath))
        options = QgsVectorFileWriter.SaveVectorOptions()
        path_to_gpkg = '{}.gpkg|layername={}'.format(self.layer_filepath, self.layer.name())
        if os.path.exists(self.layer_filepath + '.gpkg'):
            gpkg_layer = QgsVectorLayer(path_to_gpkg, self.layer.name(), 'ogr')
        else:
            options.driverName = 'GPKG'
            options.layerName = self.layer.name()
            _writer = QgsVectorFileWriter.writeAsVectorFormatV3(self.layer, self.layer_filepath,
                                                                QgsProject.instance().transformContext(), options)
            if _writer[0] != 0:
                raise IOError(_writer)
            gpkg_layer = QgsVectorLayer(path_to_gpkg, self.layer.name(), 'ogr')
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
                layer_in_group_flag = True
                break
        if not layer_in_group_flag:
            QgsProject.instance().addMapLayer(self.layer, False)
            self.group_node.addLayer(self.layer)

    def get_layer(self) -> QgsVectorLayer:
        return self.layer
