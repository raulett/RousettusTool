import logging
from typing import List

from PyQt5.QtCore import QThread, pyqtSignal, QMutex
from qgis.core import QgsFeature, QgsCoordinateReferenceSystem, QgsRasterLayer

from tools.FlightPlanningLib.FlightPlanner import FlightPlanner
from tools.ServiceClasses.RousettusLoggerHandler import RousettusLoggerHandler


class FlightPlannerWorker(QThread):
    finished_all = pyqtSignal(int)
    planned_flight = pyqtSignal()

    def __init__(self, queue: List[QgsFeature], result_queue: List[FlightPlanner],
                 worker_num: int,
                 mutex: QMutex, result_mutex: QMutex,
                 layer_crs: QgsCoordinateReferenceSystem,
                 dem_layer: QgsRasterLayer,
                 desired_alt: float, takeoff_point_altitude: float,
                 up_deviation: float, down_deviation: float):
        super().__init__()
        self.queue = queue
        self.result_queue = result_queue
        self.worker_num = worker_num
        self.mutex = mutex
        self.result_mutex = result_mutex
        self.layer_crs = layer_crs
        self.dem_layer = dem_layer
        self.desired_alt = desired_alt
        self.takeoff_point_altitude = takeoff_point_altitude
        self.up_deviation = up_deviation
        self.down_deviation = down_deviation
        self.logger = RousettusLoggerHandler.get_handler().logger
        self.logger.debug(f'New worker {self.worker_num} created')


    def run(self):
        while len(self.queue) > 0:
            self.mutex.lock()
            if len(self.queue) > 0:
                self.logger.debug(f'Worker {self.worker_num} got route from queue under mutex')
                route_feature = self.queue.pop(0)
                self.mutex.unlock()
                self.logger.debug(f'Worker {self.worker_num} unlocked queue mutex')
            else:
                self.mutex.unlock()
                break
            flight_planner = None
            try:
                flight_planner = FlightPlanner(route_feature, self.layer_crs,
                                               self.dem_layer, 1,
                                               self.desired_alt, self.up_deviation,
                                               self.down_deviation, self.takeoff_point_altitude)
            except Exception as e:
                self.logger.warning(f'Worker {self.worker_num} have exception in FlightPlanner init: '
                                    f'{e.with_traceback()}')
                # raise e
            self.logger.debug(f'Worker {self.worker_num} created FLIGHT PLANNER instance')
            try:
                flight_planner.general_algorithm()
            except Exception as e:
                self.logger.warning(f'Worker {self.worker_num} have exception in FlightPlanner.general_algorithm')
                flight_planner = None
                # raise e
            self.logger.debug(f'Worker {self.worker_num} processed general algorithm')
            self.result_mutex.lock()
            self.result_queue.append(flight_planner)
            self.result_mutex.unlock()
            self.planned_flight.emit()
        self.finished_all.emit(self.worker_num)
