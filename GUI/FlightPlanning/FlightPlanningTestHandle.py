from ...UI.FlightPlanning.FlightPlan_test_ui import Ui_FlightPlan_test_form
from qgis.PyQt.QtWidgets import QDialog

from qgis.core import QgsMapLayerProxyModel

from ...tools.Configurable import Configurable
from ...tools.FlightPlanningLib.FlightRoute import FlightRoute

import matplotlib as mpl
from matplotlib import pyplot as plt


# TODO сдедать проверку, что маршрут полностью закрыт демкой
class FlightPlanningTestHandle(Ui_FlightPlan_test_form, QDialog, Configurable):
    def __init__(self, main_window=None):
        super().__init__()
        self.flight_route = None
        self.setupUi(self)
        self.initGui()
        self.section_name = 'test_flight_plan'


    def initGui(self):
        # set geometry filters on qgs comboboxes
        self.profiles_mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.LineLayer)
        self.DEM_mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.update_route_features_combobox()


        # connect signals
        self.pushButton_generate_flight.clicked.connect(self.generate_flight_btn_pushed)
        self.profiles_mMapLayerComboBox.layerChanged.connect(self.update_route_features_combobox)

    def generate_flight_btn_pushed(self):
        print('test flight plan btn pushed')
        flight_poins_list = [(point.x(), point.y())
                             for point in self.mFeatureListComboBox.feature().geometry().asMultiPolyline()[0]]
        self.flight_route = FlightRoute(flight_poins_list,
                                   self.profiles_mMapLayerComboBox.currentLayer().crs().authid())
        self.flight_route.make_dist_to_x_func()
        self.flight_route.make_dist_to_y_func()
        errors_count = self.flight_route.qgs_set_altitude_points(self.DEM_mMapLayerComboBox.currentLayer(), 1)
        if 1:
            print('points are out of DEM: ', errors_count)
        dist_alt_table = self.flight_route.get_altitude_points_list()
        self.flight_route.make_dist_to_alt_finction()
        fig, ax = plt.subplots()
        ax.plot([point[0] for point in dist_alt_table], [point[1] for point in dist_alt_table])
        ax.scatter([p[2] for p in self.flight_route.get_turning_points()],
                   [self.flight_route.get_altitude(p[2]) for p in self.flight_route.get_turning_points()],
                   color='r')
        plt.show()

    def update_route_features_combobox(self):
        self.mFeatureListComboBox.setLayer(self.profiles_mMapLayerComboBox.currentLayer())



