from ...UI.FlightPlanning.FlightPlan_test_ui import Ui_FlightPlan_test_form
from qgis.PyQt.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog

from qgis.core import QgsMapLayerProxyModel, QgsCoordinateReferenceSystem, QgsCoordinateTransform, \
    QgsProject, QgsPointXY, QgsGeometry
from ...tools.ServiceClasses.get_current_project_name import get_current_project_name

from ...tools.Configurable import Configurable
from ...tools.FlightPlanningLib.FlightPlan import FlightPlan

import matplotlib as mpl
from matplotlib import pyplot as plt

import time


# TODO сдедать проверку, что маршрут полностью закрыт демкой
class FlightPlanningTestHandle(Ui_FlightPlan_test_form, QDialog, Configurable):
    def __init__(self, main_window=None):
        super().__init__()
        self.takeoff_point_altitude = None
        self.main_window = main_window
        self.flight_plan = None
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
        self.show_graph_btn.clicked.connect(self.show_flight_graph)
        self.pushButton_export.clicked.connect(self.export_flight_plan)

    def generate_flight_btn_pushed(self):
        # print('test flight plan btn pushed')
        # Init FlightRoute
        flight_poins_list = [(point.x(), point.y())
                             for point in self.mFeatureListComboBox.feature().geometry().asMultiPolyline()[0]]
        self.flight_plan = FlightPlan(flight_poins_list,
                                      self.profiles_mMapLayerComboBox.currentLayer().crs().authid())
        self.flight_plan.make_dist_to_x_func()
        self.flight_plan.make_dist_to_y_func()
        errors_count = self.flight_plan.qgs_set_altitude_points(self.DEM_mMapLayerComboBox.currentLayer(), 1)
        # if 1:
        #     print('points are out of DEM: ', errors_count)

        self.flight_plan.make_dist_to_alt_finction()
        # init FlightPlan
        is_service_vector = [int(flag) for flag in self.mFeatureListComboBox.feature().attribute('service').split(';')]
        self.flight_plan.set_service_flight_flags(is_service_vector)
        self.flight_plan.set_alt_deviation(self.up_deviation_spinbox.value(), self.down_deviation_spinbox.value())
        self.flight_plan.set_flight_altitude(self.flight_alt_spinBox.value())
        self.flight_plan.make_initial_flight_plan()
        # print('init flight points: ', ((i, point['distance'], point['gnd_alt']) for i, point in enumerate(self.flight_plan.get_flight_points())))
        # print('init flight points len: ', len(self.flight_plan.get_flight_points()))
        start_time = time.time()
        self.flight_plan.make_flight_plan()
        print('make_flight_plan execution time: ', time.time()-start_time)
        # print('flight points: ', self.flight_plan.get_flight_points())
        # print('flight points len: ', len(self.flight_plan.get_flight_points()))

    def show_flight_graph(self):
        dist_alt_table = self.flight_plan.get_altitude_points_list()
        flight_plan = self.flight_plan.get_flight_points()
        fig, ax = plt.subplots()
        ax.plot([point[0] for point in dist_alt_table], [point[1] for point in dist_alt_table])
        ax.scatter([p[2] for p in self.flight_plan.get_turning_points()],
                   [self.flight_plan.get_altitude(p[2]) for p in self.flight_plan.get_turning_points()],
                   color='r')
        ax.plot([point['distance'] for point in flight_plan],
                [point['flight_alt']+point['gnd_alt'] for point in flight_plan])
        ax.scatter([point['distance'] for point in flight_plan],
                   [point['flight_alt']+point['gnd_alt'] for point in flight_plan], color='g')
        # print('flight altitudes: ')
        # print(str([point['flight_alt'] for point in dist_alt_table]))
        # print("ground altitudes: ")
        # print([point['flight_alt'] for point in dist_alt_table)
        plt.fill_between([point[0] for point in dist_alt_table],
                         [point[1]+self.up_deviation_spinbox.value()+
                          self.flight_alt_spinBox.value() for point in dist_alt_table],
                         [point[1]+self.down_deviation_spinbox.value()+
                          self.flight_alt_spinBox.value() for point in dist_alt_table],
                         color='r', alpha=0.1)
        plt.show()

    def export_flight_plan(self):
        curr_path = get_current_project_name()
        export_filename = QFileDialog.getSaveFileName(self, 'Export waypoints',
                                                      curr_path[1], "waypoints (*.waypoints)")[0]
        flight_plan_crs = QgsCoordinateReferenceSystem(self.flight_plan.get_crs_str())
        dest_crs = QgsCoordinateReferenceSystem(4326)
        tr = QgsCoordinateTransform(flight_plan_crs, dest_crs, QgsProject.instance())
        if self.takeoff_point_altitude is None:
            self.takeoff_point_altitude = self.flight_plan.get_flight_points()[0]['gnd_alt']
        file = open(export_filename, 'w')
        file.write("QGC WPL 110\n")


        flight_points = self.flight_plan.get_flight_points()
        first_point_flag = 1
        for i in range(len(flight_points)):
            x, y = self.flight_plan.get_coord_from_dist(flight_points[i]['distance'])
            flight_point = tr.transform(QgsPointXY(x, y))
            alt = flight_points[i]['gnd_alt'] -  self.takeoff_point_altitude + flight_points[i]['flight_alt']
            if first_point_flag:
                file.write("0\t1\t0\t16\t0.0\t0.0\t0.0\t0.0\t{}\t{}\t0.0\t1\n".format(str(flight_point.y()),
                                                                                      str(flight_point.x())))
                first_point_flag = 0
            waypoint_string = '\t'.join([str(i), str(0), str(3), str(16), str(0.0), str(0.0), str(0.0), str(0.0),
                                         str(flight_point.y()), str(flight_point.x()), str(alt), str(1)])
            # print(waypoint_string)
            file.write(waypoint_string + '\n')
        file.write('\t'.join([str(len(flight_points)), str(0), str(3), str(20), str(0.0), str(0.0),
                              str(0.0), str(0.0), str(0.0), str(0.0), str(0.0), str(1)]))
        file.close()



    # def add_flight_point(self):
    #     for i, flight_point in self.flight_plan.get_flight_points():
    #         pass


    def update_route_features_combobox(self):
        self.mFeatureListComboBox.setLayer(self.profiles_mMapLayerComboBox.currentLayer())



