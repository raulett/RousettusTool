from .FlightRoute import FlightRoute
from .geometry_functions.generate_linear_by_two_points import generate_linear_by_two_points
# import pydevd_pycharm
import time

''' Usage protocol:
- init FlightRoute object.
add flight information, prepare to generate
- set_service_flight_flags(flags_list: list) add service flight flags
- set_alt_deviation(up_deviation: float, down_deviation: float), add altitude deviation parameters
- set_flight_altitude(flight_altitude: float)
- set_takeoff_and_landing_point_altitude(to_point_alt: float) or set_takeoff_point_alt_from_first_point() set

- make_initial_flight_plan() - init flight plan by base points
'''


class FlightPlan(FlightRoute):
    def __init__(self, multiline, crs):
        super().__init__(multiline, crs)
        self.flight_points = None
        self.flight_alt_agl = None
        self.alt_deviation_limit = None
        self.takeoff_and_landing_point_altitude = None
        self.alt_above_takeoff_point = None
        self.service_flight_flags_list = None

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
        first_iteration_done = 0
        self.flight_points = []
        for i, route_point in enumerate(self.input_multiline):
            if first_iteration_done == 0:
                flight_point = dict(distance=route_point[2],
                                    gnd_alt=self.get_altitude(route_point[2]),
                                    is_service_flag=0,
                                    k_alt_coef=0,
                                    b_alt_coef=0,
                                    flight_alt=self.alt_above_takeoff_point \
                                        if self.alt_above_takeoff_point is not None \
                                        else self.flight_alt_agl,
                                    prepared_flag=1,
                                    is_corner_point_flag=1)
                self.flight_points.append(flight_point)
                first_iteration_done = 1
            else:
                k_alt_coef, b_alt_coef = generate_linear_by_two_points((self.input_multiline[i-1][2],
                                                                     self.get_altitude(self.input_multiline[i-1][2])),
                                                                    (route_point[2],
                                                                     self.get_altitude(route_point[2])))
                flight_point = dict(distance=route_point[2],
                                    gnd_alt=self.get_altitude(route_point[2]),
                                    is_service_flag=self.service_flight_flags_list[i-1],
                                    k_alt_coef=k_alt_coef,
                                    b_alt_coef=b_alt_coef,
                                    flight_alt=self.flight_alt_agl,
                                    prepared_flag=0,
                                    is_corner_point_flag=1)
                self.flight_points.append(flight_point)
        return self

    def make_flight_plan(self):
        # print('call make flight plan')
        all_prepared_flag = 0
        # pydevd_pycharm.settrace('localhost', port=5566, stdoutToServer=True, stderrToServer=True)
        while all_prepared_flag == 0:
            all_prepared_flag = 1
            for i, flight_point in enumerate(self.flight_points):
                # print('execute for cycle')
                if flight_point['prepared_flag'] == 0:
                    all_prepared_flag = 0
                    self.flight_points[i-1: i+1] = self.add_mid_flight_point(self.flight_points[i-1],
                                                                             self.flight_points[i])
                    # print('New points: ', self.flight_points[i - 1], '; ', self.flight_points[i])
                    # print('Renew flight points count', len(self.flight_points))
                    time.sleep(1)
                    break
            # print('all prepared flag: ', all_prepared_flag)
            # print('flight points: ', [(i, point['distance'], point['gnd_alt']) for i, point in
            #                                enumerate(self.get_flight_points())])
        # print('make flight plan, finish while')
        return self

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
