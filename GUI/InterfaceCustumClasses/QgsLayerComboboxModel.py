from PyQt5.QtCore import QAbstractListModel, QModelIndex
from qgis.core import QgsLayerTree, QgsWkbTypes





class QgsLayerComboboxModel(QAbstractListModel):
    # TODO Сделать перевод.
    """
    Класс представляющий модель слоев, отфильтрованных по заданным условиям для отображения в QComboBox.

    Methods
    ____
    set_visibility(bool) - Устанавливает фильтр, "только видимые", по умолчанию True
    """
    def __init__(self, layers_group: QgsLayerTree, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layers_geometry_type = None
        self.show_visible_only_flag = True
        self.layer_tree_list = []

    def set_visibility(self, show_visible_only_flag :bool):
        self.show_visible_only_flag = show_visible_only_flag
        return self

    def set_geometry_type(self, geometry_type: QgsWkbTypes.WkbType):
        self.layers_geometry_type = geometry_type
        return self

    def rowCount(self, parent = QModelIndex(), *args, **kwargs):
        return len(self.layer_tree_list)

    def data(self, index, role = None):
        return self.layer_tree_list[index].layer().name()
