from qgis.PyQt.QtWidgets import QMainWindow, QDialog
from qgis.core import *
from ..UI.mainWindow_ui import Ui_MainWindow
from ..GUI.DataProcessing.VariationCalculateHandle import VariationCalculateHandle

class RousettusMainWindow(QMainWindow, Ui_MainWindow, QDialog):

    def __init__(self, enable_flags_dict, parent=None):
        """Constructor."""
        super(RousettusMainWindow, self).__init__(parent)
        """Enable and disable functions"""
        self.setupUi(self)
        self.enable_functions(enable_flags_dict)

        # add slots
        # pydevd.settrace('localhost', port=5566, stdoutToServer=True, stderrToServer=True, suspend=False)
        self.actionVariation_calculate.triggered.connect(self.add_variation_calculate_tab)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)

    def enable_functions(self, menu_flags):
        if menu_flags['data processing'][0]:
            self.data_processing_menu.setEnabled(True)
            if menu_flags['data processing'][1]['magnetic data'][0]:
                self.menuMagnetic_Data.setEnabled(True)
                if menu_flags['data processing'][1]['magnetic data'][1]['variation calculate'][0]:
                    self.actionVariation_calculate.setEnabled(True)

    # Add tabs functions
    def add_variation_calculate_tab(self):
        variation_calculate_widget = VariationCalculateHandle(self, self.progressBar)
        self.variation_calculate_tab = self.tabWidget.addTab(variation_calculate_widget, 'Variation Calculate')

    def closeTab(self, currentIndex):
        self.tabWidget.removeTab(currentIndex)

