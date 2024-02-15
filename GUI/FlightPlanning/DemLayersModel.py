from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from qgis.core import Qgis, QgsProject, QgsRasterLayer


class DemLayersModel(QAbstractListModel):
    def __init__(self) -> None:
        super().__init__()
        self._data = []
        QgsProject.instance().layersRemoved.connect(self.init_project_layers)
        QgsProject.instance().layersAdded.connect(self.init_project_layers)
        QgsProject.instance().layerTreeRoot().visibilityChanged.connect(self.init_project_layers)
        self.init_project_layers()

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()].name()
        if role == Qt.UserRole:
            return self._data[index.row()]
        return None

    def init_project_layers(self):
        self.beginResetModel()
        self._data = []
        for layer in [layer for layer in QgsProject.instance().layerTreeRoot().checkedLayers()
                      if isinstance(layer, QgsRasterLayer)]:
            print(layer.name())
            if layer.isValid():
                self._data.append(layer)
        self._data.sort(key=lambda raster_layer: raster_layer.name())
        self.endResetModel()
