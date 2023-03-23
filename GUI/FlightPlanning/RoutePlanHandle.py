from ...tools.Configurable import Configurable
from ...UI.FlightPlanning.RoutePlan_ui import Ui_RoutePlan_form
from qgis.PyQt.QtWidgets import QDialog


class RoutePlanHandle(Ui_RoutePlan_form, QDialog, Configurable):
    debug = 1

    def __init__(self, progressBar=None, logger=None, main_window=None, parent=None, config=None):
        super().__init__()
        self.module_tag = 'Route plan handler'
        self.main_window = main_window
        self.section_name = 'route_plan'
        self.setupUi(self)
        self.initGui()

    def initGui(self):
        pass
