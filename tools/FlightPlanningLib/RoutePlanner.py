from typing import List, Tuple, Dict

from PyQt5.QtCore import pyqtSignal, QVariant
from PyQt5.QtWidgets import QMessageBox

from qgis.core import QgsVectorLayer, QgsFeature, QgsPoint, QgsCoordinateReferenceSystem, QgsCoordinateTransform, \
    QgsProject, QgsPointXY, QgsLineString, QgsGeometry, QgsSpatialIndex, QgsFeatureRequest, QgsWkbTypes, QgsFields, \
    QgsField, QgsExpression

# import pydevd_pycharm
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class RoutePlanner:
    """
    TODO Перевести комментарии а английский.
    Класс, реализующий функциональность планирования маршрутов.
    """
    debug = 0
    plan_next_route_debug = 0
    get_nearest_profiles_pair_debug = 0
    plan_p_segment_debug = 0
    plan_p_segment_outer_debug = 0
    move_feats_debug = 0
    rotate_feats_debug = 0
    process_algorithm_debug_step_planning = 0
    process_algorithm_debug = 0
    init_debug = 0
    initial_choose_profiles_debug = 0
    debug_visualisation = 0
    cut_segment_debug = 0
    estimate_single_profile_debug = 0

    status_signal = pyqtSignal(str)
    pecent_status_signal = pyqtSignal(int)

    def __init__(self,
                 profile_layer: QgsVectorLayer,
                 max_service_flight_len: int,
                 max_flight_len: int,
                 takeoff_point: QgsFeature,
                 takeoff_point_crs: QgsCoordinateReferenceSystem,
                 selected_only_flag=False,
                 plan_ring_segments_flag=True):
        """
        Конструктор класса для планирования полетных маршрутов
        :param profile_layer: QgsVectorLayer, Слой опорных профилей для планирования маршрутов. Оттуда берется азимут
        и расстояние между профилями
        :param max_service_flight_len: int, Максимальная дальность долета.
        :param max_flight_len: int Максимальная дальность всего маршрута.
        :param takeoff_point: Взлетная точка вместе с именем.
        :type QgsFeature
        :param takeoff_point_crs
        :type QgsCoordinateReferenceSystem
        """
        if self.init_debug:
            print("\n====_init======")
            print("input layer name: ", profile_layer.name())
        self.plan_ring_flights = plan_ring_segments_flag
        self.selected_only_flag = selected_only_flag
        profile_feature_to_get_attributes = list(profile_layer.getFeatures())[0]
        self.input_profiles_layer = profile_layer
        self.profiles_azimuth = profile_feature_to_get_attributes.attribute('azimuth')
        self.profiles_distance = profile_feature_to_get_attributes.attribute('pr_dist')
        self.takeoff_point_name = takeoff_point.attribute('name')
        self.max_flight_len = max_flight_len
        self.max_service_flight_len = max_service_flight_len
        self.profile_layer_crs = profile_layer.crs()
        self.to_point_crs = takeoff_point_crs
        if self.init_debug:
            print("source crs: {}, dest crs: {}".format(self.profile_layer_crs, self.to_point_crs))
        coord_transform = QgsCoordinateTransform(self.to_point_crs, self.profile_layer_crs, QgsProject.instance())
        self.takeoff_point_geometry = takeoff_point.geometry()
        transform_result = self.takeoff_point_geometry.transform(coord_transform)
        self._current_takeoff_point_place = self.takeoff_point_geometry.asPoint()
        if self.init_debug:
            print("current takeoff point coordinate: ", self._current_takeoff_point_place)
            print("transform_result: ", transform_result)
        self.not_planned_profiles = []
        self.planned_routes = []
        if not selected_only_flag:
            features = profile_layer.getFeatures()
        else:
            features = profile_layer.selectedFeatures()
            self.selected_features_ids = profile_layer.selectedFeatureIds()
        for feature in features:
            output_feature = QgsFeature(feature)
            self.not_planned_profiles.append(output_feature)
        if self.init_debug:
            print("not planned profiles len: ", len(self.not_planned_profiles))
        self.temp_planning_profiles = []
        self.temp_planning_profiles_layer = QgsVectorLayer()
        self.planned_routes_fields = QgsFields()
        self.planned_routes_fields.append(QgsField('name', QVariant.String))
        self.planned_routes_fields.append(QgsField('service', QVariant.String))
        self.planned_routes_fields.append(QgsField('length', QVariant.Double))
        self.planned_routes_fields.append(QgsField('profiles', QVariant.String))
        if self.init_debug:
            print("====end init======\n")

    def process_algorithm(self):
        """
        Основной алгоритм, осуществляющий планирование маршрутов.
        :return:
        """
        # Отберем профиля на расстоянии долета в новый слой

        if self.process_algorithm_debug:
            print("\n====general process algorithm======")
        self.rotate_features()
        self.move_features()
        self.scale_features()
        self.temp_planning_profiles, self.not_planned_profiles = \
            self.initial_choose_profiles(self.not_planned_profiles)
        if self.process_algorithm_debug:
            print("len of temp planning profiles: ", len(self.temp_planning_profiles))
            print("len of not planned profiles: ", len(self.not_planned_profiles))
            cycle_count = 0

        while len(self.temp_planning_profiles) > 0:
            if self.process_algorithm_debug:
                print("iteration {} began".format(cycle_count))
                cycle_count += 1
            planned_route = self.plan_next_route()

            if self.process_algorithm_debug_step_planning:
                out_of_plan_profiles_layername = "out_of_plan"
                routes_layer_name = "routes"
                geom_type = "LineString"
                layers = QgsProject.instance().mapLayersByName(routes_layer_name)
                if len(layers) > 0:
                    QgsProject.instance().removeMapLayer(layers[0].id())
                routes_layer = QgsVectorLayer(geom_type,
                                              routes_layer_name,
                                              "memory")
                routes_layer.setCrs(self.profile_layer_crs)
                if routes_layer.isValid():
                    temp_provider = routes_layer.dataProvider()
                    if len(self.planned_routes_fields) > 0:
                        temp_provider.addAttributes(self.planned_routes_fields)
                    routes_layer.updateFields()
                    QgsProject.instance().addMapLayer(routes_layer)
                    for feat in self.get_planned_routes():
                        temp_provider.addFeature(feat)

                layers = QgsProject.instance().mapLayersByName(out_of_plan_profiles_layername)
                if len(layers) > 0:
                    QgsProject.instance().removeMapLayer(layers[0].id())
                out_of_plan_profiles_layer = QgsVectorLayer(geom_type,
                                                            out_of_plan_profiles_layername,
                                                            "memory")
                out_of_plan_profiles_layer.setCrs(self.profile_layer_crs)
                if out_of_plan_profiles_layer.isValid():
                    temp_provider = out_of_plan_profiles_layer.dataProvider()
                    temp_provider.addAttributes(self.input_profiles_layer.fields())
                    out_of_plan_profiles_layer.updateFields()
                    for feat in self.get_output_profiles():
                        temp_provider.addFeature(feat)
                    out_of_plan_profiles_layer.commitChanges()
                    out_of_plan_profiles_layer.updateExtents()
                    QgsProject.instance().addMapLayer(out_of_plan_profiles_layer)
                QMessageBox.information(None, 'New route done', 'new route generated')

            if planned_route is None:
                break
        self.scale_features(True).move_features(True).rotate_features(True)
        if self.process_algorithm_debug:
            print("====end general process algorithm======\n")

    def plan_next_route(self) -> QgsFeature or None:
        '''
        Планирует следующий маршрут. Возвращает QgsFeature с новым сегментом или None, если профилей для планирования
        больше нет.
        На месте изменяет список спланированных маршрутов,
        Изменяет список профилей для планирования
        Изменяет список профилей исключенных из планирования
        :return:
        '''
        if self.plan_next_route_debug:
            print("\n===plan next route===")
        result_route_points = []
        result_attribute_points = []
        exluded_profiles = []
        result_profiles_with_point_binds = {}
        estimation_result = True
        plan_current_point = self._current_takeoff_point_place
        first_segment_flag = True
        current_max_len = self.max_flight_len
        route_len = 0
        dist_to_home_from_current_point = 0
        result_route_points.append(plan_current_point)
        direction_dict = {1: 0, -1: 0, 0: 0}
        self.temp_planning_profiles_layer = self.pack_to_layer(self.temp_planning_profiles)
        direction = 0
        while estimation_result is not None:
            # Отберем следующую пару профилей. Они отбираются из временного слоя temp_layer, надо следить за его
            # актуальностью
            if self.plan_next_route_debug:
                print("===========")
                print("go into While cycle")
            nearest_profiles_pair = self.get_nearest_profiles_pair(plan_current_point,
                                                                   self.temp_planning_profiles_layer,
                                                                   exluded_profiles)

            if nearest_profiles_pair is None:
                if self.plan_next_route_debug:
                    print("nearest_profiles_pair is none")
                break
            else:
                profiles_num, *nearest_profiles = nearest_profiles_pair
                if self.plan_next_route_debug:
                    print("current nearest profiles pair in plan next route: ", [near_profile.attribute('prof_num')
                                                                                 for near_profile in nearest_profiles
                                                                                 if near_profile is not None])
                # if nearest_profiles[0] is not None and \
                #         nearest_profiles[0].attribute('prof_num') in list(range(210, 216)):
                #     pydevd_pycharm.settrace('localhost', port=5566, stdoutToServer=True, stderrToServer=True)
            # Проверим случай планирования для одинарного профиля
            if profiles_num == 1:
                estimation_result = self.estimate_single_profile(nearest_profiles,
                                                                 plan_current_point,
                                                                 current_max_len
                                                                 - route_len
                                                                 - dist_to_home_from_current_point,
                                                                 first_segment_flag)

            else:
                # Случай, когда у нас 2 профиля
                # Проверим, что можно запланировать полет по кольцу. Отменим планирование по кольцу
                if self.plan_ring_flights:
                    segment_len = nearest_profiles[0].geometry().distance(QgsGeometry.fromPointXY(plan_current_point))
                    segment_len += 2 * nearest_profiles[0].geometry().distance(nearest_profiles[1].geometry())
                    for prof in nearest_profiles:
                        segment_len += prof.geometry().length()
                if all([prof_point.y() >= self._current_takeoff_point_place.y()
                        for prof_point in nearest_profiles[0].geometry().asPolyline()]) or \
                        all([prof_point.y() <= self._current_takeoff_point_place.y()
                             for prof_point in nearest_profiles[0].geometry().asPolyline()]):
                    # Если все точки лежат к югу или к северу от стартовой.
                    if self.plan_next_route_debug:
                        print("-> planning p segment with outer point")
                    estimation_result = self.estimate_p_segment_with_outer_point(nearest_profiles,
                                                                                 plan_current_point,
                                                                                 current_max_len
                                                                                 - route_len
                                                                                 - dist_to_home_from_current_point,
                                                                                 first_segment_flag,
                                                                                 direction)
                elif self.plan_ring_flights and (segment_len < current_max_len - dist_to_home_from_current_point):
                    if self.plan_next_route_debug:
                        print("-> planning o segment")
                    estimation_result = self.estimate_o_segment(nearest_profiles,
                                                                plan_current_point,
                                                                current_max_len
                                                                - route_len
                                                                - dist_to_home_from_current_point)

                else:
                    # Случай, если стартовая точка лежит в середине профиля
                    if self.plan_next_route_debug:
                        print("-> planning p segment with inner point")
                    estimation_result = self.estimate_p_segment_with_inner_point(nearest_profiles,
                                                                                 plan_current_point,
                                                                                 current_max_len
                                                                                 - route_len
                                                                                 - dist_to_home_from_current_point,
                                                                                 first_segment_flag,
                                                                                 direction)

            if self.plan_next_route_debug:
                print("checking estimation result: ", estimation_result)

            if estimation_result is not None:
                segment_points, attribute_points, current_segment_len, profiles_with_points_bind, \
                    current_point, direction = estimation_result
                result_route_points.extend(segment_points)
                result_attribute_points.extend(attribute_points)
                exluded_profiles.extend([nearest_profile for nearest_profile in nearest_profiles
                                         if nearest_profile is not None])
                plan_current_point = current_point
                dist_to_home_from_current_point = plan_current_point.distance(self._current_takeoff_point_place)
                route_len += current_segment_len
                result_profiles_with_point_binds.update(profiles_with_points_bind)
                direction_dict[direction] += 1
            first_segment_flag = False

        result_route_points.append(self._current_takeoff_point_place)
        result_attribute_points.append(0)
        if self.plan_next_route_debug:
            print("result route points count: ", len(result_route_points))
            print("if <= 2 will be return none")
        if len(result_route_points) <= 2:
            return None
        route_len += plan_current_point.distance(self._current_takeoff_point_place)
        # Формируем имя маршрута
        route_num_prefix = [min([int(prof_id.attribute('prof_num') / 2) for prof_id in exluded_profiles \
                                 if prof_id.attribute('prof_num') % 2 == 0],
                                default=int((exluded_profiles[0].attribute('prof_num') + 1) / 2)),
                            max([int(prof_id.attribute('prof_num') / 2) for prof_id in exluded_profiles \
                                 if prof_id.attribute('prof_num') % 2 == 0],
                                default=int((exluded_profiles[0].attribute('prof_num') + 1) / 2))]
        if route_num_prefix[0] == route_num_prefix[1]:
            route_num_prefix = f'{route_num_prefix[0]}'
        else:
            route_num_prefix = f"{route_num_prefix[0]}-{route_num_prefix[1]}"

        route_general_direction = max([direction_dict_key for direction_dict_key in direction_dict.keys()],
                                      key=lambda dir_value: direction_dict.get(dir_value))
        if route_general_direction == 1:
            route_direction_prefix = "N"
        elif route_general_direction == -1:
            route_direction_prefix = "S"
        else:
            route_direction_prefix = "O"
        estimate_route_name = "{}_f{}{}".format(self.takeoff_point_name, route_num_prefix, route_direction_prefix)
        planned_routes_names = [planned_route.attribute('name') for planned_route in self.planned_routes]
        counter = 0
        while estimate_route_name in planned_routes_names:
            counter += 1
            estimate_route_name = "{}_f{}{}_{}".format(self.takeoff_point_name, route_num_prefix,
                                                       route_direction_prefix, counter)
        # Формируем значения аттрибутов
        route_service_str = ";".join([str(attr) for attr in result_attribute_points])
        route_geometry = QgsGeometry().fromPolylineXY(result_route_points)
        route_length = route_len
        route_profiles = ";".join([str(prof.attribute('prof_num')) for prof in exluded_profiles])
        route_feature = QgsFeature()
        route_feature.setFields(self.planned_routes_fields)
        route_feature.setAttributes([estimate_route_name, route_service_str, route_length / 10, route_profiles])
        route_feature.setGeometry(route_geometry)
        if self.plan_next_route_debug:
            print("output of 'plan next route': ")
            print("current route feature: ", route_feature.attributes(), "route_feature geom: ",
                  route_feature.geometry().asPolyline())
        new_profiles, removing_profiles_ids = self.cut_segment_from_profiles(self.temp_planning_profiles_layer,
                                                                             result_profiles_with_point_binds)
        temp_data_provider = self.temp_planning_profiles_layer.dataProvider()
        if self.plan_next_route_debug:
            print("result of cut_segment: new_profiles_len: ", len(new_profiles),
                  " removing_profiles_len: ", len(removing_profiles_ids))
            print(" count temp profiles in layer: ", len(list(self.temp_planning_profiles_layer.getFeatures())))
        temp_data_provider.deleteFeatures(removing_profiles_ids)
        if self.plan_next_route_debug:
            print(" count temp profiles in layer after delete: ",
                  len(list(self.temp_planning_profiles_layer.getFeatures())))
        temp_data_provider.addFeatures(new_profiles)
        if self.plan_next_route_debug:
            print(" count temp profiles in layer after add: ",
                  len(list(self.temp_planning_profiles_layer.getFeatures())))
        self.temp_planning_profiles_layer.commitChanges()
        self.planned_routes.append(route_feature)
        if self.plan_next_route_debug:
            print("planned profiles len: ", len(self.planned_routes))
        temp_planning_profiles, output_profiles = \
            self.initial_choose_profiles(list(self.temp_planning_profiles_layer.getFeatures()))
        self.temp_planning_profiles = temp_planning_profiles
        self.not_planned_profiles.extend(output_profiles)
        if len(self.temp_planning_profiles) > 0:
            self.temp_planning_profiles_layer = self.pack_to_layer(self.temp_planning_profiles)
        if self.plan_next_route_debug:
            print("\n===End plan next route===")
        return route_feature

    def get_nearest_profiles_pair(self,
                                  start_point: QgsPointXY,
                                  profiles_layer: QgsVectorLayer,
                                  exclude_profiles: List[QgsFeature]) -> \
            Tuple[int, int, int or None] or None:
        """
        Служебная функция взятия следующей пары профилей.
        :param start_point:
        :param profiles_layer:
        :param exclude_profiles Список профилей, которые будут исключены из отбора
        :return: Возвращает количество профилей (Их должно быть 2, но может оказаться и один, если у последнего
        профиля нет пары) и пару профилей ближайшую к переданной точке. Ближайший всегда возврашается первым
        :rtype: Typle[int Количество профилей.
        QgsFeature первого, профиля.
        QgsFeature второй, профиль с номером +1, может быть None
        """
        # Отберем ближайшие профиля или None, Если больше профилей нет, с учетом исключенных.
        exclude_profiles_numbers = [feat.attribute('prof_num') for feat in exclude_profiles]
        exclude_string = ",".join([f"\'{str(i)}\'" for i in exclude_profiles_numbers])
        if len(exclude_profiles) > 0:
            request = QgsFeatureRequest().setFilterExpression(f"{'prof_num'} NOT IN ({exclude_string})")
            index = QgsSpatialIndex(profiles_layer.getFeatures(request))
        else:
            index = QgsSpatialIndex(profiles_layer.getFeatures())
        nearest_neighbor = index.nearestNeighbor(start_point)
        if self.get_nearest_profiles_pair_debug:
            print("\n===begin get nearest profile===")
            print("go into get nearest number")
            print("current exluding profiles: ", exclude_string)
            print("current start_point: ", start_point)
            print("current feature count in layer: ", profiles_layer.featureCount())
            print("current nearest_neighbor = index.nearestNeighbor(start_point) length: ", len(nearest_neighbor))
        if len(nearest_neighbor) > 0:
            frist_prof_feature = profiles_layer.getFeature(nearest_neighbor[0])
            if self.get_nearest_profiles_pair_debug:
                print("current first profile: ", frist_prof_feature)
                print("current first profile num: ", frist_prof_feature.attribute('prof_num'))
        else:
            if self.get_nearest_profiles_pair_debug:
                print("there is no profiles pair, return None")
                print("===end get nearest profile===\n")
            return None
        # Получим парный ему профиль (его номер + 1 если первый нечетный и -1, если четный.)
        second_profile_num = frist_prof_feature.attribute('prof_num') + \
                             (1 if frist_prof_feature.attribute('prof_num') % 2 == 1 else -1)
        if self.get_nearest_profiles_pair_debug:
            print("calculated second profile num: ", second_profile_num)

        if len(exclude_profiles) > 0:
            request = QgsFeatureRequest().setFilterExpression(
                f"{'prof_num'} = '{str(second_profile_num)}' and 'prof_num' NOT IN ({exclude_string})")
        else:
            request = QgsFeatureRequest().setFilterExpression(
                f"{'prof_num'} = '{second_profile_num}'")

        index = QgsSpatialIndex(profiles_layer.getFeatures(request))
        nearest_neighbor = index.nearestNeighbor(start_point)
        if len(nearest_neighbor) > 0:
            second_prof_feature = profiles_layer.getFeature(nearest_neighbor[0])
        else:
            second_prof_feature = None
        # сформируем возвращаемые данные для выдачи
        features_num = 1 if second_prof_feature is None else 2
        if self.get_nearest_profiles_pair_debug:
            print("profile 1: {}, profile 2: {}".format(frist_prof_feature.attribute('prof_num'),
                                                        second_prof_feature.attribute('prof_num')
                                                        if second_prof_feature is not None else None))
            print("==========\n")
        return features_num, frist_prof_feature, second_prof_feature

    def estimate_single_profile(self,
                                profile_feats: List[QgsFeature],
                                initial_point: QgsPointXY,
                                max_segment_len: int,
                                first_segment_in_route_flag: bool) -> \
            Tuple[List[QgsPointXY], List[int], int, Dict[int, List[QgsPointXY]], QgsPointXY, int] or None:
        '''
        Служебная функция оценки полета по единственному профилю. Летит к ближайшей точке, а потом летит к следующей
        :param profile_feats: Список профилей. Второй профиль None
        :param initial_point: стартовая точка
        :param max_segment_len: Масимальная длинна сегмента
        :param first_segment_in_route_flag:
        :return: Список маршрутных точек сегмента,
        Список аттрибутов маршрутных точек (служебный, рабочий),
        длина сегмента
        Словарь связей: профиль - точки
        Финальная точка,
        Направление
        None, Если сегмент не удается спланировать в указанных ограничениях.
        :rtype: Tuple[List[QgsPointXY], List[int], int, Dict[int, List[QgsPointXY]], QgsPointXY, int] or None
        '''
        if self.estimate_single_profile_debug:
            print("\n===begin estimate single profile===")
        segment_points = []
        attribute_points = []
        current_segment_len = 0
        current_point = initial_point
        vertex_list = sorted(profile_feats[0].geometry().asPolyline(),
                             key=lambda point: QgsGeometry.fromPointXY(initial_point).
                             distance(QgsGeometry.fromPointXY(point)))
        # ставим первую точку 1 на ближайшей точке профиля
        segment_points.append(vertex_list[0])
        attribute_points.append(0)
        current_segment_len += vertex_list[0].distance(current_point)
        current_point = vertex_list[0]
        if vertex_list[1].y() - current_point.y() > 0:
            # Направление - север
            direction = 1
        elif vertex_list[1].y() - current_point.y() < 0:
            # Направление - юг
            direction = -1
        else:
            if self.estimate_single_profile_debug:
                print("vertex distance is 0, return NONE")
                print("===end estimate single profile===\n")
            return None
        max_profile_segment = (max_segment_len - 2 * current_segment_len) / 2
        if current_point.distance(vertex_list[1]) <= max_profile_segment:
            point = vertex_list[1]
        else:
            if first_segment_in_route_flag:
                point = QgsPointXY(vertex_list[1].x(), current_point.y() + direction * max_profile_segment)
            else:
                if self.estimate_single_profile_debug:
                    print("it is not first segment, and distance is not enough, return NONE")
                    print("===end estimate single profile===\n")
                return None
        segment_points.append(point)
        attribute_points.append(1)
        current_segment_len += point.distance(current_point)
        current_point = point
        profiles_with_points_bind = {profile_feats[0].attribute('fid'): segment_points}
        print("===end estimate single profile===\n")
        return segment_points, attribute_points, current_segment_len, \
            profiles_with_points_bind, current_point, direction

    def estimate_p_segment_with_inner_point(self,
                                            profile_feats: List[QgsFeature],
                                            initial_point: QgsPointXY,
                                            max_segment_len: int,
                                            first_segment_in_route_flag: bool,
                                            direction: int = 0) -> \
            Tuple[List[QgsPointXY], List[int], int, Dict[int, List[QgsPointXY]], QgsPointXY, int] or None:
        '''
        Служебная функция, когда profile_point_1.y() < takeoff_point.y < profile_point_2.y(), Внутри себя
        разбивает профиль на 2 части и использует функцию планирования для внешней точки.
        :param profile_feats: Профиля над которыми будет спланирован сегмент
        :param initial_point: Стартовая точка
        :param max_segment_len: Максимальная длина сегмента
        :param first_segment_in_route_flag: Флаг, первый ли это сегмент в полете
        :return: Список маршрутных точек сегмента,
        Список аттрибутов маршрутных точек (служебный, рабочий),
        длина сегмента
        Словарь связей: профиль - точки
        Финальная точка,
        Направление
        None, Если сегмент не удается спланировать в указанных ограничениях.
        :rtype: Tuple[List[QgsPointXY], List[int], int, Dict[int, List[QgsPointXY]], QgsPointXY, int] or None
        '''
        # Отработаем случай, когда у нас случай только одного профиля
        if self.plan_p_segment_debug:
            print("\n===estimate_p_segment_with_inner_point=====")
            print("input data: ")
            print("profile_feats len: ", [type(profile_feat) for profile_feat in profile_feats])
            print("initial point: ", initial_point)
            print("max_segment_len: ", max_segment_len)
            print("first_segment_in_route_flag: ", first_segment_in_route_flag)
        temp_profiles = []
        for profile_feat in profile_feats:
            if profile_feat is not None:
                feat = QgsFeature()
                feat.setFields(profile_feat.fields())
                feat.setAttributes(profile_feat.attributes())
                profile_feat_points = profile_feat.geometry().asPolyline()
                geometry = QgsGeometry().fromPolylineXY([QgsPointXY(profile_feat_points[0].x(),
                                                                    max([
                                                                        self._current_takeoff_point_place.y(),
                                                                        min([point.y() for point in
                                                                             profile_feat_points])])),
                                                         QgsPointXY(profile_feat_points[0].x(),
                                                                    max(profile_feat_points, \
                                                                        key=lambda point: point.y()).y())])
                feat.setGeometry(geometry)
                temp_profiles.append(feat)
            else:
                temp_profiles.append(None)
        if self.plan_p_segment_debug:
            print("Formed new profiles to call p segment with outer point estimation: \n",
                  ["feat: " + str(feat.geometry().asPolyline()) for feat in temp_profiles])
        estimation_result = self.estimate_p_segment_with_outer_point(temp_profiles,
                                                                     initial_point,
                                                                     max_segment_len,
                                                                     first_segment_in_route_flag)
        if self.plan_p_segment_debug:
            print("Estimation p segment with outer point result output:", estimation_result)
        if estimation_result is None:
            '''Если спланировать полет на север не получилось, потому что не хватило расстояния, проверим планирование
            на юг.'''
            temp_profiles = []
            for profile_feat in profile_feats:
                if profile_feat is not None:
                    feat = QgsFeature()
                    feat.setFields(profile_feat.fields())
                    feat.setAttributes(profile_feat.attributes())
                    profile_feat_points = profile_feat.geometry().asPolyline()
                    geometry = QgsGeometry().fromPolylineXY([QgsPointXY(profile_feat_points[0].x(),
                                                                        min(profile_feat_points,
                                                                            key=lambda point: point.y()).y()),
                                                             QgsPointXY(profile_feat_points[0].x(),
                                                                        min([self._current_takeoff_point_place.y(),
                                                                             max([point.y() for point in
                                                                                  profile_feat_points])]))])
                    feat.setGeometry(geometry)
                    temp_profiles.append(feat)
                else:
                    temp_profiles.append(None)
        estimation_result = self.estimate_p_segment_with_outer_point(temp_profiles,
                                                                     initial_point,
                                                                     max_segment_len,
                                                                     first_segment_in_route_flag)
        if estimation_result is None:
            return None
        segment_points, attribute_points, current_segment_len, profiles_with_points_bind, current_point, direction = \
            estimation_result
        res_profiles_with_points_bind = {}
        for profile_feat_num in range(len(profile_feats)):
            if profile_feats[profile_feat_num] is not None:
                res_profiles_with_points_bind[profile_feats[profile_feat_num].attribute('fid')] = \
                    profiles_with_points_bind.get(temp_profiles[profile_feat_num].attribute('fid'))
        if self.plan_p_segment_debug:
            print("===return estimate_p_segment_with_inner_point=====\n")
        return segment_points, attribute_points, current_segment_len, \
            res_profiles_with_points_bind, current_point, direction

    def estimate_p_segment_with_outer_point(self,
                                            profile_feats: List[QgsFeature],
                                            initial_point: QgsPointXY,
                                            max_segment_len: int,
                                            first_segment_in_route_flag: bool,
                                            direction: int = 0) -> \
            Tuple[List[QgsPointXY], List[int], int, Dict[int, List[QgsPointXY]], QgsPointXY, int] or None:

        '''
        Служебная функция для оценки П сегмента в одну сторону (Когда весь полет выполняется в одну сторону,
        на юг или на север). Факт того, что полет односторонний проверяется вне функции.
        :param profile_feats: Профиля над которыми будет спланирован сегмент
        :param initial_point: Стартовая точка
        :param max_segment_len: Максимальная длина сегмента
        :param first_segment_in_route_flag: Флаг, первый ли это сегмент в полете
        :return: Список маршрутных точек сегмента,
        Список аттрибутов маршрутных точек (служебный, рабочий),
        длина сегмента
        Словарь связей: профиль - точки
        Финальная точка,
        Направление
        None, Если сегмент не удается спланировать в указанных ограничениях.
        :rtype: Tuple[List[QgsPointXY], List[int], int, Dict[int, List[QgsPointXY]], QgsPointXY, int] or None
        '''
        if self.plan_p_segment_outer_debug:
            print("\n===estimate_p_segment_with_outer_point=====")
            print("input data: ")
            print("profile_feats fields: ", profile_feats[0].fields().toList())
            print("profile_feats num: ", [profile_feat.attribute('prof_num') for profile_feat in profile_feats])
            print("initial point: ", initial_point)
            print("max_segment_len: ", max_segment_len)
            print("first_segment_in_route_flag: ", first_segment_in_route_flag)
        segment_points = []
        attribute_points = []
        current_segment_len = 0
        profiles_with_points_bind = {profile_feats[0].attribute('fid'): []}
        profiles_points = [point for point in profile_feats[0].geometry().asPolyline()] + \
                          [point for point in profile_feats[1].geometry().asPolyline()]
        if self.plan_p_segment_outer_debug:
            print("profiles points: ", [point for point in profile_feats[0].geometry().asPolyline()] + \
                  [point for point in profile_feats[1].geometry().asPolyline()])
            print("first profile: ", profile_feats[0].geometry())
            print("second profile: ", profile_feats[1].geometry())
            print("direction condition: ", [point.y() - self._current_takeoff_point_place.y() >= 0
                                            for point in profiles_points])
        if all([point.y() - self._current_takeoff_point_place.y() >= 0 for point in profiles_points]):
            # Направление - север
            direction = 1
        elif all([point.y() - self._current_takeoff_point_place.y() <= 0 for point in profiles_points]):
            # Направление - юг
            direction = -1
        else:
            direction = 0
        if self.plan_p_segment_outer_debug:
            print("got direction: {}".format(direction))
        # Поставим точку 1
        prof_geometry = profile_feats[0].geometry()
        current_point = self._current_takeoff_point_place.y()
        point = QgsPointXY(profile_feats[0].geometry().asPolyline()[0].x(),
                           min([point for point in prof_geometry.asPolyline()],
                               key=lambda point: QgsGeometry.fromPointXY(point).
                               distance(QgsGeometry.fromPointXY(self._current_takeoff_point_place))).y())
        segment_points.append(point)
        attribute_points.append(0)
        current_segment_len += initial_point.distance(point)
        if max_segment_len - current_segment_len <= 0:
            if self.plan_p_segment_outer_debug:
                print("===return {} estimate_p_segment_with_outer_point=====\n".format(None))
            return None
        profiles_with_points_bind.get(profile_feats[0].attribute('fid')).append(point)
        current_point = point
        # Определим направление: -1 на юг, 1 на север
        target_point = max([point for point in profile_feats[0].geometry().asPolyline()],
                           key=lambda point: abs(point.y() - current_point.y()))

        profiles_with_points_bind[profile_feats[1].attribute('fid')] = []

        dist_to_target_point = current_point.distance(target_point)
        # Поставим точку 2
        # Случай, когда не хватает расстояния долететь до конца профиля
        if self.plan_p_segment_outer_debug:
            print("Set_point_2 section")
        max_profile_seg_len = (max_segment_len - 2 * (current_segment_len + self.profiles_distance)) / 2
        if max_profile_seg_len < dist_to_target_point:
            # Если сегмент не превый, то возращаем None
            if not first_segment_in_route_flag:
                if self.plan_p_segment_outer_debug:
                    print("max_profile_seg_len < dist_to_target_point and first_segment_in_route_flag = 0")
                    print("===return {} estimate_p_segment_with_outer_point=====\n".format(None))
                return None
            point = QgsPointXY(target_point.x(), int(current_point.y() + direction * max_profile_seg_len))
        else:
            # Случай, когда хватает расстояния долететь до конца профиля
            point = QgsPointXY(target_point.x(), target_point.y())
        segment_points.append(point)
        attribute_points.append(1)
        current_segment_len += current_point.distance(point)
        profiles_with_points_bind.get(profile_feats[0].attribute('fid')).append(point)
        current_point = point
        # Ищем точку на профиле 2 до которой летим
        excess_len = max_profile_seg_len - dist_to_target_point  # Это соколько у нас осталось запаса дальности.
        if direction == 1:
            target_point = max(profile_feats[1].geometry().asPolyline(), key=lambda point: point.y())
            final_point = min(profile_feats[1].geometry().asPolyline(), key=lambda point: point.y())
        else:
            target_point = min(profile_feats[1].geometry().asPolyline(), key=lambda point: point.y())
            final_point = max(profile_feats[1].geometry().asPolyline(), key=lambda point: point.y())

        if self.plan_p_segment_outer_debug:
            print("Ищем точку на профиле 2 до которой летим")
            print("target point: {}, final point: {}".format(target_point, final_point))
            print("segment_points: ", segment_points)
        profile_len = target_point.distance(final_point)
        estimating_rest = current_point.distance(target_point) + profile_len + final_point.distance(initial_point)
        if self.plan_p_segment_outer_debug:
            print("profile 2 len: {}, estimating_rest: {}".format(profile_len, estimating_rest))
            print("max_segment_len - current_segment_len - "
                  "estimating_rest: {} - {} - {} = {}".format(max_segment_len, current_segment_len, estimating_rest,
                                                              max_segment_len - current_segment_len - estimating_rest))
        # поставим точку 3
        if max_segment_len - current_segment_len - estimating_rest >= 0:
            # Дальности хватает, планируем перелет в вершину
            point = target_point
        else:
            if not first_segment_in_route_flag:
                if self.plan_p_segment_outer_debug:
                    print("max_profile_seg_len < dist_to_target_point and first_segment_in_route_flag = 0")
                    print("===return {} estimate_p_segment_with_outer_point=====\n".format(None))
                return None
            else:
                point = QgsPointXY(profile_feats[1].geometry().asPolyline()[0].x(),
                                   current_point.y())
        segment_points.append(point)
        attribute_points.append(0)
        current_segment_len += current_point.distance(point)
        profiles_with_points_bind.get(profile_feats[1].attribute('fid')).append(point)
        current_point = point
        if self.plan_p_segment_outer_debug:
            print("Ищем точку 3 на профиле 2 до которой летим")
            print("segment_points: ", segment_points)
        # Ставим точку 4
        point = final_point
        segment_points.append(point)
        attribute_points.append(1)
        current_segment_len += current_point.distance(point)
        profiles_with_points_bind.get(profile_feats[1].attribute('fid')).append(point)
        current_point = point
        if self.plan_p_segment_outer_debug:
            print("result segment point: ", segment_points)
            print("===return estimate_p_segment_with_outer_point=====\n")
        return segment_points, attribute_points, current_segment_len, \
            profiles_with_points_bind, current_point, direction

    def estimate_o_segment(self,
                           profile_feats: List[QgsFeature],
                           initial_point: QgsPointXY,
                           max_segment_len: int) -> \
            Tuple[List[QgsPointXY], List[int], int, Dict[int, List[QgsPointXY]], QgsPointXY, int] or None:
        """
        Функция, планирующая сегмент маршрута по кольцу. Предполагается, что проверка длины сегмента будет выполнена
        вне функции.
        :param profile_feats: Список профилей. Должно быть 2 и только 2.
        :type List[QgsFeature]
        :param initial_point: Точка с которой стартует планирование полета
        :type QgsPointXY
        :param max_segment_len: Максимальная длинна сегмента для проверки
        :type int
        :return:
        :rtype: List[QgsPointXY] - Сисок маршрутных точек сегмента.
        List[int] - Список аттрибутов точек (сервисный, рабочий)
        int - Длинна сегмента
        Dict[int, List[QgsPointXY]] - Словарь отображающий связи между профилями и точками, для вырезания отрезков
        QgsPointXY - Точка на которой был окончен сегмент
        """
        # Инициализируем выходные данные
        current_segment_distance = 0
        segment_points = []
        segment_attributes = []
        profiles_with_points_bind = {profile_feats[0].attribute('fid'): [],
                                     profile_feats[1].attribute('fid'): []}
        profile_points_list = [feat.geometry().asPolyline() for feat in profile_feats]
        current_point = initial_point
        # Добавляем точку 1
        point = QgsPointXY(profile_points_list[0][0].x(), initial_point.y())
        segment_points.append(point)
        segment_attributes.append(0)
        current_segment_distance += QgsGeometry.fromPointXY(current_point).distance(QgsGeometry.fromPointXY(point))
        if current_segment_distance > max_segment_len:
            return None
        profiles_with_points_bind.get(profile_feats[0].attribute('fid')).append(point)
        current_point = point
        # Добавляем точкb 2-5
        extremum_func = max
        for i in range(2):
            for j in range(2):
                point = QgsPointXY(profile_points_list[(i + j) % 2][0].x(),
                                   extremum_func([pr_point.y() for pr_point in profile_points_list[(i + j) % 2]]))
                segment_points.append(point)
                segment_attributes.append((i + 1) % 2)
                current_segment_distance += QgsGeometry.fromPointXY(current_point).distance(
                    QgsGeometry.fromPointXY(point))
                if current_segment_distance > max_segment_len:
                    return None
                profiles_with_points_bind.get(profile_feats[(i + j) % 2].attribute('fid')).append(point)
                current_point = point
            extremum_func = min
        # Добавляем точку 6
        point = QgsPointXY(profile_points_list[0][0].x(), initial_point.y())
        segment_points.append(point)
        segment_attributes.append(1)
        current_segment_distance += QgsGeometry.fromPointXY(current_point).distance(QgsGeometry.fromPointXY(point))
        if current_segment_distance > max_segment_len:
            return None
        profiles_with_points_bind.get(profile_feats[0].attribute('fid')).append(point)
        current_point = point
        return segment_points, segment_attributes, current_segment_distance, \
            profiles_with_points_bind, current_point, 0

    def cut_segment_from_profiles(self, profiles_layer: QgsVectorLayer,
                                  profiles_dict: Dict[int, List[QgsPointXY]]) -> Tuple[List[QgsFeature], List[int]]:
        '''
        Служебная функция для удаления запланированного отрезка из профилей. Сама ничего не удаляет,
        только формирует новые профиля, которые получаются из разрезанного старого.
        :param profiles_layer: Слой с профилями.
        :param profiles_dict: словарь, где ключами являются ID профилей для резки, а значениями - список точек маршрута
        на этом профиле
        :return: возвращает список полученных после обрезки профилей и список ID профилей для удаления
        '''
        if self.cut_segment_debug:
            print("\n====begin cut segment======")
            print("input data:")
            print("profiles layer name to cut profiles: ", profiles_layer.name() if
            profiles_layer.isValid() else "layer invalid")
            print("profiles dict to cut: ", profiles_dict)
        output_feature_list = []
        remove_feats_id = []
        # Для каждого входного профиля в список будут добавлены 0, 1 или 2 профиля.
        for feature_fid in profiles_dict:
            request = QgsFeatureRequest(QgsExpression("fid = {}".format(feature_fid)))
            profile_feature = list(profiles_layer.getFeatures(request))
            if len(profile_feature) > 0:
                profile_feature = profile_feature[0]
            else:
                continue
            if self.cut_segment_debug:
                print("prof num to cut: ", profile_feature.attribute('prof_num'))
                print("prof num to cut geometry: ", profile_feature.geometry())
            fields = profile_feature.fields()
            attributes = profile_feature.attributes()
            x = profile_feature.geometry().asPolyline()[0].x()
            max_point_y = max([point.y() for point in profiles_dict.get(feature_fid)])
            min_point_y = min([point.y() for point in profiles_dict.get(feature_fid)])
            max_profile_y = max([point.y() for point in profile_feature.geometry().asPolyline()])
            min_profile_y = min([point.y() for point in profile_feature.geometry().asPolyline()])
            if min_point_y > min_profile_y:
                new_profile_geom = QgsGeometry.fromPolylineXY(
                    [QgsPointXY(x, min_profile_y), QgsPointXY(x, min_point_y)])
                new_feat = QgsFeature()
                new_feat.setFields(fields)
                new_feat.setAttributes(attributes)
                new_feat.setGeometry(new_profile_geom)
                output_feature_list.append(new_feat)
            if max_point_y < max_profile_y:
                new_profile_geom = QgsGeometry.fromPolylineXY(
                    [QgsPointXY(x, max_point_y), QgsPointXY(x, max_profile_y)])
                new_feat = QgsFeature()
                new_feat.setFields(fields)
                new_feat.setAttributes(attributes)
                new_feat.setGeometry(new_profile_geom)
                output_feature_list.append(new_feat)
            remove_feats_id.append(profile_feature.id())
        if self.cut_segment_debug:
            print("output_feature_list: ", [output_feature.attribute('prof_num') for output_feature
                                            in output_feature_list])
            print("output_feature_list geometries: ", [output_feature.geometry() for output_feature
                                                       in output_feature_list])
            print("feature id to remove", remove_feats_id)
            print("====end cut segment======\n")
        return output_feature_list, remove_feats_id

    def pack_to_layer(self, packing_features: List[QgsFeature]):
        """
        Сервисная функция упаковывающая список features во временный слой.
        :param packing_features: список QgsFeatures
        :return: QgsVectorLayer
        """
        geom_type = packing_features[0].geometry().wkbType()
        layer = QgsVectorLayer(QgsWkbTypes.displayString(geom_type),
                               'temp_layer',
                               'memory')
        layer.setCrs(self.profile_layer_crs)
        provider = layer.dataProvider()
        provider.addAttributes(packing_features[0].fields())
        layer.updateFields()
        provider.addFeatures(packing_features)
        provider.createSpatialIndex()
        layer.commitChanges()
        return layer

    def rotate_features(self, rotate_back_flag: bool = False) -> 'RoutePlanner':
        """
        Метод поворачивает все геометрии из self.output_pofiles на угол -profilese_azimuth, чтобы повернуть отбратно
        нужно вызвать метода с параметром rotate_back_flag=True, возвращает список QgsFeature
        :param rotate_back_flag: Флаг, False, чтобы повернуть геометрии вертикально или True чтобы вернуть обратно
        :type bool
        :return: self
        :rtype: RoutePlanner
        """
        if self.rotate_feats_debug:
            print("\n====call rotate_features=====")

        def rotate_features_list(feature_list: List[QgsFeature]):
            for feat in feature_list:
                if self.rotate_feats_debug:
                    print("feat before rotation: ", feat.geometry())
                geom = feat.geometry()
                geom.rotate(-1 * self.profiles_azimuth if not rotate_back_flag else self.profiles_azimuth,
                            self._current_takeoff_point_place)
                feat.setGeometry(geom)
                if self.rotate_feats_debug:
                    print("feat after rotation: ", feat.geometry())

        rotate_features_list(self.not_planned_profiles)
        rotate_features_list(self.planned_routes)
        if self.rotate_feats_debug:
            print("===end call rotate_features===\n")
        return self

    def scale_features(self, move_back_flag: bool = False) -> 'RoutePlanner':
        # Преобразую координаты к дециметрам, чтобы уйти от чисел с плавающей точкой к целым.
        self.max_service_flight_len = (self.max_service_flight_len * 10 if not move_back_flag else
                                       self.max_service_flight_len / 10)
        self.max_flight_len = (self.max_flight_len * 10 if not move_back_flag else
                               self.max_flight_len / 10)
        self.profiles_distance = (self.profiles_distance * 10 if not move_back_flag else
                                  self.profiles_distance / 10)

        def scale_qgs_line_string_feat(feature_list: List[QgsFeature]):
            for feat in feature_list:
                geom = feat.geometry()
                new_points = []
                for vertex in geom.vertices():
                    new_x = int(vertex.x() * 10) if not move_back_flag else vertex.x() / 10
                    new_y = int(vertex.y() * 10) if not move_back_flag else vertex.y() / 10
                    new_points.append(QgsPointXY(new_x, new_y))
                feat.setGeometry(QgsLineString(new_points))

        scale_qgs_line_string_feat(self.not_planned_profiles)
        scale_qgs_line_string_feat(self.planned_routes)
        return self

    def move_features(self, move_back_flag: bool = False) -> 'RoutePlanner':
        """
        Метод передвигает все геометрии на месте так, чтобы точка взлета была в начале координат
        :param move_back_flag: Параметр указывает куда двигаем False - в начало координат, True - обратно.
        :return: self
        :rtype: RoutePlanner
        """
        if self.move_feats_debug:
            print("\n====call move_features=====")
        self._current_takeoff_point_place = QgsPointXY(0, 0) if not move_back_flag \
            else self.takeoff_point_geometry.asPoint()

        def move_qgs_line_string_feat(feature_list: List[QgsFeature]):
            for feat in feature_list:
                if self.move_feats_debug:
                    print("before move line: ", feat.geometry())
                geom = feat.geometry()
                new_points = []

                for vertex in geom.vertices():
                    new_x = vertex.x() + (-1 * self.takeoff_point_geometry.asPoint().x() if not move_back_flag else
                                          self.takeoff_point_geometry.asPoint().x())
                    new_y = vertex.y() + (-1 * self.takeoff_point_geometry.asPoint().y() if not move_back_flag else
                                          self.takeoff_point_geometry.asPoint().y())

                    new_points.append(QgsPointXY(new_x, new_y))
                feat.setGeometry(QgsLineString(new_points))
                if self.move_feats_debug:
                    print("new line: ", feat.geometry())

        move_qgs_line_string_feat(self.not_planned_profiles)
        move_qgs_line_string_feat(self.planned_routes)
        if self.move_feats_debug:
            print("\n====END move_features=====")
        return self

    def initial_choose_profiles(self, filtering_profiles: List[QgsFeature]):
        """
        Первичный отбор профилей, над которыми будут проводится планирования полетов. Профиля отбираются по удаленности
        от точки взлета, меньшей, чем длина долета. Также в отбор включится крайне левый нечетный профиль, если долет
        меньше, чем длина долета + расстояние между профилями и крайне правый четный профиль, по тому же признаку.
        :return: filtered_features, chosen_profiles
        """
        # self.status_signal.emit('Making profile choose')
        filtered_features = []  # Профиля не вошедшие в отбор.
        chosen_profiles = []  # Профиля вошедшие в отбор.
        profiles_quantity = len(filtering_profiles)
        current_progress = 0
        if self.initial_choose_profiles_debug:
            print("\n===begin initial_choose_profiles===")
            print("go in initial_choose_profile: ")
            print("Current profiles quantity: ", len(filtering_profiles))
            print("Current max_service_flight_len: ", self.max_service_flight_len)
            print("Current takeoff point place: ", self._current_takeoff_point_place)
        for i, feat in enumerate(filtering_profiles):
            progress = int((i / profiles_quantity) * 100)
            if progress != current_progress:
                current_progress = progress
                # self.pecent_status_signal.emit(current_progress)
            profile_x_coord = list(feat.geometry().vertices())[0].x()
            profile_distance = feat.geometry().distance(QgsGeometry().fromPointXY(self._current_takeoff_point_place))
            profile_number = feat.attribute('prof_num')
            if self.initial_choose_profiles_debug:
                print("{} profile_num: {}, x coord: {}, distance: {}".format(i, profile_number,
                                                                             profile_x_coord, profile_distance))
            if profile_distance < self.max_service_flight_len:
                chosen_profiles.append(QgsFeature(feat))
            else:
                if (profile_distance < self.max_service_flight_len + self.profiles_distance) and \
                        (((profile_number % 2 == 0) and (profile_x_coord > 0)) or \
                         ((profile_number % 2 != 0) and (profile_x_coord < 0))):
                    # Проверяем на крайние профиля. Добавляем дополнительный нечетный слева и четный справа
                    chosen_profiles.append(QgsFeature(feat))
                else:
                    filtered_features.append(QgsFeature(feat))
        if self.initial_choose_profiles_debug:
            print("===end initial_choose_profiles===\n")
        return chosen_profiles, filtered_features

    def get_output_profiles(self):
        if self.selected_only_flag:
            not_selected_profiles_ids = [feature.id() for feature in self.input_profiles_layer.getFeatures()
                                         if feature.id() not in self.selected_features_ids]
            self.not_planned_profiles.extend(self.input_profiles_layer.getFeatures(not_selected_profiles_ids))
        new_fid = 1
        for feat in self.not_planned_profiles:
            if feat.fieldNameIndex('fid') > -1:
                feat.setAttribute('fid', new_fid)
            new_fid += 1
        return self.not_planned_profiles

    def get_temp_profiles(self):
        return self.temp_planning_profiles

    def get_planned_routes(self):
        return self.planned_routes
