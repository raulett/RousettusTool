import multiprocessing
from typing import Any, List
import re

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant, QMutex
from PyQt5.QtGui import QIcon
from qgis.core import QgsFeature, QgsField, QgsVectorLayer, QgsFields, QgsGeometry, QgsRasterLayer, QgsPoint

from .FlightPlannerWorker import FlightPlannerWorker
from .FlightPlanFeatureFabric import FlightPlanFeatureFabric
from ...tools.FlightPlanningLib.FlightPlanner import FlightPlanner


class FlightPlansTableModel(QAbstractTableModel):

    def __init__(self, layer: QgsVectorLayer):
        super().__init__()
        self._thread_count = 0
        self._down_deviation = None
        self._up_deviation = None
        self._takeoff_point_altitude = None
        self._desired_alt = None
        self._dem_layer = None
        self._dem_band = None
        self._planning_mutex = None
        if layer is not None:
            self.flights_layer_name = layer.name().replace('routes', 'flights')
            self.to_point = re.search(r'^routes_iteration-\d*_(.*)$', layer.name()).group(0)
            self._temp_flight_layer = QgsVectorLayer("PointZ", self.flights_layer_name, "memory")
            self._temp_flight_layer.setCrs(layer.crs())
            self.crs = layer.crs()
        else:
            self.flights_layer_name = None
            self.to_point = None
            self._temp_flight_layer = None
            self.crs = None
        self._temp_flight_layer.startEditing()
        self._temp_flight_layer.dataProvider().addAttributes(FlightPlanFeatureFabric.get_fields())
        self._temp_flight_layer.updateExtents()
        self._temp_flight_layer.commitChanges()
        self._planning_queue = []
        self._result_queue = []
        self._data = []
        self._workers = {}
        self._planning_mutex = QMutex()
        self._result_mutex = QMutex()
        self._worker_management_mutex = QMutex()
        self._layer_add_mutex = QMutex()
        self._headers = ['Process', 'Name', 'p_num']
        self._thread_num = multiprocessing.cpu_count() - 2 if multiprocessing.cpu_count() > 2 else 1

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        column_name = self._headers[index.column()]
        if role == Qt.DisplayRole:
            if column_name == 'Name':
                return self._data[index.row()].get('route_feature').attribute('name')
            elif column_name == 'Process':
                return self._data[index.row()].get('flight_planned')
            elif column_name == 'p_num':
                return self._data[index.row()].get('point_num')
            else:
                return None
        if role == Qt.DecorationRole:
            if column_name == 'Process':
                if self._data[index.row()].get('flight_planned'):
                    return QIcon(":/plugins/RousettusTool/resources/yes36.png")
                else:
                    return QIcon(":/plugins/RousettusTool/resources/time36.png")
        if role == Qt.UserRole:
            return self._data[index.row()]
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            else:
                return section

    def add_data(self, route_feature_list: List[QgsFeature]):
        self.beginResetModel()
        if self._temp_flight_layer is not None:
            for route_feature in route_feature_list:
                if (route_feature.attribute('name') not in
                        [feat.get('route_feature').attribute('name') for feat in self._data]):
                    self._data.append({'layer_name': self._temp_flight_layer.name(),
                                       'route_feature': route_feature,
                                       'flight_planned': False})
        self.endResetModel()
        self.start_workers()

    def start_workers(self):
        self._planning_mutex.lock()
        for route_feature in self._data:
            if (not route_feature.get('flight_planned') and route_feature.get('route_feature')
                    and route_feature.get('route_feature').attribute('name') not in
                    [feat.attribute('name') for feat in self._planning_queue]):
                self._planning_queue.append(route_feature.get('route_feature'))
        self._planning_mutex.unlock()
        self._thread_count = min(len(self._planning_queue), self._thread_num)
        print('Thread count: ', self._thread_count)
        while self._thread_count > 0:
            print('Thread count in while: ', self._thread_count)
            print('management_ mutex lock')
            self._worker_management_mutex.lock()
            self._thread_count -= 1
            self._worker_management_mutex.unlock()
            print('management_ mutex unlock')
            self._workers[self._thread_num] = FlightPlannerWorker(self._planning_queue,
                                                                  self._result_queue,
                                                                  self._thread_num,
                                                                  self._planning_mutex,
                                                                  self._result_mutex,
                                                                  self.crs,
                                                                  self._dem_layer,
                                                                  self._desired_alt,
                                                                  self._takeoff_point_altitude,
                                                                  self._up_deviation,
                                                                  self._down_deviation)
            self._workers.get(self._thread_num).finished_all.connect(self.worker_finished)
            self._workers.get(self._thread_num).planned_flight.connect(self.worker_planned_flight)
        self._worker_management_mutex.lock()
        for worker in self._workers.values():
            worker.start()
        self._worker_management_mutex.unlock()

    def get_to_pointname(self) -> str:
        return self.to_point

    def worker_finished(self, worker_num: int):
        '''
        Method that is called by worker finished custom event a FlightPlannerWorker finishes.
        :param worker_num:
        :return:
        '''
        self._worker_management_mutex.lock()
        if len(self._workers) > 0:
            worker = self._workers.pop(worker_num)
            worker.exit()
        self._thread_count += 1
        self._worker_management_mutex.unlock()

    def worker_planned_flight(self):
        flight_plan = None
        self._result_mutex.lock()
        if len(self._result_queue) > 0:
            flight_plan = self._result_queue.pop(0)
        self._result_mutex.unlock()
        flight_features = flight_plan.get_flight()
        index = [feat.get('route_feature').attribute('name')
                 for feat in self._data].index(flight_plan.get_route_feature().attribute('name'))
        route_feature = flight_plan.get_route_feature()
        self.beginResetModel()
        self._data[index]['flight_planned'] = True
        self._data[index]['point_num'] = len(flight_features)
        self.endResetModel()
        self._data[index]['flight_points'] = flight_features
        self._data[index]['flight_metrics'] = flight_plan.get_flight_metrics()

        self._temp_flight_layer.startEditing()
        for flight_feat in flight_features:
            flight_feature = (
                FlightPlanFeatureFabric.
                get_flight_plan_feature(point_num=flight_feat.attribute('point_num'),
                                        name=route_feature.attribute('name'),
                                        lon=flight_feat.geometry().asPoint().x(),
                                        lat=flight_feat.geometry().asPoint().y(),
                                        alt=flight_feat.attribute('alt'),
                                        alt_asl=flight_feat.attribute('alt_asl'),
                                        distance=flight_feat.attribute('distance'),
                                        to_point=self.to_point,
                                        is_service=flight_feat.attribute('is_service')))
            flight_feature.setGeometry(flight_feat.geometry())
            self._temp_flight_layer.addFeature(flight_feature)
        self._temp_flight_layer.updateExtents()
        self._temp_flight_layer.commitChanges()

    def save_layer(self):
        pass

    def set_dem_layer(self, layer: QgsRasterLayer):
        self._dem_layer = layer

    def set_desired_alt(self, desired_alt: float):
        self._desired_alt = desired_alt

    def set_takeoff_point_alt(self, to_point_alt: float):
        self._takeoff_point_altitude = to_point_alt

    def set_up_deviation_alt(self, up_dev: float):
        self._up_deviation = up_dev

    def set_down_deviation_alt(self, down_dev: float):
        self._down_deviation = down_dev
