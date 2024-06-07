import os
from qgis.core import QgsProject, QgsVectorLayer, QgsVectorFileWriter, QgsLayerTreeGroup, QgsLayerTreeLayer, \
    QgsRendererCategory, QgsLineSymbol, QgsArrowSymbolLayer
from typing import Dict
from PyQt5.QtGui import QColor
import random

class VectorLayerSaverGPKG:
    debug = 0
    add_layer_to_group_debug = 0
    set_style_to_profiles_layer_debug = 1

    def __init__(self):
        self.layer_group_path = None
        self.layer_filepath = None

    # Creates group tree in QGis interface. If groups exists it do nothing.
    # group_structure - list of groups in hierarchy
    def init_group_tree(self, groups_structure: list) -> QgsLayerTreeGroup:
        current_group_node = QgsProject.instance().layerTreeRoot()
        for group_name in groups_structure:
            find_node = current_group_node.findGroup(group_name)
            if find_node is not None:
                current_group_node = find_node
            else:
                current_group_node = current_group_node.addGroup(group_name)
        return current_group_node

    def add_layer_to_group(self, layer: QgsVectorLayer, group: QgsLayerTreeGroup) -> 'VectorLayerSaverGPKG':
        '''
        Служебная функция для добавления слоя в группу
        :param layer: Layer to add in group and to project
        :param group: Group where add layer.
        :return: self
        '''
        for child in group.children():
            if isinstance(child, QgsLayerTreeLayer) and child.name() == layer.name():
                group.removeChildNode(child)
        QgsProject.instance().addMapLayer(layer, False)
        group.addLayer(layer)
        return self

    # get full filename and layer, save layer to file if not exist and returns layer, loaded from file to add it to
    # project
    def init_layer_to_file(self, filename: str,
                           layer: QgsVectorLayer):
        '''
        Функция для сохранения слоя в файл,
        :param filename:
        :param layer:
        :return:
        '''
        if self.debug:
            print('file to save: {}'.format(filename))
        path_to_file = os.path.dirname(filename)
        if not os.path.exists(path_to_file):
            os.makedirs(path_to_file)

        options = QgsVectorFileWriter.SaveVectorOptions()
        path_to_gpkg = '{}|layername={}'.format(filename, layer.name())
        if os.path.exists(filename):
            gpkg_layer = QgsVectorLayer(path_to_gpkg, layer.name(), 'ogr')
            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
            if gpkg_layer.isValid():  # or not gpkg_layer.geometryType() == Qgis.GeometryType.Point:
                QgsVectorFileWriter.deleteShapeFile(gpkg_layer.source())
        options.driverName = 'GPKG'
        options.layerName = layer.name()
        _writer = QgsVectorFileWriter.writeAsVectorFormatV3(layer, os.path.splitext(filename)[0],
                                                            QgsProject.instance().transformContext(), options)
        if _writer[0] != 0:
            raise IOError(_writer)

        if self.debug:
            print('full gpkg path_to_gpkg: {},\n layername: {}'.format(path_to_gpkg, layer.name()))
        output_layer = QgsVectorLayer(path_to_gpkg, layer.name(), 'ogr')
        if not output_layer.isValid():
            raise IOError('layer {} failed to load'.format(layer.name()))
        return output_layer

    # Get filesystem path functions
    def get_takeoff_points_filepath(self):
        self.layer_filepath = os.sep.join(['flights', 'takeoff_points.gpkg'])
        return self.layer_filepath

    def get_flight_profiles_filepath(self, method_name):
        self.layer_filepath = os.sep.join(['flights', method_name, 'survey_profiles.gpkg'])
        return self.layer_filepath

    def get_flight_routes_filepath(self, method_name: str):
        self.layer_filepath = os.sep.join(['flights', method_name, 'flight_routes.gpkg'])
        return self.layer_filepath

    def get_flight_plans_filepath(self, method_name: str):
        self.layer_filepath = os.sep.join(['flights', method_name, 'flight_plans.gpkg'])
        return self.layer_filepath

    # Qgis group hierarchy environment
    def get_takeoff_points_group(self):
        self.layer_group_path = {'groups': ['flights'], 'layer_name': 'takeoff_points'}
        return self.layer_group_path

    def get_survey_profiles_group(self, method_name):
        self.layer_group_path = {'groups': ['flights', method_name, 'profiles'], 'layer_name': 'survey_profiles'}
        return self.layer_group_path

    def get_flight_routes_group(self, method_name: str) -> Dict:
        self.layer_group_path = {'groups': ['flights', method_name, 'routes'], 'layer_name': 'routes'}
        return self.layer_group_path

    def get_flight_planes_group(self, method_name: str) -> Dict:
        self.layer_group_path = {'groups': ['flights', method_name, 'flight_plans'], 'layer_name': 'flights'}
        return self.layer_group_path

    def set_style_to_profiles_layer(self, layer: QgsVectorLayer, plugin_path: str):
        style_file = os.path.join(plugin_path, 'resources', "layer_styles", 'profiles_style.qml')
        if self.set_style_to_profiles_layer_debug:
            print("current file path: ", style_file, '\nfile exists: ', os.path.exists(style_file))
        res = layer.loadNamedStyle(style_file)
        if self.set_style_to_profiles_layer_debug:
            print("result of load named file: ", res)
        layer.triggerRepaint()
        return self

    def set_style_to_routes_layer(self, layer: QgsVectorLayer, plugin_path: str):
        '''
        Служебный метод, чтобы установить стиль для слоя маршрутов.
        :param layer:
        :param plugin_path:
        :return:
        '''
        style_file = os.path.join(plugin_path, 'resources', "layer_styles", 'routes_style.qml')
        res = layer.loadNamedStyle(style_file)
        unique_names = layer.dataProvider().uniqueValues(layer.dataProvider().fieldNameIndex('name'))
        renderer = layer.renderer()
        renderer.deleteAllCategories()

        for name in unique_names:
            color = QColor(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            new_symbol = QgsLineSymbol.createSimple({'type': 'arrow', 'color': color})
            arrow_layer = QgsArrowSymbolLayer.create({"arrow_width": "1",
                                                      "head_length": "2",
                                                      "head_thickness": "2",
                                                      "head_type": "0",
                                                      "arrow_type": "0",
                                                      "is_curved": "0",
                                                      "arrow_start_width": "1",
                                                      "color": color})
            new_symbol.changeSymbolLayer(0, arrow_layer)
            new_category = QgsRendererCategory(name, new_symbol, str(name))
            renderer.addCategory(new_category)
        return self

