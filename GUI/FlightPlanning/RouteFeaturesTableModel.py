import os
from typing import Dict, List, Any

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QColor
from qgis.core import QgsVectorLayer, QgsField


class RouteFeaturesTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.layer = None
        self._data = {}
        self._headers = ['Name', 'Profiles', 'Len']

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        column_name = self._headers[index.column()]
        if role == Qt.DisplayRole:
            if column_name == 'Name':
                return self._data[index.row()].attribute('name')
            elif column_name == 'Profiles':
                return self._data[index.row()].attribute('profiles')
            elif column_name == 'Len':
                return self._data[index.row()].attribute('length')
            else:
                return None
        if role == Qt.UserRole:
            return self._data[index.row()]
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            else:
                return section

    def set_layer(self, layer: QgsVectorLayer):
        self.beginResetModel()
        self.layer = layer
        fieldnames = [field.name() for field in self.layer.fields()]
        if (('name' in fieldnames) and ('service' in fieldnames)
                and ('length' in fieldnames) and ('profiles' in fieldnames)):
            self._data = [feature for feature in self.layer.getFeatures()]
        else:
            self._data = []
        self.endResetModel()

    def get_layer(self) -> QgsVectorLayer:
        return self.layer
