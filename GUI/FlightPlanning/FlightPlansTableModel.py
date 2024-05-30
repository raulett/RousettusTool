import multiprocessing
import os
from pathlib import Path
from typing import Any, List
import re
import time

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant, QMutex
from PyQt5.QtGui import QIcon
from qgis.core import QgsFeature, QgsField, QgsVectorLayer, QgsFields, QgsGeometry, QgsRasterLayer, QgsPoint, \
    QgsFeatureRequest, QgsProject, QgsCoordinateReferenceSystem, QgsCoordinateTransform

from GUI.FlightPlanning.FlightPlannerWorker import FlightPlannerWorker
from GUI.FlightPlanning.FlightPlanFeatureFabric import FlightPlanFeatureFabric

from tools.ServiceClasses.RousettusLoggerHandler import RousettusLoggerHandler
from tools.VectorLayerSaverGPKG.FlightLayerSaverGPKG import FlightLayerSaverGPKG
from tools import constants


class FlightPlansTableModel(QAbstractTableModel):

    def __init__(self, layer: QgsVectorLayer, method_name: str, main_window):
        super().__init__()
        self.logger = RousettusLoggerHandler.get_handler().logger
        self.method_name = method_name
        self.main_window = main_window
        self._thread_count = 0
        self._down_deviation = None
        self._up_deviation = None
        self._takeoff_point_altitude = None
        self._desired_alt = None
        self._dem_layer = None
        self._dem_band = None
        self._planning_mutex = None
        self.logger.debug(f"Flights table model, route layer: {layer}")
        if layer is not None:
            self.flights_layer_name = layer.name().replace('routes', 'flights')
            self.to_point = re.search(r'^routes_iteration-\d*_(.*)$', layer.name()).group(0)
            self.logger.debug(f"takeoff point name: {self.to_point}")
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
        self.layer_saver = FlightLayerSaverGPKG(self.method_name, self._temp_flight_layer, self.main_window)

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

    def remove_data(self, removing_feats: List[int]):
        feat_names = [self._data[index].get('route_feature').attribute('name') for index in removing_feats]
        temp_data_names_list = [feat.get('route_feature').attribute('name') for feat in self._data]
        self.beginResetModel()
        self._temp_flight_layer.startEditing()
        for name in feat_names:
            rem_index = temp_data_names_list.index(name)
            self._data.pop(rem_index)
            temp_data_names_list.pop(rem_index)
            request = QgsFeatureRequest().setFilterExpression(f'"name" = \'{name}\'')
            features = self._temp_flight_layer.getFeatures(request)
            for feature in features:
                self._temp_flight_layer.deleteFeature(feature.id())
        self.endResetModel()
        self._temp_flight_layer.commitChanges()
        self._temp_flight_layer.updateExtents()

    def start_workers(self):
        """
        Функция для запуска обработчиков планирования добавленных полетов. Сначала маршруты добавляются в очередь обработки,
        потом создаются обработчики не более чем размер очереди или количество ядер.
        """
        self._planning_mutex.lock()
        for route_feature in self._data:
            if (not route_feature.get('flight_planned') and route_feature.get('route_feature')
                    and route_feature.get('route_feature').attribute('name') not in
                    [feat.attribute('name') for feat in self._planning_queue]):
                self._planning_queue.append(route_feature.get('route_feature'))
        self._planning_mutex.unlock()
        self._thread_count = min(len(self._planning_queue), self._thread_num)
        while self._thread_count > 0:
            self.logger.debug(f'Thread count in while cycle: {self._thread_count}')
            self._worker_management_mutex.lock()
            self.logger.debug(f'Worker management mutex locked')
            self._thread_count -= 1
            self._worker_management_mutex.unlock()
            self.logger.debug(f'Worker management mutex unlocked')
            self._workers[self._thread_count] = FlightPlannerWorker(self._planning_queue,
                                                                    self._result_queue,
                                                                    self._thread_count,
                                                                    self._planning_mutex,
                                                                    self._result_mutex,
                                                                    self.crs,
                                                                    self._dem_layer,
                                                                    self._desired_alt,
                                                                    self._takeoff_point_altitude,
                                                                    self._up_deviation,
                                                                    self._down_deviation)
            self._workers.get(self._thread_count).finished_all.connect(self.worker_finished)
            self._workers.get(self._thread_count).planned_flight.connect(self.worker_planned_flight)
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
        if flight_plan is not None:
            flight_features = flight_plan.get_flight()
        else:
            return
        try:  #Эта проверка на случай если строчку удалили из списка до того как воркер закончил работу.
            index = [feat.get('route_feature').attribute('name')
                     for feat in self._data].index(flight_plan.get_route_feature().attribute('name'))
        except ValueError:
            return
        route_feature = flight_plan.get_route_feature()
        self.beginResetModel()
        self._data[index]['flight_planned'] = True
        self._data[index]['flight_plan'] = flight_plan
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
        self._temp_flight_layer.commitChanges()
        self._temp_flight_layer.updateExtents()

    def _make_waypoints_flight_plan(self, flight_plan_features: List[QgsFeature],
                                    crs: QgsCoordinateReferenceSystem) -> str:
        """
        Формирует строку представляющую файл waypoints для загрузки в MissionPlanner
        :param flight_plan_layer:
        :return:
        """
        flight_plan_features.sort(key=lambda input_feat: input_feat.attribute('point_num'))
        coord_transform = QgsCoordinateTransform(crs, QgsCoordinateReferenceSystem(4326), QgsProject.instance())
        waypoints_file_content = "QGC WPL 110\n"
        for i, feat in enumerate(flight_plan_features):

            flight_point = coord_transform.transform(feat.geometry().asPoint())
            alt = feat.attribute('alt')
            if i == 0:
                waypoints_file_content += (f"{str(i)}\t1\t0\t16\t0.0\t0.0\t0.0\t0.0"
                                           f"\t{str(flight_point.y())}"
                                           f"\t{str(flight_point.x())}"
                                           f"\t{str(feat.attribute('alt_asl'))}\t1\n")
            waypoints_file_content += (f"{str(i+1)}\t0\t3\t16\t0.0\t0.0\t0.0\t0.0"
                                       f"\t{str(flight_point.y())}\t{str(flight_point.x())}\t{str(alt)}\t1\n")
        # TODO оттестировать постановку первой точки. Нормально ли, что она стоит на высоте?
        # TODO добавить функционал выставления acc radius для точки. сейчас 0.
        #  Лучше поставить равным отклонению вниз max_dn_dev
        # TODO нет изменений скорости при планировании полета. Стоит сделать.
        flight_point = coord_transform.transform(flight_plan_features[-1].geometry().asPoint())
        alt = flight_plan_features[-1].attribute('alt')
        waypoints_file_content += (f"{str(len(flight_plan_features) + 1)}"
                                   f"\t0\t3\t20\t0.0\t0.0\t0.0\t0.0"
                                   f"\t{str(flight_point.y())}"
                                   f"\t{str(flight_point.x())}"
                                   f"\t{str(alt)}\t1\n")
        return waypoints_file_content

    def export_waypoints_files(self, flight_layer: QgsVectorLayer):
        def write_waypoints_file(flight_name: str):
            filepath = Path(QgsProject.instance().absolutePath(),
                            constants.get_flight_waypoints_filepath(
                                self.method_name,
                                flight_name,
                                flight_layer.name().split('_')[-1]
                            )
                            )
            filepath.parents[0].mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"filename: {filepath}, save waypoints filepath: {filepath.parents[0]}")
            request = QgsFeatureRequest().setFilterExpression(f'"name" = \'{flight_name}\'')

            feats = [f for f in flight_layer.getFeatures(request)]
            self.logger.debug(f'current flight name {flight_name}, features: {feats}')
            waypoints_file_content = self._make_waypoints_flight_plan(feats, flight_layer.crs())
            with open(filepath, 'w') as f:
                f.write(waypoints_file_content)

        flight_names = flight_layer.dataProvider().uniqueValues(flight_layer.dataProvider().fieldNameIndex('name'))
        self.logger.debug(f"exporting file names: {flight_names}")
        curr_time = time.time()
        for f_name in list(flight_names):
            write_waypoints_file(f_name)
        self.logger.debug(f"saving time: {time.time() - curr_time}")

    def save_flight_layer(self):
        self.logger.debug(f"saving flight layer: {self._temp_flight_layer.name()}, "
                          f"{self._temp_flight_layer.featureCount()} features")
        self.layer_saver.renew_features(self._temp_flight_layer)
        self.layer_saver.set_style_to_flights_layer()

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

    def get_layer(self) -> QgsVectorLayer:
        return self._temp_flight_layer
