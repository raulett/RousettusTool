from qgis.core import QgsFeature
from QgsFlightProfilesFields import QgsFlightProfileFields


class QgsFlightProfileFeature(QgsFeature):
    def __init__(self):
        super().__init__()
        self.setFields(QgsFlightProfileFields())