# coding=utf-8
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, pyqtSignal


class LoggingListModel(QAbstractListModel):
    data_added = pyqtSignal()
    def __init__(self, parent=None):
        super(LoggingListModel, self).__init__(parent)
        self._data = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()]
        return None

    def add_data(self, record):
        self.beginResetModel()
        self._data.append(record)
        self.endResetModel()
        self.data_added.emit()
