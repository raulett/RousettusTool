from qgis.PyQt.QtWidgets import QDialog
from ...UI.FlightPlanning.ProfileGenerate_ui import Ui_ProfileGenerateWiget


class ProfileGenerateHandle(Ui_ProfileGenerateWiget, QDialog):
    def __init__(self, progressBar=None, logger=None, main_window=None, parent=None):
        super(ProfileGenerateHandle, self).__init__(parent)
        self.setupUi(self)
        self.progressBar = progressBar

    def initGui(self):
        pass