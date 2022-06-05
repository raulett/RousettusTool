from qgis.PyQt.QtWidgets import QDialog
from ...UI.FlightPlanning.ProfileGenerate_ui import Ui_ProfileGenerateWiget
from .GetLineTool import GetLineTool
from ...tools.DataProcessing.GeometryHandling.AffineTransform import AffilneTransform

from PyQt5.QtGui import QPixmap

from qgis.core import Qgis, QgsMapLayerProxyModel
from qgis.gui import QgisInterface
from qgis.utils import iface
import os




class ProfileGenerateHandle(Ui_ProfileGenerateWiget, QDialog):
    debug = 1
    def __init__(self, progressBar=None, logger=None, main_window=None, parent=None):
        super(ProfileGenerateHandle, self).__init__(parent)
        self.module_tag = 'Profile generate handler'
        self.setupUi(self)
        self.progressBar = progressBar
        self.main_window = main_window
        self.logger = logger
        self.canvas = None
        self.current_tool = None

        #init fields
        self.profiles_save_path = os.path.join(self.main_window.current_project_path,
                                              "flights", 'flight_planning.gpkg')
        self.update_polygon_features_combobox()
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)

        # connect signals
        self.mMapLayerComboBox.layerChanged.connect(self.mMapLayerComboBox_update_layer_handler)
        self.pushButton_get_azimuth.clicked.connect(self.pushButton_get_azimuth_handler)


        self.initGui()

    def initGui(self):
        try:
            self.lineEdit_projectName.setText(str(self.profiles_save_path))
        except Exception as e:

            self.logger.log_msg("no project name from main window. {}".format(e), self.module_tag, Qgis.Warning)

        self.set_icon()

    def update_polygon_features_combobox(self):
        self.mFeaturePickerWidget.setLayer(self.mMapLayerComboBox.currentLayer())

    def pushButton_get_azimuth_handler(self):
        self.main_window.showMinimized()
        self.select_line()

    def select_line(self):
        self.pushButton_get_azimuth.setEnabled(False)
        self.canvas = iface.mapCanvas()

        current_layer = self.canvas.currentLayer()

        if (current_layer.type() == 0) and (current_layer.geometryType()>=1):
            current_layer = self.canvas.currentLayer()
        else:
            current_layer = self.mMapLayerComboBox.currentLayer()
            self.canvas.setCurrentLayer(current_layer)

        self.current_tool = GetLineTool(self.canvas, current_layer)
        # connect signals
        self.current_tool.decline_signal.connect(self.uset_tool)
        self.current_tool.line_found_signl.connect(self.set_azimuth)

        self.canvas.setMapTool(self.current_tool)
        self.main_window.showMinimized()

    def uset_tool(self):
        self.canvas.unsetMapTool(self.current_tool)
        self.pushButton_get_azimuth.setEnabled(True)
        self.main_window.showNormal()

    def set_azimuth(self, azimuth):
        azimuth = azimuth[0]
        if self.debug:
            print('set_azimuth call: {}'.format(azimuth))
        if azimuth < -90:
            azimuth = azimuth + 180
        elif azimuth > 90:
            azimuth = azimuth - 180

        self.mQgsDoubleSpinBox_azimuth.setValue(azimuth)

    # Set or unset warning icon when layer is not metric
    def set_icon(self):
        if self.debug:
            print('set icon call')
        if not (r'units=m' in self.mMapLayerComboBox.currentLayer().crs().toProj()):
            self.label_layer_icon.setPixmap(QPixmap(":/plugins/RousettusTool/resources/warning.png"))
            self.label_layer_icon.setToolTip('Layer has non metric CRS')
        else:
            self.label_layer_icon.setPixmap(QPixmap())
            self.label_layer_icon.setToolTip('')

    def mMapLayerComboBox_update_layer_handler(self):
        self.set_icon()
        self.update_polygon_features_combobox()