from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from ..DataProcessing.ImportData.DataTypeParser import DataTypeParser


class InputDataTypesList(QAbstractListModel):

    def __init__(self, parent=None):
        super(InputDataTypesList, self).__init__(parent)
        self.__data = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.__data)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        if index.row() >= len(self.__data):
            return QVariant()

        if role == Qt.DisplayRole:
            return QVariant(self.__data[index.row()].get_datatype_name)
        else:
            return QVariant()

    def add_data_record(self, data_type_parcer):
        dataLen = self.rowCount()
        record = (dataLen - 1, data_type_parcer)
        self.__data.append(record)

    def get_current_parcer(self, index):
        return self.__data[index].get_parser




