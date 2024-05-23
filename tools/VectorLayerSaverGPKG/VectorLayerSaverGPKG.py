"""
НЕ ИСПОЛЬЗУЕТСЯ
"""
import os.path
from pathlib import Path
import random
from typing import List

from PyQt5.QtGui import QColor
from qgis.core import QgsProject, QgsLayerTreeGroup, QgsVectorLayer, QgsVectorFileWriter, QgsLayerTreeLayer, \
    QgsRendererCategory, QgsArrowSymbolLayer, QgsLineSymbol

from tools.ServiceClasses.RousettusLoggerHandler import RousettusLoggerHandler


class VectorLayerSaverGPKG:
    """
    Вспомогательный класс для создания и управления векторным слоем для профилей, маршрутов и полетов.
    A helper class for creating and managing a vector layer for profiles, routes, and flights.
    """
    def __init__(self, main_window, group_path: List[str],
                 relative_filepath: Path, vector_layer: QgsVectorLayer):
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
        self.layer_filepath = Path(main_window.current_project_path, relative_filepath)
        self.logger.debug(f"VectorLayerSaverGPKG, layer_filepath: {self.layer_filepath}")

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
        if os.path.exists(self.layer_filepath):
            gpkg_layer = QgsVectorLayer(str(self.layer_filepath), self.layer.name(), 'ogr')
        else:
            options.driverName = 'GPKG'
            options.layerName = self.layer.name()
            _writer = QgsVectorFileWriter.writeAsVectorFormatV3(self.layer, str(self.layer_filepath),
                                                                QgsProject.instance().transformContext(), options)
            if _writer[0] != 0:
                raise IOError(_writer)
            gpkg_layer = QgsVectorLayer(str(self.layer_filepath), self.layer.name(), 'ogr')
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

    # def set_style_to_routes_layer(self, layer: QgsVectorLayer, plugin_path: str):
    #     '''
    #     Служебный метод, чтобы установить стиль для слоя маршрутов.
    #     :param layer:
    #     :param plugin_path:
    #     :return:
    #     '''
    #     style_file = os.path.join(plugin_path, 'resources', "layer_styles", 'routes_style.qml')
    #     res = layer.loadNamedStyle(style_file)
    #     unique_names = layer.dataProvider().uniqueValues(layer.dataProvider().fieldNameIndex('name'))
    #     renderer = layer.renderer()
    #     renderer.deleteAllCategories()
    #     for name in unique_names:
    #         color = QColor(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    #         new_symbol = QgsLineSymbol.createSimple({'type': 'arrow', 'color': color})
    #         arrow_layer = QgsArrowSymbolLayer.create({"arrow_width": "1",
    #                                                   "head_length": "2",
    #                                                   "head_thickness": "2",
    #                                                   "head_type": "0",
    #                                                   "arrow_type": "0",
    #                                                   "is_curved": "0",
    #                                                   "arrow_start_width": "1",
    #                                                   "color": color})
    #         new_symbol.changeSymbolLayer(0, arrow_layer)
    #         new_category = QgsRendererCategory(name, new_symbol, str(name))
    #         renderer.addCategory(new_category)
    #     return self
