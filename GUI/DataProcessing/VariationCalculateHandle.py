from qgis.PyQt.QtWidgets import QDialog
from ...UI.DataProcessing.VariationCalculate_ui import Ui_CalculateVariationWiget
from ...tools.DataModels.InputDataTypesList import InputDataTypesList

class VariationCalculateHandle(Ui_CalculateVariationWiget, QDialog):

    def __init__(self, progressBar, parent=None):
        super(VariationCalculateHandle, self).__init__(parent)
        self.setupUi(self)
        self.progressBar = progressBar
        # self.variation_data_type_model =
        self.VariationImportDataType_comboBox.setModel(self.variation_data_type_model)

    def init_variation_dt_model(self):
        variation_data_type_model = InputDataTypesList(self)
        # variation_data_type_model



