from ...tools.FlightPlanningLib.geometry_functions.qgs_get_distance import qgs_get_distance

from ...libs.LinearSplineInterpolation.SplinesArray import SplinesArray

from qgis.core import QgsPointXY

''' Usage protocol:
- init object with list of points in form of tuple(float, float) and crs in form str('EPSG:X')
- Make dist to x and dist to y functions, calling make_dist_to_x_func(), and make_dist_to_y_func()
- add altitude, calling qgs_set_altitude_points(raster_layer, band: int), with raster layer, and band
- Make dist to alt linear function, calling make_dist_to_alt_finction().
'''


class FlightRoute:
    # multiline is list of tuples, represents points of multiline,
    # crs is str value, represents coordinate system in 'EPSG:X' format
    def __init__(self, multiline, crs):
        self.alt_points = None
        self.input_multiline = []

        # init external functions
        self.get_distance_function = qgs_get_distance
        self.input_multiline.append((multiline[0][0], multiline[0][1], 0))
        for i in range(1, len(multiline)):
            self.input_multiline.append((multiline[i][0],
                                         multiline[i][1],
                                         self.input_multiline[i - 1][2] +
                                         self.get_distance_function(multiline[i - 1], multiline[i], crs)))

        if 1:
            print('flight route input multiline: ', self.input_multiline)

        self.multiline = None
        self.multiline_lenght = None
        self.distance_x_splines = None
        self.distance_y_splines = None
        self.dist_altitude_points = None
        self.dist_alt_splines = None

    def get_turning_points(self):
        return self.input_multiline

    def make_dist_to_x_func(self):
        self.distance_x_splines = SplinesArray()
        dist_x_table = [(point[2], point[0]) for point in self.input_multiline]
        print('dist x table: ', dist_x_table)
        self.distance_x_splines.add_spline(dist_x_table)
        return self

    def make_dist_to_y_func(self):
        self.distance_y_splines = SplinesArray()
        self.distance_y_splines.add_spline([(point[2], point[1]) for point in self.input_multiline])
        return self

    def get_coord_from_dist(self, dist: float):
        x = self.distance_x_splines.get_value(dist)
        y = self.distance_y_splines.get_value(dist)
        return x, y

    # Making (distance, altitude) points table by input raster layer dem/dsm data,
    # returns number of points where there was no alt values
    def qgs_set_altitude_points(self, raster_layer, band=1):
        distance_d = min(raster_layer.rasterUnitsPerPixelX(), raster_layer.rasterUnitsPerPixelX())
        no_value_errors_count = 0
        self.alt_points = []
        data_provider = raster_layer.dataProvider()
        for i in range(1, len(self.input_multiline)):
            curr_distance = self.input_multiline[i - 1][2]
            print('current distance: ', curr_distance)
            point = QgsPointXY(self.input_multiline[i - 1][0], self.input_multiline[i - 1][1])
            alt_value, is_exist = data_provider.sample(point, band)
            if is_exist:
                self.alt_points.append((self.input_multiline[i - 1][2], alt_value))
            else:
                no_value_errors_count += 1
            curr_distance += distance_d
            while ((self.input_multiline[i][2] - curr_distance) > distance_d):
                point_tuple = self.get_coord_from_dist(curr_distance)
                point = QgsPointXY(point_tuple[0], point_tuple[1])
                alt_value, is_exist = data_provider.sample(point, band)
                if is_exist:
                    self.alt_points.append((curr_distance, alt_value))
                else:
                    no_value_errors_count += 1
                curr_distance += distance_d
        point = QgsPointXY(self.input_multiline[len(self.input_multiline) - 1][0],
                           self.input_multiline[len(self.input_multiline) - 1][1])
        alt_value, is_exist = data_provider.sample(point, band)
        if is_exist:
            self.alt_points.append((self.input_multiline[len(self.input_multiline) - 1][2], alt_value))
        else:
            no_value_errors_count += 1
        return no_value_errors_count

    def make_dist_to_alt_finction(self):
        self.dist_to_alt_ground_function = SplinesArray()
        self.dist_to_alt_ground_function.add_spline(self.alt_points)

    def get_altitude(self, distance: float):
        return self.dist_to_alt_ground_function.get_value(distance)

    def get_altitude_points_list(self):
        return self.alt_points
