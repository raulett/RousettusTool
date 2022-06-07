from ...UI.FlightPlanning.FlightPlan_prototype_ui import Ui_FlightPlan_form

from qgis.PyQt.QtWidgets import QDialog
from qgis.gui import QgsFileWidget
from qgis.core import QgsMapLayerProxyModel, QgsCoordinateTransform, QgsCoordinateReferenceSystem, QgsProject

from PyQt5.QtGui import QPixmap, QDoubleValidator
from PyQt5.QtCore import QLocale

import os



class FlightPlanningHandle(Ui_FlightPlan_form, QDialog):
    debug = 1
    def __init__(self, progressBar=None, logger=None, main_window=None, parent=None):
        super(FlightPlanningHandle, self).__init__(parent)
        self.setupUi(self)
        self.module_tag = 'Fligh planning handler'
        self.main_window = main_window
        self.logger = logger


        self.flight_missions_save_path = os.path.join(self.main_window.current_project_path, "flights", "FlightMissions")
        self.flights_layers_save_path = os.path.join(self.flight_missions_save_path, 'layers')
        self.exported_flights_save_path = os.path.join(self.flight_missions_save_path, 'FM_export')

        self.initGui()

    def initGui(self):
        self.takeoff_point_layer_ComboBox.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.profiles_mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.LineLayer)
        self.DEM_mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.update_takeoff_feats_combobox()
        self.save_file_mQgsFileWidget.setStorageMode(QgsFileWidget().GetDirectory)
        self.save_file_mQgsFileWidget.setFilePath(self.flight_missions_save_path)
        self.update_warning_block()

        self.takeoff_point_layer_ComboBox.layerChanged.connect(self.update_takeoff_feats_combobox)
        self.profiles_mMapLayerComboBox.layerChanged.connect(self.update_profiles_combobox)
        self.DEM_mMapLayerComboBox.layerChanged.connect(self.update_dem_combobox)
        self.pushButton_get_to_point.clicked.connect(self.get_takeoff_point_from_layer)

        locale = QLocale(QLocale.English)
        validator = QDoubleValidator().setLocale(locale)
        self.lineEdit_lon.setValidator(validator)
        self.lineEdit_lat.setValidator(validator)
        self.lineEdit_alt.setValidator(validator)


    def update_takeoff_feats_combobox(self):
        self.takeoff_point_ComboBox.setLayer(self.takeoff_point_layer_ComboBox.currentLayer())
        self.update_warning_block()

    def update_profiles_combobox(self):
        self.update_warning_block()

    def update_dem_combobox(self):
        self.update_warning_block()

    def update_warning_block(self):
        takeoff_points_crs = self.takeoff_point_layer_ComboBox.currentLayer().crs().authid()
        profiles_crs = self.profiles_mMapLayerComboBox.currentLayer().crs().authid()
        DEM_crs = self.DEM_mMapLayerComboBox.currentLayer().crs().authid()
        if (takeoff_points_crs == None) or (profiles_crs == None) or (DEM_crs == None):
            return
        if not (takeoff_points_crs == profiles_crs == DEM_crs):
            self.warning_icon_label.setPixmap(QPixmap(":/plugins/RousettusTool/resources/warning.png"))
            self.warning_icon_label.setToolTip('DEM, points and profiles CRS aren`t the same')
            self.warning_text_label.setText('DEM, points and Profiles CRS are different')
        else:
            self.warning_icon_label.setPixmap(QPixmap())
            self.warning_text_label.setText('')
            self.warning_icon_label.setToolTip('')

    def get_takeoff_point_from_layer(self):
        source_crs = self.takeoff_point_layer_ComboBox.currentLayer().crs()
        dest_crs = QgsCoordinateReferenceSystem("EPSG:4326")
        transformer = QgsCoordinateTransform(source_crs, dest_crs, QgsProject.instance())
        takeoff_point = self.takeoff_point_ComboBox.feature().geometry()
        takeoff_point.transform(transformer)
        if self.debug:
            print('from FlightPlanningHandle.get_takeoff_point_from_layer   transformed takeoff: {}'.format(takeoff_point))
        self.lineEdit_lon.setText(str(takeoff_point.asPoint().x()))
        self.lineEdit_lat.setText(str(takeoff_point.asPoint().y()))

    def handle_generate_flights_button(self):
        pass
    
    def generate_flight_features(self):
        pass



