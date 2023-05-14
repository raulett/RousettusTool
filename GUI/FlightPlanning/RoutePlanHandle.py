from ...tools.Configurable import Configurable
from ...UI.FlightPlanning.RoutePlan_ui import Ui_RoutePlan_form
from ..InterfaceCustumClasses.SurveyMethodCombobox import SurveyMethodCombobox
from ...tools.DataProcessing.NodesFilesHandling import VectorLayerSaverGPKG
from ...tools.DataModels.Flight_planning.generate_takeoff_points_layer import generate_takeoff_points_layer
from ...tools.FlightPlanningLib.QThreadFlightRouteGenerator import QThreadFlightRouteGenerator
from ...tools.FlightPlanningLib.RoutePlanner import RoutePlanner

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QSize, Qt, QRegExp, QVariant
from PyQt5.QtGui import QValidator, QRegExpValidator, QPixmap

import os

from qgis.core import QgsMapLayerProxyModel, QgsVectorLayer, QgsCoordinateReferenceSystem, \
    QgsProject, QgsWkbTypes, QgsFields, QgsField


class RoutePlanHandle(Ui_RoutePlan_form, QDialog, Configurable):
    debug = 1

    def __init__(self, progressBar=None, logger=None, main_window=None, parent=None, config=None):
        super().__init__()
        self.route_planner_obj = None
        self.generate_btn_pushed_once = 0
        self.survey_method_combobox = None
        self.takeoff_points_layer = None

        self.module_tag = 'Route plan handler'
        self.main_window = main_window
        self.progressBar = progressBar

        self.vector_layer_saver = VectorLayerSaverGPKG.VectorLayerSaverGPKG()
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

        # connect signals
        # self.takeoff_point_layer_ComboBox.layerChanged.connect(
        #     lambda: self.takeoff_point_ComboBox.setLayer(self.takeoff_point_layer_ComboBox.currentLayer()))
        self.takeoff_point_ComboBox.layerChanged.connect(self.update_takeoff_points_features_combobox)
        self.pushButton_generate_routes.clicked.connect(self.generate_button_handler)

        # load config
        if self.debug:
            print("config is None: ", self.config is None)
        self.load_config()

    def update_takeoff_points_features_combobox(self):
        self.takeoff_point_ComboBox.setLayer(self.takeoff_point_layer_ComboBox.currentLayer())
        if self.takeoff_point_layer_ComboBox.currentLayer().featureCount() == 0:
            self.TO_feature_Label.setPixmap(QPixmap(":/plugins/RousettusTool/resources/warning.png"))
            self.TO_feature_Label.setToolTip(
                "There is no takeoff points. Add points to layer manually oк from other layer")
        else:
            self.TO_feature_Label.setPixmap(QPixmap())
            self.TO_feature_Label.setToolTip('')

    def generate_button_handler(self):
        print('hello from button handler')
        temp_profiles_layer_name = 'temp_profiles'
        out_of_plan_profiles_layer_name = "out_of_plan"
        routes_layer_name = "routes"
        self.route_planner_obj = RoutePlanner(self.profiles_mMapLayerComboBox.currentLayer(),
                                              self.service_dist_spinBox.value(),
                                              self.survey_dist_spinBox.value(),
                                              self.takeoff_point_ComboBox.feature(),
                                              self.takeoff_point_layer_ComboBox.currentLayer().crs(),
                                              selected_only_flag=self.checkBox.isChecked())
        self.route_planner_obj.process_algorithm()
        geom_type = "LineString"
        layer_crs = self.profiles_mMapLayerComboBox.currentLayer().crs()
        layers = QgsProject.instance().mapLayersByName(routes_layer_name)
        if len(layers) > 0:
            QgsProject.instance().removeMapLayer(layers[0].id())
        routes_layer = QgsVectorLayer(geom_type,
                                      routes_layer_name,
                                      "memory")
        routes_layer.setCrs(layer_crs)
        if routes_layer.isValid():
            temp_provider = routes_layer.dataProvider()
            features = self.route_planner_obj.get_planned_routes()
            if len(features) > 0:
                temp_provider.addAttributes(features[0].fields())
            routes_layer.updateFields()
            for feat in features:
                temp_provider.addFeature(feat)
            routes_layer.commitChanges()
            routes_layer.updateExtents()
            QgsProject.instance().addMapLayer(routes_layer)
        else:
            print("routes_layer memory layer invalid")

        geom_type = self.profiles_mMapLayerComboBox.currentLayer().wkbType()
        layer_crs = self.profiles_mMapLayerComboBox.currentLayer().crs()
        layers = QgsProject.instance().mapLayersByName(out_of_plan_profiles_layer_name)
        if len(layers) > 0:
            QgsProject.instance().removeMapLayer(layers[0].id())
        out_of_plan_profiles_layer = QgsVectorLayer(QgsWkbTypes.displayString(geom_type),
                                                    out_of_plan_profiles_layer_name,
                                                    "memory")
        out_of_plan_profiles_layer.setCrs(layer_crs)
        if out_of_plan_profiles_layer.isValid():
            temp_provider = out_of_plan_profiles_layer.dataProvider()
            temp_provider.addAttributes(self.profiles_mMapLayerComboBox.currentLayer().fields())
            out_of_plan_profiles_layer.updateFields()
            for feat in self.route_planner_obj.get_output_profiles():
                temp_provider.addFeature(feat)
            out_of_plan_profiles_layer.commitChanges()
            out_of_plan_profiles_layer.updateExtents()
            QgsProject.instance().addMapLayer(out_of_plan_profiles_layer)
        else:
            print("out_of_plan_profiles_layer memory layer invalid")
        print("count of out of plan feats: ", len(self.route_planner_obj.get_output_profiles()))

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
                    self.service_dist_spinBox.setValue(self.config[self.section_name].getint('serveice_route_limit'))
                if 'initial_profiles_layer' in self.config[self.section_name]:
                    layer_name = self.config[self.section_name].get('initial_profiles_layer')
                    item_index = self.profiles_mMapLayerComboBox.findText(layer_name, flags=Qt.MatchFixedString)
                    if self.debug:
                        print('match exactly ', item_index, 'Layer name: ',
                              self.config[self.section_name].get('initial_profiles_layer'))
                    if item_index >= 0:
                        self.profiles_mMapLayerComboBox.setCurrentIndex(item_index)
                # if 'takeoff_points_layer' in self.config[self.section_name]:
                #     layer_name = self.config[self.section_name].get('takeoff_points_layer')
                #     item_index = self.takeoff_point_layer_ComboBox.findText(layer_name, flags=Qt.MatchFixedString)
                #     if self.debug:
                #         print('loading point layer, layer name: ', layer_name, '\n', 'layer index: ', item_index)
                #         print('match exactly ', item_index, 'Layer name: ',
                #               self.config[self.section_name].get('takeoff_points_layer'))
                #     if item_index >= 0:
                #         self.takeoff_point_layer_ComboBox.setCurrentIndex(item_index)
                #     if 'takeoff_point_id' in self.config[self.section_name]:
                #         takeoff_point_id = self.config[self.section_name].getint('takeoff_point_id')
                #         self.takeoff_point_ComboBox.setLayer(self.takeoff_point_layer_ComboBox.currentLayer())
                #         try:
                #             self.takeoff_point_ComboBox.setLayer(self.takeoff_point_layer_ComboBox.currentLayer())
                #             self.takeoff_point_ComboBox.setFeature(takeoff_point_id)
                #         except:
                #             pass

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
            self.config[self.section_name]['serveice_route_limit'] = str(self.service_dist_spinBox.value())
            self.config[self.section_name]['initial_profiles_layer'] = str(
                self.profiles_mMapLayerComboBox.currentLayer().name() if
                self.profiles_mMapLayerComboBox.currentLayer().isValid() else None)
            # self.config[self.section_name]['takeoff_points_layer'] = str(
            #     self.takeoff_point_layer_ComboBox.currentLayer().name() if
            #     self.takeoff_point_layer_ComboBox.currentLayer().isValid() else None)
            self.config[self.section_name]['takeoff_point_id'] = str(
                self.takeoff_point_ComboBox.feature().id() if
                self.takeoff_point_ComboBox.feature().isValid() else None)
