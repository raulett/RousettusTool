import os

#Get filesystem path functions
def get_takeoff_points_filepath():
    return os.sep.join(['flights', 'takeoff_points.gpkg'])


def get_flight_profiles_filepath(method_name):
    return os.sep.join(['flights', method_name, 'survey_profiles.gpkg'])


def get_flight_routes_filepath(method_name):
    return os.sep.join(['flights', method_name, 'flight_routes.gpkg'])


#Qgis groupe hierarchy environment
def get_takeoff_points_group():
    return {'groups': ['flights'], 'layer_name': 'takeoff_points'}

def get_survey_profiles_group(method_name):
    return {'groups': ['flights', method_name, 'profiles'], 'layer_name': 'survey_profiles'}