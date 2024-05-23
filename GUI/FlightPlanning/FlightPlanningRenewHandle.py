from PyQt5.QtCore import QItemSelectionModel, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QDialog

from qgis.core import QgsLayerTreeGroup, QgsProject, Qgis

from GUI.FlightPlanning.PreviewFlightWindowHandle import PreviewFlightWindowHandle
from UI.FlightPlanning.FlightPlan_renew_ui import Ui_FlightPlan_renew_form
from tools.Configurable import Configurable
from tools.ServiceClasses.RousettusLoggerHandler import RousettusLoggerHandler
from GUI.FlightPlanning.LayerListModel import LayerListModel
from GUI.FlightPlanning.RouteFeaturesTableModel import RouteFeaturesTableModel
from GUI.FlightPlanning.FlightPlansTableModel import FlightPlansTableModel
from GUI.FlightPlanning.DemLayersModel import DemLayersModel

from tools import constants
from tools.VectorLayerSaverGPKG.FlightLayerSaverGPKG import FlightLayerSaverGPKG


class FlightPlanningHandle(Ui_FlightPlan_renew_form, QDialog, Configurable):
    flight_layer_saver: FlightLayerSaverGPKG

    def __init__(self, main_window=None):
        super().__init__()
        self.flight_layer_saver = None
        self.main_window = main_window
        self.preview_window = None
        self.raster_layers_model = None
        self.flight_table_model: FlightPlansTableModel or None = None
        self.route_feature_table_model = None
        self.route_layers_model = None
        self.main_window = main_window
        self.section_name = 'flight_plan'
        self.logger = RousettusLoggerHandler.get_handler().logger
        self.setupUi(self)
        self.init_signals()
        self.init_gui()

    def init_gui(self):
        self.route_layers_model = LayerListModel(Qgis.GeometryType.Line)
        self.init_route_layer_list_model()
        self.route_layer_combobox.setModel(self.route_layers_model)
        self.route_feature_table_model = RouteFeaturesTableModel()
        self.routes_table_view.setModel(self.route_feature_table_model)
        self.routes_table_view.setSelectionBehavior(QTableView.SelectRows)
        self.init_route_feature_table_model()
        self.flights_tableView.setSelectionBehavior(QTableView.SelectRows)
        self.raster_layers_model = DemLayersModel()
        self.dem_layer_combobox.setModel(self.raster_layers_model)
        self.init_dem_crs_warning()
        self.init_flights_table_model()

    def init_signals(self):
        self.routes_only_checkBox.stateChanged.connect(self.init_gui)
        self.method_name_layer.currentIndexChanged.connect(self.init_route_layer_list_model)
        self.route_layer_combobox.currentIndexChanged.connect(self.init_route_feature_table_model)
        self.select_all_button.clicked.connect(self.select_all_button_handler)
        self.add_button.clicked.connect(self.add_button_handler)
        self.rem_button.clicked.connect(self.remove_button_handler)
        self.dem_layer_combobox.currentIndexChanged.connect(self.init_dem_crs_warning)
        self.dem_layer_combobox.currentIndexChanged.connect(
            lambda: self.flight_table_model.set_dem_layer(self.dem_layer_combobox.currentData()))
        self.f_alt_dspbox.valueChanged.connect(
            lambda: self.flight_table_model.set_desired_alt(self.f_alt_dspbox.value()))
        self.to_point_alt_dspbox.valueChanged.connect(
            lambda: self.flight_table_model.set_takeoff_point_alt(self.to_point_alt_dspbox.value()))
        self.down_dev_dspbox.valueChanged.connect(
            lambda: self.flight_table_model.set_down_deviation_alt(self.down_dev_dspbox.value()))
        self.up_dev_dspbox.valueChanged.connect(
            lambda: self.flight_table_model.set_up_deviation_alt(self.up_dev_dspbox.value()))
        self.previw_btn.clicked.connect(self.preview_button_handler)
        self.save_flight_button.clicked.connect(self.save_button_handler)
        self.wp_export_btn.clicked.connect(self.export_waypoints_btn_handler)
        self.to_point_alt_dspbox.valueChanged.connect(
            lambda: self.flight_table_model.set_takeoff_point_alt(self.to_point_alt_dspbox.value())
        )

    def init_dem_crs_warning(self):
        layer = self.dem_layer_combobox.currentData()
        if layer:
            if not (r'units=m' in layer.crs().toProj()):
                self.dem_crs_warn_label.setPixmap(QPixmap(":/plugins/RousettusTool/resources/warning.png"))
                self.dem_crs_warn_label.setToolTip('Layer has non metric CRS')
                return
            else:
                self.dem_crs_warn_label.setPixmap(QPixmap())
                self.dem_crs_warn_label.setToolTip('')
            if layer.crs().authid() != self.dem_layer_combobox.currentData().crs().authid():
                self.dem_crs_warn_label.setPixmap(QPixmap(":/plugins/RousettusTool/resources/warning.png"))
                self.dem_crs_warn_label.setToolTip('route and dem layers CRS aren`t the same')
                return
            else:
                self.dem_crs_warn_label.setPixmap(QPixmap())
                self.dem_crs_warn_label.setToolTip('')

    def init_route_layer_list_model(self):
        self.route_layers_model.set_layer_group(self.get_route_layer_group())

    def init_route_feature_table_model(self):
        if self.route_feature_table_model:
            self.route_feature_table_model.set_layer(self.route_layer_combobox.currentData())
            self.init_flights_table_model()

    def init_flights_table_model(self):
        if self.route_feature_table_model:
            self.flight_table_model = FlightPlansTableModel(self.route_feature_table_model.get_layer(),
                                                            self.method_name_layer.currentText(),
                                                            self.main_window,
                                                            )
            self.flights_tableView.setModel(self.flight_table_model)
            self.flight_table_model.set_dem_layer(self.dem_layer_combobox.currentData())
            self.flight_table_model.set_desired_alt(self.f_alt_dspbox.value())
            self.flight_table_model.set_takeoff_point_alt(self.to_point_alt_dspbox.value())
            self.flight_table_model.set_down_deviation_alt(self.down_dev_dspbox.value())
            self.flight_table_model.set_up_deviation_alt(self.up_dev_dspbox.value())
            self.flight_layer_saver = FlightLayerSaverGPKG(self.method_name_layer.currentText(),
                                                           self.flight_table_model.get_layer(),
                                                           self.main_window)

    def route_table_selection_handler(self):
        pass

    def add_button_handler(self):
        self.flight_table_model.add_data(
            [self.route_feature_table_model.data(row_index, Qt.UserRole) for row_index in
             [index for index in self.routes_table_view.selectedIndexes() if index.column() == 0]]
        )

    def remove_button_handler(self):
        self.flight_table_model.remove_data([index.row() for index in
                                             self.flights_tableView.selectedIndexes() if index.column() == 0])

    def save_button_handler(self):
        """
        обработчик для кнопки сохранения изменений на слой.
        handler for the button to save changes to the layer.
        """
        self.save_flight_button.setEnabled(False)
        self.flight_layer_saver.save_layer(self.flight_table_model.get_layer())
        self.flight_layer_saver.set_style_to_routes_layer()
        self.save_flight_button.setEnabled(True)
        QgsProject.instance().reloadAllLayers()

    def select_all_button_handler(self):
        self.logger.debug(self.routes_table_view.selectionMode())
        self.routes_table_view.selectAll()

    def preview_button_handler(self):
        self.preview_window = PreviewFlightWindowHandle(self.flight_table_model)
        self.preview_window.show()

    def get_route_layer_group(self) -> QgsLayerTreeGroup or None:
        root = QgsProject.instance().layerTreeRoot()
        if self.routes_only_checkBox.isChecked():
            group_path_list = constants.get_routes_group_path(self.method_name_layer.currentText())
            find_node = None
            for gr_name in group_path_list:
                find_node = root.findGroup(gr_name)
                if find_node is None:
                    return find_node
            return find_node
        else:
            return QgsProject.instance().layerTreeRoot()

    def export_waypoints_btn_handler(self):
        self.save_button_handler()
        # TODO убрать LayerSaver в модель данных.
        self.flight_table_model.export_waypoints_files(self.flight_layer_saver.get_layer())
        QgsProject.instance().write()

    def closeEvent(self, event):
        self.preview_window = None
