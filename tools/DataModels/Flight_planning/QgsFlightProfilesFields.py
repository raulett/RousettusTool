from qgis.core import QgsFields, QgsField
from PyQt5.QtCore import QVariant


class QgsFlightProfileFields(QgsFields):
    def __init__(self):
        super().__init__()
        self.append(QgsField('prof_num', QVariant.Int))
        self.append(QgsField('azimuth', QVariant.Double))
        self.append(QgsField('pr_dist', QVariant.Int))