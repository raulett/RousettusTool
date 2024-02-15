from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, pyqtSignal
from qgis.core import QgsLayerTreeGroup, QgsVectorLayer, Qgis


class LayerListModel(QAbstractListModel):
    """
    Модель данных представляющая список слоев содержащих спланированные маршруты
    """
    layers_reset_sgn = pyqtSignal()

    def __init__(self, geometry_type: Qgis.GeometryType) -> None:
        super(LayerListModel, self).__init__()
        self._data = []
        self.geometry_type = geometry_type
        self._data.sort(key=lambda layer: layer.name())

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()].name()
        if role == Qt.UserRole:
            return self._data[index.row()]
        return None

    def set_layer_group(self, layer_group: QgsLayerTreeGroup or None) -> None:
        self.beginResetModel()
        self.layer_group = layer_group
        self._data = [layer.layer() for layer in self.layer_group.findLayers()
                      if (isinstance(layer.layer(), QgsVectorLayer)
                          and layer.layer().geometryType() is self.geometry_type)] if self.layer_group else []
        self._data.sort(key=lambda layer: layer.name())
        self.endResetModel()
        self.layers_reset_sgn.emit()