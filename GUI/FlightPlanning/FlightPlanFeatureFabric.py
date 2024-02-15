from qgis.core import QgsFields, QgsField, QgsFeature
from PyQt5.QtCore import QVariant


class FlightPlanFeatureFabric:
    flight_feats_fields = QgsFields()
    flight_feats_fields.append(QgsField('point_num', QVariant.Int))
    flight_feats_fields.append(QgsField('name', QVariant.String))
    flight_feats_fields.append(QgsField('lon', QVariant.Double))
    flight_feats_fields.append(QgsField('lat', QVariant.Double))
    flight_feats_fields.append(QgsField('alt', QVariant.Double))
    flight_feats_fields.append(QgsField('alt_asl', QVariant.Double))
    flight_feats_fields.append(QgsField('distance', QVariant.Double))
    flight_feats_fields.append(QgsField('route_name', QVariant.String))
    flight_feats_fields.append(QgsField('to_point', QVariant.String))
    flight_feats_fields.append(QgsField('is_service', QVariant.Int))

    @classmethod
    def get_flight_plan_feature(cls,
                                point_num: int,
                                name: str,
                                lon: float,
                                lat: float,
                                alt: float,
                                alt_asl: float,
                                distance: float,
                                to_point: str,
                                is_service: int) -> QgsFeature:
        feature = QgsFeature()
        feature.setFields(cls.flight_feats_fields)
        feature.setAttribute('point_num', point_num)
        feature.setAttribute('name', name)
        feature.setAttribute('lon', lon)
        feature.setAttribute('lat', lat)
        feature.setAttribute('alt', alt)
        feature.setAttribute('alt_asl', alt_asl)
        feature.setAttribute('distance', distance)
        feature.setAttribute('to_point', to_point)
        feature.setAttribute('is_service', is_service)
        return feature

    @classmethod
    def get_fields(cls):
        return cls.flight_feats_fields

