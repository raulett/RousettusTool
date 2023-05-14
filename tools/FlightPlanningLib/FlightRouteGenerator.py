from qgis.core import QgsVectorLayer, QgsPoint, QgsCoordinateReferenceSystem

'''
Содержит логику планирования полетных путей (ЛПП).
Принимает на вход слой с разведочными профилями.
После цикла генерации, возвращает слой с профилями, над которыми небыли сгенерированы ДПП.
'''


class FlightRouteGenerator:
    '''
    @:param survey_profiles_layer QgisVectorLayer object, with prof_num, azimuth, pr_dist attributes.
    crs must be metric
    prof_num - profiles have to be enumerate.
    azimuth - azimuth of profiles
    @:param takeoff_point - sould have the same crs as survey profile layer
    @:param dist_limit - maximum flight route lenght.
    @:param service_dist_limit - maximum distance from takeoff point to profile
    '''

    def __init__(self, survey_profiles_layer: QgsVectorLayer,
                 takeoff_point: QgsPoint,
                 point_crs: QgsCoordinateReferenceSystem,
                 dist_limit: int,
                 service_dist_limit: int):
        self.source_profile_layer = survey_profiles_layer
        self.takeoff_point = takeoff_point
        self.point_crs = point_crs
        self.dist_limit = dist_limit
        self.service_dist_limit = service_dist_limit

    def a(self):
        print('test a')

    def b(self):
        print('test b')

    def show_mpl(self):
        pass
