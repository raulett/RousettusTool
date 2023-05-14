from PyQt5 import QtWidgets, QtCore
import typing


COMBOBOX_ITEMS = ['magn', 'gamma']
#Class specifies combobox for choose survey method name (to specify survey method)
class SurveyMethodCombobox(QtWidgets.QComboBox):
    def __init__(self,
                 parent_form: QtWidgets.QWidget,
                 minimum_size: QtCore.QSize = None,
                 combobox_items: typing.List[str] = COMBOBOX_ITEMS):
        super().__init__(parent_form)
        # self.setMinimumSize(minimum_size)
        self.setEditable(True)
        self.setObjectName("choose_surv_method_comboBox")
        for i, item in enumerate(combobox_items):
            self.addItem("")
            self.setItemText(i, item)


