from ...tools.Configurable import Configurable
from ...UI.FlightPlanning.RoutePlan_ui import Ui_RoutePlan_form
from ..InterfaceCustumClasses.SurveyMethodCombobox import SurveyMethodCombobox
from qgis.PyQt.QtWidgets import QDialog

from ...tools.Configurable import Configurable


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
        # self.survey_method_combobox = SurveyMethodCombobox(self, self.choose_surv_method_comboBox.minimumSize())
        # self.method_name_horizontalLayout.removeWidget(self.choose_surv_method_comboBox)
        self.choose_surv_method_comboBox = SurveyMethodCombobox(self, self.choose_surv_method_comboBox.minimumSize())
        self.method_name_horizontalLayout.insertWidget(1, self.choose_surv_method_comboBox)
