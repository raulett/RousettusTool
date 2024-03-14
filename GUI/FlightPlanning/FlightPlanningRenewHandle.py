from PyQt5.QtCore import QItemSelectionModel, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QDialog
from qgis.core import QgsLayerTreeGroup, QgsProject, Qgis

from tools import constants
from UI.FlightPlanning.FlightPlan_renew_ui import Ui_FlightPlan_renew_form
from tools.Configurable import Configurable
from tools.VectorLayerSaverGPKG.FlightLayerSaverGPKG import FlightLayerSaverGPKG
from GUI.FlightPlanning.LayerListModel import LayerListModel
from GUI.FlightPlanning.RouteFeaturesTableModel import RouteFeaturesTableModel
from GUI.FlightPlanning.FlightPlansTableModel import FlightPlansTableModel
from GUI.FlightPlanning.DemLayersModel import DemLayersModel




class FlightPlanningHandle(Ui_FlightPlan_renew_form, QDialog, Configurable):
    def __init__(self, main_window=None):
        super().__init__()
        self.raster_layers_model = None
        self.flight_table_model = None
        self.route_feature_table_model = None
        self.route_layers_model = None
        self.main_window = main_window
        self.section_name = 'flight_plan'
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
        self.init_flights_table_model()
        self.init_dem_crs_warning()
        self.flight_table_model.set_dem_layer(self.dem_layer_combobox.currentData())
        self.flight_table_model.set_desired_alt(self.f_alt_dspbox.value())
        self.flight_table_model.set_takeoff_point_alt(self.to_point_alt_dspbox.value())
        self.flight_table_model.set_down_deviation_alt(self.down_dev_dspbox.value())
        self.flight_table_model.set_up_deviation_alt(self.up_dev_dspbox.value())

    def init_signals(self):
        self.routes_only_checkBox.stateChanged.connect(self.init_gui)
        self.method_name_layer.currentIndexChanged.connect(self.init_route_layer_list_model)
        self.route_layer_combobox.currentIndexChanged.connect(self.init_route_feature_table_model)
        self.select_all_button.clicked.connect(self.select_all_button_handler)
        self.add_button.clicked.connect(self.add_button_handler)
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
            self.flight_table_model = FlightPlansTableModel(self.route_feature_table_model.get_layer())
            self.flights_tableView.setModel(self.flight_table_model)
            self.flight_table_model.set_dem_layer(self.dem_layer_combobox.currentData())

    def route_table_selection_handler(self):
        pass

    def add_button_handler(self):
        self.flight_table_model.add_data(
            [self.route_feature_table_model.data(row_index, Qt.UserRole) for row_index in
             [index for index in self.routes_table_view.selectedIndexes() if index.column() == 0]]
        )

    def remove_button_handler(self):
        pass

    def save_button_handler(self):
        pass

    def select_all_button_handler(self):
        self.routes_table_view.setSelectionMode(QTableView.MultiSelection)
        for i in range(self.route_feature_table_model.rowCount()):
            self.routes_table_view.selectRow(i)
        self.routes_table_view.setSelectionMode(QTableView.SingleSelection)

    def unplan_button_handler(self):
        pass

    def get_route_layer_group(self) -> QgsLayerTreeGroup or None:
        root = QgsProject.instance().layerTreeRoot()
        if self.routes_only_checkBox.isChecked():
            group_path_list = constants.get_routes_group_path(self.method_name_layer.currentText())
            find_node = None
            for gr_name in group_path_list:
                find_node = root.findGroup(gr_name)
                # print(f'gr_name: {gr_name}, find_node: {find_node}')
                if find_node is None:
                    return find_node
            return find_node
        else:
            return QgsProject.instance().layerTreeRoot()
