from datetime import datetime

from PyQt5.QtGui import QPixmap

# icons
in_progress_pixmap = QPixmap(":/plugins/RousettusTool/resources/inprogress_icon.png").scaled(12, 12)
done_pixmap = QPixmap(":/plugins/RousettusTool/resources/positive_icon.png").scaled(12, 12)

# datetime format project constants
datetime_format = '%Y-%m-%dT%H:%M:%S,%f'
default_datetime = datetime(1900, 1, 1).strftime(datetime_format)

# general data
geometry_types = {'Point': 'Point', 'PointZ': 'PointZ', 'LineString': 'LineString', 'Polygon': 'Polygon'}

# general data group path
data_group_path = ['data']

# GPS layer groups and filepath constants.
gps_group_path = data_group_path[:] + ['gps']
gps_layer_name = 'gps_data'
gps_filepath = ['data']
gps_filename = 'gps_data'

# Routes flights and profiles layer groups and filepath constants.
flights_group_path = ['flights']
flights_filepath = ['flights']


def get_routes_group_path(method_name: str):
    return flights_group_path + [method_name] + ['routes']


def get_routes_file_path(method_name: str):
    return flights_filepath + [method_name] + ['flight_routes.gpkg']


def get_flight_group_path(method_name: str) -> list:
    return flights_group_path + [method_name] + ['flight_plans']


def get_flight_file_path(method_name: str):
    return flights_filepath + [method_name] + ['flight_plans.gpkg']


