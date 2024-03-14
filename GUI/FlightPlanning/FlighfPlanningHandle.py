import time

from qgis.core import QgsMapLayerProxyModel, QgsCoordinateReferenceSystem, QgsCoordinateTransform, \
    QgsProject
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
import matplotlib as mpl
from matplotlib import pyplot as plt


from tools.get_current_project_name import get_current_project_name
from ...UI.FlightPlanning.FlightPlan_ui import Ui_FlightPlan_form
from ...tools.Configurable import Configurable
from ...tools.FlightPlanningLib.FlightPlanner import FlightPlanner




# TODO сдедать проверку, что маршрут полностью закрыт демкой
class FlightPlanningHandle(Ui_FlightPlan_form, QDialog, Configurable):
    init_flight_btn_pushed_debug = 1
    def __init__(self, main_window=None):
        super().__init__()
        self.takeoff_point_altitude = None
        self.main_window = main_window
        self.flight_planner = None
        self.setupUi(self)
        self.initGui()
        self.section_name = 'flight_plan'

    def initGui(self):

        # set geometry filters on qgs comboboxes
        self.profiles_mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.LineLayer)
        self.DEM_mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.update_route_features_combobox()

        # connect signals
        self.pushButton_generate_flight.clicked.connect(self.generate_flight_btn_pushed)
        self.profiles_mMapLayerComboBox.layerChanged.connect(self.update_route_features_combobox)
        self.show_graph_btn.clicked.connect(self.show_flight_graph)
        self.pushButton_export.clicked.connect(self.export_flight_plan)

    def generate_flight_btn_pushed(self):
        # Init FlightRoute
        if self.init_flight_btn_pushed_debug:
            print("\n===begin init_flight_btn_pushed===")
            print('flight planner call arguments: ')
            print('flight alt: ', self.flight_alt_spinBox.value(),
                  ", type: ", type(self.flight_alt_spinBox.value()))
            print('up deviation: ', self.up_deviation_spinbox.value(),
                  ", type: ", type(self.up_deviation_spinbox.value()))
            print('down deviation: ', self.down_deviation_spinbox.value(),
                  ", type: ", type(self.down_deviation_spinbox.value()))
            start_time = time.time()
        self.takeoff_point_altitude = self.takeoff_point_alt_spinBox.value()
        self.flight_planner = FlightPlanner(self.mFeatureListComboBox.feature(),
                                            self.profiles_mMapLayerComboBox.currentLayer().crs(),
                                            self.DEM_mMapLayerComboBox.currentLayer(),
                                            1,
                                            self.flight_alt_spinBox.value(),
                                            self.up_deviation_spinbox.value(),
                                            self.down_deviation_spinbox.value(),
                                            self.takeoff_point_altitude)
        self.flight_planner.general_algorithm()
        if self.init_flight_btn_pushed_debug:
            print('make_flight_plan execution time: ', time.time() - start_time)
            print("\n===end init_flight_btn_pushed===")

    def show_flight_graph(self):

        dist_alt_table = self.flight_planner.get_altitude_points_list()
        print('flight_metrics: ', self.flight_planner.get_flight_metrics())
        flight_plan = self.flight_planner.get_flight_points()
        fig, ax = plt.subplots()
        ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(500))
        ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(50))
        ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(25))
        ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
        ax.grid(color='g', linestyle=':', linewidth=0.5)
        ax.set_xlabel('Distance, m')
        ax.set_ylabel('Altitude, m')
        ax.plot([point[0] for point in dist_alt_table], [point[1] for point in dist_alt_table])
        ax.scatter([p[2] for p in self.flight_planner.get_turning_points()],
                   [self.flight_planner.get_altitude(p[2]) for p in self.flight_planner.get_turning_points()],
                   color='r')
        ax.plot([point['distance'] for point in flight_plan],
                [point['flight_alt'] + point['gnd_alt'] for point in flight_plan])
        ax.scatter([point['distance'] for point in flight_plan],
                   [point['flight_alt'] + point['gnd_alt'] for point in flight_plan], color='g')
        plt.fill_between([point[0] for point in dist_alt_table],
                         [point[1] + self.up_deviation_spinbox.value() +
                          self.flight_alt_spinBox.value() for point in dist_alt_table],
                         [point[1] + self.down_deviation_spinbox.value() +
                          self.flight_alt_spinBox.value() for point in dist_alt_table],
                         color='r', alpha=0.1)
        plt.show()

    def export_flight_plan(self):
        curr_path = get_current_project_name()
        export_filename = QFileDialog.getSaveFileName(self, 'Export waypoints',
                                                      curr_path[1], "waypoints (*.waypoints)")[0]
        flight_plan_crs = self.profiles_mMapLayerComboBox.currentLayer().crs()
        dest_crs = QgsCoordinateReferenceSystem(4326)
        tr = QgsCoordinateTransform(flight_plan_crs, dest_crs, QgsProject.instance())
        file = open(export_filename, 'w')
        file.write("QGC WPL 110\n")
        flight_points = self.flight_planner.get_flight()
        first_point_flag = 1
        for i in range(len(flight_points)):
            flight_point = tr.transform(flight_points[i].geometry().asPoint())
            alt = flight_points[i].attribute('alt')
            if first_point_flag:
                file.write("0\t1\t0\t16\t0.0\t0.0\t0.0\t0.0\t{}\t{}\t0.0\t1\n".format(str(flight_point.y()),
                                                                                      str(flight_point.x())))
                first_point_flag = 0
            waypoint_string = '\t'.join([str(i), str(0), str(3), str(16), str(0.0), str(0.0), str(0.0), str(0.0),
                                         str(flight_point.y()), str(flight_point.x()), str(alt), str(1)])
            file.write(waypoint_string + '\n')
        file.write('\t'.join([str(len(flight_points)), str(0), str(3), str(20), str(0.0), str(0.0),
                              str(0.0), str(0.0), str(0.0), str(0.0), str(0.0), str(1)]))
        file.close()


    def update_route_features_combobox(self):
        self.mFeatureListComboBox.setLayer(self.profiles_mMapLayerComboBox.currentLayer())

    def load_config(self):
        if self.config is not None:
            if self.section_name in self.config:
                if 'route_layer' in self.config[self.section_name]:
                    route_layer_name = self.config[self.section_name].get('route_layer')
                    item_index = self.profiles_mMapLayerComboBox.findText(route_layer_name, flags=Qt.MatchFixedString)
                    if item_index >= 0:
                        self.profiles_mMapLayerComboBox.setCurrentIndex(item_index)
                if 'takeoff_point_alt' in self.config[self.section_name]:
                    self.takeoff_point_alt_spinBox.setValue(self.config[self.section_name].getint('takeoff_point_alt'))

    def store_config(self):
        if self.config is not None:
            if self.section_name not in self.config:
                self.config[self.section_name] = {}
            self.config[self.section_name]['route_layer'] = \
                str(self.profiles_mMapLayerComboBox.currentLayer().name())
            self.config[self.section_name]['DEM_layer'] = str(self.DEM_mMapLayerComboBox.currentLayer().name())
            self.config[self.section_name]['planning_function_id'] = str(self.comboBox_function.currentIndex())
            self.config[self.section_name]['flight_alt'] = str(self.flight_alt_spinBox.value())
            self.config[self.section_name]['takeoff_point_alt'] = str(self.takeoff_point_alt_spinBox.value())
            self.config[self.section_name]['up_deviation'] = str(self.up_deviation_spinbox.value())
            self.config[self.section_name]['down_deviation'] = str(self.down_deviation_spinbox.value())
            self.config[self.section_name]['Regular_points_dist'] = str(self.spinBox.value())
