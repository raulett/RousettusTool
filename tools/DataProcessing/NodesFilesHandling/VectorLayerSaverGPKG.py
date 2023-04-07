import os
from qgis.core import QgsProject, QgsVectorLayer, QgsVectorFileWriter


class VectorLayerSaverGPKG():
    debug = 1
    def __init__(self):
        self.layer_group_path = None
        self.layer_filepath = None

    def init_group_tree(self, groups_structure: list):
        current_group_node = QgsProject.instance().layerTreeRoot()
        for group_name in groups_structure:
            find_node = current_group_node.findGroup(group_name)
            if find_node is not None:
                current_group_node = find_node
            else:
                current_group_node = current_group_node.addGroup(group_name)
        return current_group_node

    # get filepath and layer and returns layer, loaded from file to add it to project
    def init_layer_to_file(self, filename: str, layer: QgsVectorLayer):
        if self.debug:
            print('file to save: {}'.format(filename))
        path_to_file = os.path.dirname(filename)
        if not os.path.exists(path_to_file):
            os.makedirs(path_to_file)

        options = QgsVectorFileWriter.SaveVectorOptions()
        if os.path.exists(filename):
            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
        options.driverName = 'GPKG'
        options.layerName = layer.name()
        _writer = QgsVectorFileWriter.writeAsVectorFormatV3(layer, os.path.splitext(filename)[0],
                                                            QgsProject.instance().transformContext(), options)
        if _writer[0] != 0:
            raise IOError(_writer)

        path_to_gpkg = '{}|layername={}'.format(filename, layer.name())
        if self.debug:
            print('fool gpkg path_to_gpkg: {},\n layername: {}'.format(path_to_gpkg, layer.name()))
        output_layer = QgsVectorLayer(path_to_gpkg, layer.name(), 'ogr')
        if not output_layer.isValid():
            raise IOError('layer {} failed to load'.format(layer.name()))
        return output_layer

    # Get filesystem path functions
    def get_takeoff_points_filepath(self):
        self.layer_filepath = os.sep.join(['flights', 'takeoff_points.gpkg'])
        return self.layer_filepath

    def get_flight_profiles_filepath(self, method_name):
        self.layer_filepath = os.sep.join(['flights', method_name, f'{method_name}_survey_profiles.gpkg'])
        return self.layer_filepath

    def get_flight_routes_filepath(self, method_name):
        self.layer_filepath = os.sep.join(['flights', method_name, 'flight_routes.gpkg'])
        return self.layer_filepath

    # Qgis groupe hierarchy environment
    def get_takeoff_points_group(self):
        self.layer_group_path = {'groups': ['flights'], 'layer_name': 'takeoff_points'}
        return self.layer_group_path

    def get_survey_profiles_group(self, method_name):
        self.layer_group_path = {'groups': ['flights', method_name, 'profiles'], 'layer_name': 'survey_profiles'}
        return self.layer_group_path