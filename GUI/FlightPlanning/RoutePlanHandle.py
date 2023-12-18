import re
from typing import List

from ...tools.Configurable import Configurable
from ...UI.FlightPlanning.RoutePlan_ui import Ui_RoutePlan_form
from ..InterfaceCustumClasses.SurveyMethodCombobox import SurveyMethodCombobox
from ...tools.DataProcessing.NodesFilesHandling.VectorLayerSaverGPKG import VectorLayerSaverGPKG
from ...tools.DataModels.Flight_planning.generate_takeoff_points_layer import generate_takeoff_points_layer
from ...tools.FlightPlanningLib.QThreadFlightRouteGenerator import QThreadFlightRouteGenerator
from ...tools.FlightPlanningLib.RoutePlanner import RoutePlanner

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QSize, Qt, QRegExp, QVariant
from PyQt5.QtGui import QValidator, QRegExpValidator, QPixmap

import os

from qgis.core import QgsMapLayerProxyModel, QgsVectorLayer, QgsCoordinateReferenceSystem, \
    QgsProject, QgsWkbTypes, QgsFields, QgsField, QgsFeature


class RoutePlanHandle(Ui_RoutePlan_form, QDialog, Configurable):
    debug = 0
    generate_button_handler_debug = 0

    def __init__(self, progressBar=None, logger=None, main_window=None, parent=None, config=None):
        super().__init__()
        self.route_planner_obj = None
        self.generate_btn_pushed_once = 0
        self.survey_method_combobox = None
        self.takeoff_points_layer = None

        self.module_tag = 'Route plan handler'
        self.main_window = main_window
        self.progressBar = progressBar

        self.vector_layer_saver = VectorLayerSaverGPKG()
        self.setupUi(self)
        self.logger = logger
        self.section_name = 'route_plan'
        self.set_config(config)
        self.initGui()

    def initGui(self):
        self.survey_method_combobox = SurveyMethodCombobox(self)
        self.survey_method_combobox.setMinimumSize(QSize(240, 30))
        self.survey_method_combobox.setEditable(True)
        self.survey_method_combobox.setObjectName("choose_surv_method_comboBox")
        self.method_name_horizontalLayout.insertWidget(1, self.survey_method_combobox)

        self.lineEdit_lon.setValidator(QRegExpValidator(QRegExp("[+-]?[0-9]\\d{1,2}\\.\\d{,6}")))
        self.lineEdit_lat.setValidator(QRegExpValidator(QRegExp("[+-]?[0-9]\\d{1,2}\\.\\d{,6}")))
        self.lineEdit_alt.setValidator((QRegExpValidator(QRegExp("[+-]?[0-9]\\d*\\.\\d{,2}"))))

        self.takeoff_point_layer_ComboBox.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.profiles_mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.LineLayer)
        self.update_takeoff_points_features_combobox()
        # self.takeoff_point_ComboBox.setLayer(self.takeoff_point_layer_ComboBox.currentLayer())
        # print('current layer', self.takeoff_point_layer_ComboBox.currentLayer())

        # connect signals
        # self.takeoff_point_layer_ComboBox.layerChanged.connect(
        #     lambda: self.takeoff_point_ComboBox.setLayer(self.takeoff_point_layer_ComboBox.currentLayer()))
        self.takeoff_point_layer_ComboBox.layerChanged.connect(self.update_takeoff_points_features_combobox)
        self.pushButton_generate_routes.clicked.connect(self.generate_button_handler)

        # load config
        if self.debug:
            print("config is None: ", self.config is None)
        self.load_config()

    def update_takeoff_points_features_combobox(self):
        self.takeoff_point_ComboBox.setLayer(self.takeoff_point_layer_ComboBox.currentLayer())
        print('current layer', self.takeoff_point_layer_ComboBox.currentLayer())
        if ((self.takeoff_point_layer_ComboBox.currentLayer() is None) or
                (self.takeoff_point_layer_ComboBox.currentLayer().featureCount() == 0)):
            self.TO_feature_Label.setPixmap(QPixmap(":/plugins/RousettusTool/resources/warning.png"))
            self.TO_feature_Label.setToolTip(
                "There is no takeoff points. Add points to layer manually oк from other layer")
        else:
            self.TO_feature_Label.setPixmap(QPixmap())
            self.TO_feature_Label.setToolTip('')

    def generate_button_handler(self):

        self.route_planner_obj = RoutePlanner(self.profiles_mMapLayerComboBox.currentLayer(),
                                              self.service_dist_spinBox.value(),
                                              self.survey_dist_spinBox.value(),
                                              self.takeoff_point_ComboBox.feature(),
                                              self.takeoff_point_layer_ComboBox.currentLayer().crs(),
                                              selected_only_flag=self.checkBox.isChecked())
        self.route_planner_obj.process_algorithm()
        # Сначала добавим профиля вне планирования.
        input_layer_crs = self.profiles_mMapLayerComboBox.currentLayer().crs()
        routes = self.route_planner_obj.get_planned_routes()
        out_planned_profiles = self.route_planner_obj.get_output_profiles()
        profile_layer_num_pattern = r'(\d*$)'
        source_profiles_layer_name = self.profiles_mMapLayerComboBox.currentLayer().name()
        match = re.search(profile_layer_num_pattern, source_profiles_layer_name)
        if self.generate_button_handler_debug:
            print("input layer name: ", self.profiles_mMapLayerComboBox.currentLayer().name())
            print("match groups: ", match.groups())
        if len(match.groups()) > 0:
            output_prof_layer_number = int(match[1]) + 1
            output_profiles_layer_name = source_profiles_layer_name[:match.start(1)] + str(output_prof_layer_number)
        else:
            output_prof_layer_number = 0
            output_profiles_layer_name = source_profiles_layer_name + '_0'
        # Сформируем слой маршрутов.
        out_of_plan_profiles_layer = self.pack_lines_to_layer(out_planned_profiles,
                                                              output_profiles_layer_name,
                                                              input_layer_crs)
        # выясним наименование метода
        method_name = self.get_method_name(self.profiles_mMapLayerComboBox.currentLayer())
        # Подготовим файл слоя профилей и имя группы
        out_of_plan_group_list = self.vector_layer_saver.get_survey_profiles_group(method_name)
        path_to_profile_file = self.vector_layer_saver.get_flight_profiles_filepath(method_name)
        path_to_profile_file = os.sep.join([self.main_window.current_project_path, path_to_profile_file])
        output_profiles_group_node = self.vector_layer_saver.init_group_tree(out_of_plan_group_list['groups'])
        output_profiles_gpkg_layer = self.vector_layer_saver.init_layer_to_file(path_to_profile_file,
                                                                                out_of_plan_profiles_layer)
        self.vector_layer_saver.add_layer_to_group(output_profiles_gpkg_layer, output_profiles_group_node)
        self.vector_layer_saver.set_style_to_profiles_layer(output_profiles_gpkg_layer, self.main_window.plugin_path)
        source_layer_node = QgsProject.instance().layerTreeRoot().\
            findLayer(self.profiles_mMapLayerComboBox.currentLayer())
        if source_layer_node:
            source_layer_node.setItemVisibilityChecked(False)

        # сформируем название слоя
        if self.takeoff_point_ComboBox.feature().fields().indexFromName('name') != -1:
            takeoff_point_name = self.takeoff_point_ComboBox.feature().attribute('name')
        else:
            takeoff_point_name = str(self.takeoff_point_ComboBox.feature().id())
        routes_layer_name = 'routes_iteration-{}_{}'.format(output_prof_layer_number, takeoff_point_name)
        routes_layer = self.pack_lines_to_layer(routes,
                                                routes_layer_name,
                                                input_layer_crs)
        routes_group_list = self.vector_layer_saver.get_flight_routes_group(method_name)
        path_to_route_file = self.vector_layer_saver.get_flight_routes_filepath(method_name)
        path_to_route_file = os.sep.join([self.main_window.current_project_path, path_to_route_file])
        output_routes_group_node = self.vector_layer_saver.init_group_tree(routes_group_list['groups'])
        output_routes_gpkg_layer = self.vector_layer_saver.init_layer_to_file(path_to_route_file, routes_layer)
        self.vector_layer_saver.add_layer_to_group(output_routes_gpkg_layer, output_routes_group_node)
        self.vector_layer_saver.set_style_to_routes_layer(output_routes_gpkg_layer, self.main_window.plugin_path)

    def pack_lines_to_layer(self, line_features: List[QgsFeature],
                      layer_name: str,
                      layer_crs: QgsCoordinateReferenceSystem):
        '''
        Служебная функция, для упаковки списка профилей и маршрутов в слой типа LineString.
        :param line_features:
        :param layer_name:
        :param layer_crs:
        :return:
        '''
        result_layer = QgsVectorLayer("LineString", layer_name, "memory")
        result_layer.setCrs(layer_crs)
        provider = result_layer.dataProvider()
        if len(line_features) > 0:
            provider.addAttributes(line_features[0].fields())
        else:
            QMessageBox.warning(self, 'No routes generated', 'There was no routes generated')
        result_layer.updateFields()
        provider.addFeatures(line_features)
        provider.createSpatialIndex()
        result_layer.commitChanges()
        result_layer.updateExtents()
        return result_layer

    def get_method_name(self, layer: QgsVectorLayer) -> str:
        root = QgsProject.instance().layerTreeRoot()
        node = root.findLayer(layer)
        grandparent = node.parent().parent()
        if grandparent is not None:
            return grandparent.name()
        else:
            return 'unknown'


    def load_config(self):
        if self.config is not None:
            if self.section_name in self.config:
                if 'method_title' in self.config[self.section_name]:
                    self.survey_method_combobox.setCurrentIndex(
                        self.config[self.section_name].getint('method_title'))
                if 'takeoff_point_LON' in self.config[self.section_name]:
                    self.lineEdit_lon.setText(self.config[self.section_name].get('takeoff_point_LON'))
                if 'takeoff_point_LAT' in self.config[self.section_name]:
                    self.lineEdit_lat.setText(self.config[self.section_name].get('takeoff_point_LAT'))
                if 'takeoff_point_ALT' in self.config[self.section_name]:
                    self.lineEdit_alt.setText(self.config[self.section_name].get('takeoff_point_ALT'))
                if 'takeoff_point_name' in self.config[self.section_name]:
                    self.lineEdit.setText(self.config[self.section_name].get('takeoff_point_name'))
                if 'distance_limit' in self.config[self.section_name]:
                    self.survey_dist_spinBox.setValue(self.config[self.section_name].getint('distance_limit'))
                if 'serveice_route_limit' in self.config[self.section_name]:
                    self.service_dist_spinBox.setValue(self.config[self.section_name].getint('service_route_limit'))
                if 'initial_profiles_layer' in self.config[self.section_name]:
                    layer_name = self.config[self.section_name].get('initial_profiles_layer')
                    item_index = self.profiles_mMapLayerComboBox.findText(layer_name, flags=Qt.MatchFixedString)
                    if self.debug:
                        print('match exactly ', item_index, 'Layer name: ',
                              self.config[self.section_name].get('initial_profiles_layer'))
                    if item_index >= 0:
                        self.profiles_mMapLayerComboBox.setCurrentIndex(item_index)
                if 'use_selected_profiles_only_flag' in self.config[self.section_name]:
                    self.checkBox.setChecked(self.config[self.section_name]
                                             .getboolean('use_selected_profiles_only_flag'))
                if 'plan_ring_routes_flag' in self.config[self.section_name]:
                    self.checkBox_2.setChecked(self.config[self.section_name].getboolean('plan_ring_routes_flag'))

    def store_config(self):
        if self.config is not None:
            if self.section_name not in self.config:
                self.config[self.section_name] = {}
            self.config[self.section_name]['method_title'] = str(self.survey_method_combobox.currentIndex())
            self.config[self.section_name]['takeoff_point_LON'] = str(self.lineEdit_lon.text())
            self.config[self.section_name]['takeoff_point_LAT'] = str(self.lineEdit_lat.text())
            self.config[self.section_name]['takeoff_point_ALT'] = str(self.lineEdit_alt.text())
            self.config[self.section_name]['takeoff_point_name'] = str(self.lineEdit.text())
            if self.debug:
                print("self.config[self.section_name]['takeoff_point_name']: ",
                      self.config[self.section_name]['takeoff_point_name'])
                print("str(self.lineEdit.text()) ",
                      str(self.lineEdit.text()))
            self.config[self.section_name]['distance_limit'] = str(self.survey_dist_spinBox.value())
            self.config[self.section_name]['service_route_limit'] = str(self.service_dist_spinBox.value())
            self.config[self.section_name]['initial_profiles_layer'] = str(None if
                                            self.profiles_mMapLayerComboBox.currentLayer() is None else
                                            self.profiles_mMapLayerComboBox.currentLayer().name() if
                                            self.profiles_mMapLayerComboBox.currentLayer().isValid() else None)
            # self.config[self.section_name]['takeoff_points_layer'] = str(
            #     self.takeoff_point_layer_ComboBox.currentLayer().name() if
            #     self.takeoff_point_layer_ComboBox.currentLayer().isValid() else None)
            self.config[self.section_name]['takeoff_point_id'] = str(
                self.takeoff_point_ComboBox.feature().id() if
                self.takeoff_point_ComboBox.feature().isValid() else None)
            self.config[self.section_name]['use_selected_profiles_only_flag'] = str(self.checkBox.isChecked())
            self.config[self.section_name]['plan_ring_routes_flag'] = str(self.checkBox_2.isChecked())
