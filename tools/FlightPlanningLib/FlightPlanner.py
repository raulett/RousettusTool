from ...tools.FlightPlanningLib.geometry_functions.qgs_get_distance import qgs_get_distance
from .geometry_functions.generate_linear_by_two_points import generate_linear_by_two_points

from ...libs.LinearSplineInterpolation.SplinesArray import SplinesArray

from qgis.core import QgsPointXY, QgsCoordinateReferenceSystem, QgsGeometry, QgsFeature, QgsFields, QgsRasterLayer, \
    QgsField
import math

from PyQt5.QtCore import QThread, pyqtSignal, QVariant

from typing import List, Tuple, Dict


class FlightPlanner(QThread):
    # multiline is list of tuples, represents points of multiline,
    # crs is str value, represents coordinate system in 'EPSG:X' format
    init_debug = 1
    general_algorithm_debug = 1

    def __init__(self, line_string: QgsFeature,
                 crs: QgsCoordinateReferenceSystem,
                 dem_layer: QgsRasterLayer,
                 dem_layer_band: int,
                 flight_altitude: int,
                 up_deviation: float,
                 down_deviation: float,
                 takeoff_and_landing_point_altitude: float,
                 regular_points_dist: int = None,
                 alt_above_takeoff_point: int = None):
        if self.init_debug:
            print("\n===begin init===")
            print("input line string: ", line_string)
        super(QThread).__init__()
        self.input_route_feature = line_string
        self.alt_above_takeoff_point = alt_above_takeoff_point
        self.takeoff_and_landing_point_altitude = takeoff_and_landing_point_altitude
        self.alt_deviation_limit = (up_deviation, down_deviation)
        self.flight_alt_agl = flight_altitude
        self.service_flight_flags_list = None
        self.dem_layer = dem_layer.clone()
        self.dem_layer_band = dem_layer_band
        self.input_multiline = []
        self.flight_points = []
        self.crs_str = crs
        self.dem_crs = dem_layer.crs()
        # check if need to reproject dem raster

        self.get_distance_function = qgs_get_distance
        self.input_points = []
        self.is_service_vector = [int(flag) for flag in line_string.attribute('service').split(';')]
        for i, point in enumerate(line_string.geometry().asPolyline()):
            if i == 0:
                self.input_points.append({'point': point, 'distance': 0, "is_service": 0})
            else:
                self.input_points.append({'point': point,
                                          'distance': self.input_points[i - 1]['distance'] +
                                                      self.input_points[i - 1]['point'].distance(point),
                                          "is_service": self.is_service_vector[i - 1]})
        if self.init_debug:
            print("generated init points: ", self.input_points)
        self.multiline_length = None
        self.distance_x_splines = None
        self.distance_y_splines = None
        self.dist_altitude_points = None
        self.dist_alt_splines = None
        self.dist_to_alt_ground_function = None
        self.alt_points = []
        self.flight_feats_fields = QgsFields()
        self.flight_feats_fields.append(QgsField('fid', QVariant.Int))
        self.flight_feats_fields.append(QgsField('point_num', QVariant.Int))
        self.flight_feats_fields.append(QgsField('flight_name', QVariant.String))
        self.flight_feats_fields.append(QgsField('alt', QVariant.Double))
        self.flight_feats_fields.append(QgsField('alt_asl', QVariant.Double))
        self.flight_feats_fields.append(QgsField('distance', QVariant.Double))
        self.flight_feats_fields.append(QgsField('route_name', QVariant.String))
        if self.init_debug:
            print("===end init===\n")

    def general_algorithm(self):
        if self.general_algorithm_debug:
            print("\n===begin general_algorithm_debug===")
        self.make_dist_to_x_func().make_dist_to_y_func()
        self.init_altitude_points(self.dem_layer, self.dem_layer_band)
        if self.general_algorithm_debug:
            print("dist alt function: ", self.alt_points)
        self.make_dist_to_ground_alt_function()
        self.make_initial_flight_plan()
        self.make_flight_plan()
        if self.general_algorithm_debug:
            print("===end general_algorithm_debug===\n")

    def make_dist_to_x_func(self):
        '''
        Служебная функция, создающая кусочно заданную функцию из расстояния в x координату.
        :return: self
        '''
        self.distance_x_splines = SplinesArray()
        dist_x_table = [(point['distance'], point['point'].x()) for point in self.input_points]
        self.distance_x_splines.add_spline(dist_x_table)
        return self

    def make_dist_to_y_func(self):
        '''
        Служебная функция, создающая кусочно заданную функцию из расстояния в y координату.
        :return: self
        '''
        self.distance_y_splines = SplinesArray()
        dist_y_table = [(point['distance'], point['point'].y()) for point in self.input_points]
        self.distance_y_splines.add_spline(dist_y_table)
        return self

    # Making (distance, altitude) points table by input raster layer dem/dsm data,
    # returns number of points where there was no alt values
    def init_altitude_points(self, raster_layer: QgsRasterLayer, band: int = 1, dem_resolution: float = None) -> int:
        '''
        Служебная функция инициализирующая список точек (дистанция, высота)
        :param raster_layer:
        :param band:
        :param dem_resolution:
        :return:
        '''
        min_resolution = min(self.dem_layer.rasterUnitsPerPixelX(), raster_layer.rasterUnitsPerPixelY())
        if dem_resolution is None:
            distance_d = min_resolution
        else:
            distance_d = dem_resolution if dem_resolution > min_resolution else min_resolution
        no_value_errors_count = 0
        data_provider = raster_layer.dataProvider()
        for i, point in enumerate(self.input_points):
            if i == 0:
                continue
            curr_distance = self.input_points[i - 1]['distance']
            alt_value, is_exist = data_provider.sample(self.input_points[i - 1]['point'], band)
            if is_exist:
                self.alt_points.append((self.input_points[i - 1]['distance'], alt_value))
            else:
                no_value_errors_count += 1
            curr_distance += distance_d
            while (point.get('distance') - curr_distance) > distance_d:
                got_point = self.get_point_coord_from_dist(curr_distance)
                alt_value, is_exist = data_provider.sample(got_point, band)
                if is_exist:
                    self.alt_points.append((curr_distance, alt_value))
                else:
                    no_value_errors_count += 1
                curr_distance += distance_d
        got_point = self.input_points[len(self.input_points) - 1]['point']
        alt_value, is_exist = data_provider.sample(got_point, band)
        if is_exist:
            self.alt_points.append((self.input_points[len(self.input_points) - 1]['distance'], alt_value))
        else:
            no_value_errors_count += 1
        return no_value_errors_count

    def make_dist_to_ground_alt_function(self):
        self.dist_to_alt_ground_function = SplinesArray()
        self.dist_to_alt_ground_function.add_spline(self.alt_points)

    def get_altitude(self, distance: float):
        return self.dist_to_alt_ground_function.get_value(distance)

    def get_altitude_points_list(self):
        return self.alt_points

    def get_turning_points(self):
        return self.input_multiline

    def get_crs_str(self):
        return self.crs_str

    def set_service_flight_flags(self, flags_list: list):
        self.service_flight_flags_list = flags_list
        return self

    def set_flight_altitude(self, flight_altitude: float):
        self.flight_alt_agl = flight_altitude
        return self

    def set_alt_deviation(self, up_deviation: float, down_deviation: float):
        self.alt_deviation_limit = (up_deviation, down_deviation)
        return self

    def set_takeoff_and_landing_point_altitude(self, to_point_alt: float):
        self.takeoff_and_landing_point_altitude = to_point_alt
        return self

    def set_takeoff_point_alt_from_first_point(self):
        self.takeoff_and_landing_point_altitude = self.alt_points[0][1]
        return self

    def set_flight_alt_above_to_point(self, to_point_flight_alt: float):
        self.alt_above_takeoff_point = to_point_flight_alt
        return self

    def make_initial_flight_plan(self):
        for i, route_point in enumerate(self.input_points):
            if i == 0:
                flight_point = dict(distance=route_point['distance'],
                                    gnd_alt=self.get_altitude(route_point['distance']),
                                    is_service_flag=route_point["is_service"],
                                    k_alt_coef=0,
                                    b_alt_coef=0,
                                    flight_alt=self.alt_above_takeoff_point \
                                        if self.alt_above_takeoff_point is not None \
                                        else self.flight_alt_agl,
                                    prepared_flag=1,
                                    is_corner_point_flag=1)
                self.flight_points.append(flight_point)
            else:
                k_alt_coef, b_alt_coef = generate_linear_by_two_points((self.input_points[i - 1]['distance'],
                                                                        self.get_altitude(
                                                                            self.input_points[i - 1]['distance'])),
                                                                       (route_point['distance'],
                                                                        self.get_altitude(route_point['distance'])))
                flight_point = dict(distance=route_point['distance'],
                                    gnd_alt=self.get_altitude(route_point['distance']),
                                    is_service_flag=route_point["is_service"],
                                    k_alt_coef=k_alt_coef,
                                    b_alt_coef=b_alt_coef,
                                    flight_alt=self.flight_alt_agl,
                                    prepared_flag=0,
                                    is_corner_point_flag=1)
                self.flight_points.append(flight_point)
        return self

    def make_regular_flight_plan(self, point_distance):
        new_flight_plan = []
        current_distance = 0
        prev_point = None
        for i, flight_point in enumerate(self.flight_points):
            if i == 0:
                new_flight_point = dict(distance=current_distance,
                                        gnd_alt=self.get_altitude(current_distance),
                                        is_service_flag=0,
                                        k_alt_coef=0,
                                        b_alt_coef=0,
                                        flight_alt=self.flight_alt_agl,
                                        prepared_flag=1,
                                        is_corner_point_flag=1)
                new_flight_plan.append(new_flight_point)
                current_distance += point_distance
                prev_point = new_flight_point
            else:
                while current_distance <= flight_point['distance'] - point_distance:
                    flight_g_alt = self.get_altitude(current_distance)
                    k_alt_coef, b_alt_coef = generate_linear_by_two_points((prev_point['distance'],
                                                                            self.get_altitude(
                                                                                prev_point['distance'])),
                                                                           (current_distance, flight_g_alt))
                    new_flight_point = dict(distance=current_distance,
                                            gnd_alt=self.get_altitude(current_distance),
                                            is_service_flag=flight_point['is_service_flag'],
                                            k_alt_coef=k_alt_coef,
                                            b_alt_coef=b_alt_coef,
                                            flight_alt=self.flight_alt_agl,
                                            prepared_flag=1,
                                            is_corner_point_flag=1)
                    prev_point = new_flight_point
                    new_flight_plan.append(new_flight_point)
                    current_distance += point_distance
                current_distance = flight_point['distance']
                flight_g_alt = self.get_altitude(current_distance)
                k_alt_coef, b_alt_coef = generate_linear_by_two_points((prev_point['distance'],
                                                                        self.get_altitude(
                                                                            prev_point['distance'])),
                                                                       (current_distance, flight_g_alt))
                new_flight_point = dict(distance=current_distance,
                                        gnd_alt=flight_g_alt,
                                        is_service_flag=flight_point['is_service_flag'],
                                        k_alt_coef=k_alt_coef,
                                        b_alt_coef=b_alt_coef,
                                        flight_alt=self.flight_alt_agl,
                                        prepared_flag=1,
                                        is_corner_point_flag=1)
                prev_point = new_flight_point
                new_flight_plan.append(new_flight_point)
                current_distance += point_distance
        self.flight_points = new_flight_plan

    def make_flight_plan(self):
        # print('call make flight plan')
        all_prepared_flag = 0
        while all_prepared_flag == 0:
            all_prepared_flag = 1
            for i, flight_point in enumerate(self.flight_points):
                # print('execute for cycle')
                if flight_point['prepared_flag'] == 0:
                    all_prepared_flag = 0
                    self.flight_points[i - 1: i + 1] = self.add_mid_flight_point_alternative(self.flight_points[i - 1],
                                                                                             self.flight_points[i])
                    # print('New points: ', self.flight_points[i - 1], '; ', self.flight_points[i])
                    # print('Renew flight points count', len(self.flight_points))
                    # time.sleep(1)
                    break
            # print('all prepared flag: ', all_prepared_flag)
            # print('flight points: ', [(i, point['distance'], point['gnd_alt']) for i, point in
            #                                enumerate(self.get_flight_points())])
        # print('make flight plan, finish while')
        return self

    def add_mid_flight_point_alternative(self, first_f_point: Dict, sec_f_point: Dict):
        max_up_deviation_point_distance = None
        max_down_deviation_point_distance = None
        max_up_deviation_value = 0
        max_down_deviation_value = 0
        current_distance = first_f_point['distance']
        d_distance = min(self.dem_layer.rasterUnitsPerPixelX(), self.dem_layer.rasterUnitsPerPixelY())
        while current_distance < sec_f_point['distance']:
            gnd_alt = self.get_altitude(current_distance)
            flight_g_alt = sec_f_point['k_alt_coef'] * current_distance + sec_f_point['b_alt_coef']
            current_deviation = flight_g_alt - gnd_alt
            if current_deviation > max_up_deviation_value:
                max_up_deviation_value = current_deviation
                max_up_deviation_point_distance = current_distance
            if current_deviation < max_down_deviation_value:
                max_down_deviation_value = current_deviation
                max_down_deviation_point_distance = current_distance
            current_distance = current_distance + d_distance
        if (max_down_deviation_value < self.alt_deviation_limit[1]) and max_down_deviation_value is not None:
            flight_g_alt = self.get_altitude(max_down_deviation_point_distance)
            k_alt_coef, b_alt_coef = generate_linear_by_two_points((first_f_point['distance'],
                                                                    first_f_point['gnd_alt']),
                                                                   (max_down_deviation_point_distance,
                                                                    flight_g_alt))
            new_mid_flight_point = dict(distance=max_down_deviation_point_distance,
                                        gnd_alt=flight_g_alt,
                                        is_service_flag=sec_f_point['is_service_flag'],
                                        k_alt_coef=k_alt_coef,
                                        b_alt_coef=b_alt_coef,
                                        flight_alt=sec_f_point['flight_alt'],
                                        prepared_flag=0,
                                        is_corner_point_flag=0)
            k_alt_coef, b_alt_coef = generate_linear_by_two_points((new_mid_flight_point['distance'],
                                                                    new_mid_flight_point['gnd_alt']),
                                                                   (sec_f_point['distance'],
                                                                    sec_f_point['gnd_alt']))
            sec_f_point['k_alt_coef'] = k_alt_coef
            sec_f_point['b_alt_coef'] = b_alt_coef
            return [first_f_point, new_mid_flight_point, sec_f_point]
        elif (max_up_deviation_value > self.alt_deviation_limit[0]) \
                and (sec_f_point['is_service_flag'] == 1) \
                and (max_up_deviation_value is not None):
            flight_g_alt = self.get_altitude(max_up_deviation_point_distance)
            k_alt_coef, b_alt_coef = generate_linear_by_two_points((first_f_point['distance'],
                                                                    first_f_point['gnd_alt']),
                                                                   (max_up_deviation_point_distance,
                                                                    flight_g_alt))
            new_mid_flight_point = dict(distance=max_up_deviation_point_distance,
                                        gnd_alt=flight_g_alt,
                                        is_service_flag=sec_f_point['is_service_flag'],
                                        k_alt_coef=k_alt_coef,
                                        b_alt_coef=b_alt_coef,
                                        flight_alt=sec_f_point['flight_alt'],
                                        prepared_flag=0,
                                        is_corner_point_flag=0)
            k_alt_coef, b_alt_coef = generate_linear_by_two_points((new_mid_flight_point['distance'],
                                                                    new_mid_flight_point['gnd_alt']),
                                                                   (sec_f_point['distance'],
                                                                    sec_f_point['gnd_alt']))
            sec_f_point['k_alt_coef'] = k_alt_coef
            sec_f_point['b_alt_coef'] = b_alt_coef
            return [first_f_point, new_mid_flight_point, sec_f_point]
        else:
            sec_f_point['prepared_flag'] = 1
            return [first_f_point, sec_f_point]

    def add_mid_flight_point(self, first_f_point, sec_f_point):
        max_deviation_point_index = None
        max_deviation_value = 0
        # alt_points = [point for point in self.alt_points if
        #               first_f_point['distance'] <= point[0] <= sec_f_point['distance']]
        for index, alt_point in enumerate(self.alt_points):
            if first_f_point['distance'] <= alt_point[0] <= sec_f_point['distance']:
                flight_g_alt = sec_f_point['k_alt_coef'] * alt_point[0] + sec_f_point['b_alt_coef']
                current_alt_deviation = flight_g_alt - alt_point[1]
                if abs(current_alt_deviation) > abs(max_deviation_value):
                    max_deviation_value = current_alt_deviation
                    max_deviation_point_index = index
        if (max_deviation_value < self.alt_deviation_limit[1]) and (max_deviation_point_index is not None):
            flight_g_alt = self.get_altitude(self.alt_points[max_deviation_point_index][0])
            k_alt_coef, b_alt_coef = generate_linear_by_two_points((first_f_point['distance'],
                                                                    self.get_altitude(first_f_point['distance'])),
                                                                   (self.alt_points[max_deviation_point_index][0],
                                                                    flight_g_alt))
            new_mid_flight_point = dict(distance=self.alt_points[max_deviation_point_index][0],
                                        gnd_alt=self.alt_points[max_deviation_point_index][1],
                                        is_service_flag=sec_f_point['is_service_flag'],
                                        k_alt_coef=k_alt_coef,
                                        b_alt_coef=b_alt_coef,
                                        flight_alt=sec_f_point['flight_alt'],
                                        prepared_flag=0,
                                        is_corner_point_flag=0)
            k_alt_coef, b_alt_coef = generate_linear_by_two_points((new_mid_flight_point['distance'],
                                                                    self.get_altitude(
                                                                        new_mid_flight_point['distance'])),
                                                                   (sec_f_point['distance'],
                                                                    self.get_altitude(sec_f_point['distance'])))
            sec_f_point['k_alt_coef'] = k_alt_coef
            sec_f_point['b_alt_coef'] = b_alt_coef
            return [first_f_point, new_mid_flight_point, sec_f_point]
        elif (max_deviation_value > self.alt_deviation_limit[0]) \
                and (sec_f_point['is_service_flag'] == 1) \
                and (max_deviation_point_index is not None):
            flight_g_alt = self.get_altitude(self.alt_points[max_deviation_point_index][0])
            k_alt_coef, b_alt_coef = generate_linear_by_two_points((first_f_point['distance'],
                                                                    self.get_altitude(first_f_point['distance'])),
                                                                   (self.alt_points[max_deviation_point_index][0],
                                                                    flight_g_alt))
            new_mid_flight_point = dict(distance=self.alt_points[max_deviation_point_index][0],
                                        gnd_alt=self.alt_points[max_deviation_point_index][1],
                                        is_service_flag=sec_f_point['is_service_flag'],
                                        k_alt_coef=k_alt_coef,
                                        b_alt_coef=b_alt_coef,
                                        flight_alt=sec_f_point['flight_alt'],
                                        prepared_flag=0,
                                        is_corner_point_flag=0)
            k_alt_coef, b_alt_coef = generate_linear_by_two_points((new_mid_flight_point['distance'],
                                                                    self.get_altitude(
                                                                        new_mid_flight_point['distance'])),
                                                                   (sec_f_point['distance'],
                                                                    self.get_altitude(sec_f_point['distance'])))
            sec_f_point['k_alt_coef'] = k_alt_coef
            sec_f_point['b_alt_coef'] = b_alt_coef
            return [first_f_point, new_mid_flight_point, sec_f_point]
        else:
            sec_f_point['prepared_flag'] = 1
            return [first_f_point, sec_f_point]

    # getters
    def get_point_coord_from_dist(self, dist: float) -> QgsPointXY:
        x = self.distance_x_splines.get_value(dist)
        y = self.distance_y_splines.get_value(dist)
        return QgsPointXY(x, y)

    def get_flight_alt(self):
        return self.flight_alt_agl

    def get_alt_deviation(self):
        return self.alt_deviation_limit

    def get_takeoff_point_alt(self):
        return self.takeoff_and_landing_point_altitude

    def get_to_point_flight_alt(self):
        return self.alt_above_takeoff_point

    def get_flight_points(self):
        return self.flight_points

    def get_flight(self) -> List[QgsFeature]:
        flight_feature_list = []
        fid_num = 0
        for flight_point in self.flight_points:
            feat = QgsFeature()
            feat.setFields(self.flight_feats_fields)
            feat.setGeometry(QgsGeometry.fromPointXY(self.get_point_coord_from_dist(flight_point['distance'])))
            feat.setAttribute('fid', fid_num)
            feat.setAttribute('point_num', fid_num)
            feat.setAttribute('flight_name', self.input_route_feature.attribute('name'))
            feat.setAttribute('alt', (flight_point['gnd_alt'] + flight_point['flight_alt']) -
                              self.takeoff_and_landing_point_altitude)
            feat.setAttribute('alt_asl', flight_point['gnd_alt'] + flight_point['flight_alt'])
            feat.setAttribute('distance', flight_point['distance'])
            feat.setAttribute('route_name', self.input_route_feature.attribute('name'))
            fid_num += 1
            flight_feature_list.append(feat)
        return flight_feature_list

    def get_flight_metrics(self):
        result = {}
        standart_dev_list = []
        points_count = len(self.flight_points)
        current_fp = 1
        tot_lenght = self.alt_points[len(self.alt_points) - 1][0]
        tot_climb = 0
        tot_desc = 0
        prev_alt = None
        max_delta = 0
        min_delta = 0
        for alt_point in self.alt_points:
            # print(alt_point)
            if alt_point[0] > self.flight_points[current_fp]['distance']:
                current_fp += 1
            else:
                if self.flight_points[current_fp]['is_service_flag'] == 0:
                    continue
                delta = (self.flight_points[current_fp]['k_alt_coef'] * alt_point[0] +
                         self.flight_points[current_fp]['b_alt_coef']) - alt_point[1]
                if delta > max_delta:
                    max_delta = delta
                if delta < min_delta:
                    min_delta = delta
                std_dev_in_point = math.sqrt(((self.flight_points[current_fp]['k_alt_coef'] * alt_point[0] +
                                               self.flight_points[current_fp]['b_alt_coef']) - alt_point[1]) ** 2)
                standart_dev_list.append(std_dev_in_point)
        result['max_delta'] = max_delta
        result['min_delta'] = min_delta
        result['average_SD'] = sum(standart_dev_list) / len(standart_dev_list)
        result['points_count'] = points_count
        result['tot_lenght'] = tot_lenght
        for i, flight_point in enumerate(self.flight_points):
            if i == 0:
                prev_alt = flight_point['gnd_alt']
            alt_delta = flight_point['gnd_alt'] - prev_alt
            if alt_delta > 0:
                tot_climb += alt_delta
            elif alt_delta < 0:
                tot_desc += alt_delta
            prev_alt = flight_point['gnd_alt']
        result['tot_climb'] = tot_climb
        result['tot_desc'] = tot_desc
        return result
