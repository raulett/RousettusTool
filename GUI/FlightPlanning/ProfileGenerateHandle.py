from qgis.PyQt.QtWidgets import QDialog
from ...UI.FlightPlanning.ProfileGenerate_ui import Ui_ProfileGenerateWiget
from .GetLineTool import GetLineTool
from ...tools.DataProcessing.GeometryHandling.AffineTransform import AffilneTransform

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QVariant

from qgis.core import Qgis, QgsMapLayerProxyModel, QgsVectorLayer, QgsFeature, QgsProject, QgsPointXY, \
    QgsGeometry, QgsPoint, QgsLineString, QgsField, QgsFields, QgsCoordinateReferenceSystem
from qgis.gui import QgisInterface
from qgis.utils import iface
import os, statistics




class ProfileGenerateHandle(Ui_ProfileGenerateWiget, QDialog):
    debug = 0
    def __init__(self, progressBar=None, logger=None, main_window=None, parent=None):
        super(ProfileGenerateHandle, self).__init__(parent)
        self.module_tag = 'Profile generate handler'
        self.setupUi(self)
        self.progressBar = progressBar
        self.main_window = main_window
        self.logger = logger
        self.canvas = None
        self.current_tool = None
        self.profile_fields = QgsFields()
        self.profile_fields.append(QgsField('prof_num', QVariant.Int))
        self.profile_fields.append(QgsField('azimuth', QVariant.Double))
        self.profile_fields.append(QgsField('pr_dist', QVariant.Int))

        #init fields
        self.profiles_save_path = os.path.join(self.main_window.current_project_path,
                                              "flights", 'flight_planning.gpkg')
        self.update_polygon_features_combobox()
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)

        # connect signals
        self.mMapLayerComboBox.layerChanged.connect(self.mMapLayerComboBox_update_layer_handler)
        self.pushButton_get_azimuth.clicked.connect(self.pushButton_get_azimuth_handler)
        self.pushButton_add_profiles.clicked.connect(self.add_profiles_button_handler)
        self.initGui()

    def initGui(self):
        try:
            self.lineEdit_projectName.setText(str(self.main_window.profiles_save_path))
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
        try:
            crs = self.mMapLayerComboBox.currentLayer().crs()
        except:
            crs = QgsCoordinateReferenceSystem()
        if self.debug:
            print('set icon call')
        if not (r'units=m' in crs.toProj()):
            self.label_layer_icon.setPixmap(QPixmap(":/plugins/RousettusTool/resources/warning.png"))
            self.label_layer_icon.setToolTip('Layer has non metric CRS')
        else:
            self.label_layer_icon.setPixmap(QPixmap())
            self.label_layer_icon.setToolTip('')

    def mMapLayerComboBox_update_layer_handler(self):
        self.set_icon()
        self.update_polygon_features_combobox()

    def add_profiles_button_handler(self):
        rotation_angle = -1 * self.mQgsDoubleSpinBox_azimuth.value()
        affineTransform = AffilneTransform(rotation_angle)
        # rotated_geometry = affineTransform.transform_geom(self.mFeaturePickerWidget.feature().geometry())
        geometry = self.mFeaturePickerWidget.feature().geometry()
        medianX_val = statistics.median([vertex.x() for vertex in geometry.vertices()])
        medianY_val = statistics.median([vertex.y() for vertex in geometry.vertices()])
        rotated_geometry = QgsGeometry(self.mFeaturePickerWidget.feature().geometry())
        rotated_geometry.rotate(rotation_angle, QgsPointXY(medianX_val, medianY_val))
        minX_val = min([vertex.x() for vertex in rotated_geometry.vertices()])
        minY_val = min([vertex.y() for vertex in rotated_geometry.vertices()])
        if self.debug:
            print('ProfileGenerateHandle.add_profiles_button_handler got minimum X from geom: {}'.format(min([vertex.x() for vertex in rotated_geometry.vertices()])))
        # affineTransform.set_shift_vector((-1*minX_val, -1*minY_val))
        # rotated_geometry = affineTransform.shift_geom(rotated_geometry)

        types = ('Point', 'LineString', 'Polygon')
        if self.debug:
            print("from ProfileGenerateHandle.add_profiles_button_handler self.lineEdit_layerName.text(): {}".format(self.lineEdit_profiles_name.text()))
        temp_layer = QgsVectorLayer("LineString", self.lineEdit_profiles_name.text(), "memory")
        temp_layer.setCrs(self.mMapLayerComboBox.currentLayer().crs())
        temp_provider = temp_layer.dataProvider()
        feats = self.generate_profiles(rotated_geometry)
        temp_provider.addAttributes(self.profile_fields)
        temp_layer.updateFields()

        for i in range(len(feats)):
            geom = feats[i].geometry()
            geom.rotate(-1*rotation_angle, QgsPointXY(medianX_val, medianY_val))
            feats[i].setGeometry(geom)

        for feat in feats:
            temp_provider.addFeature(feat)
        temp_layer.updateExtents()
        QgsProject.instance().addMapLayer(temp_layer)

    def generate_profiles(self, geometry):
        if self.debug:
            print("from ProfileGenerateHandle.generate_profiles input geometry: {}".format(geometry))
        vertices = [vertex for vertex in geometry.vertices()]
        segments = []
        minX_val = min([vertex.x() for vertex in geometry.vertices()])
        minY_val = min([vertex.y() for vertex in geometry.vertices()])
        maxX_val = max([vertex.x() for vertex in geometry.vertices()])

        for vertex_index in range(len(vertices)-1):
            segments.append(tuple(sorted([vertices[vertex_index], vertices[vertex_index+1]], key = lambda vertex:vertex.x())))

        profile_delta = self.profile_distance_spinBox.value()
        current_profile_num = self.spinBox_first_num.value()
        overlap_distance = self.spinBox_Overlap_borders.value()
        min_profile_len = self.spinBox_profile_len.value()
        current_profile_dist = 0 + minX_val

        profiles = []

        if self.debug:
            print("from ProfileGenerateHandle.generate_profiles current_profile_dist: {}, maxX_val: {}".format(current_profile_dist, maxX_val))
        if self.debug:
            print("from ProfileGenerateHandle.generate_profiles segments: {}".format(segments))
        # run around potential profiles to intersect
        while current_profile_dist <= maxX_val:
            intersection_segments = []

            for segment in segments:
                if (segment[0].x() <= current_profile_dist < segment[1].x()):
                    intersection_segments.append(segment)
            if len(intersection_segments) < 2:
                current_profile_dist += 1
                continue
            intersection_points = [self.get_intesection_point(current_profile_dist, segment) for segment in intersection_segments]
            intersection_points = sorted(intersection_points, key=lambda point:point.y())
            point_1 = intersection_points[0]
            point_1.setY(point_1.y() - overlap_distance)
            point_2 = intersection_points[len(intersection_points)-1]
            point_2.setY(point_2.y() + overlap_distance)
            if self.debug:
                print("from ProfileGenerateHandle.generate_profiles point1: {}, point2: {}, distance: {}".format(point_1, point_2, (point_1.distance(point_2))))
            if (point_1.distance(point_2)) < min_profile_len:
                current_profile_dist += 1
                continue
            else:
                profiles.append(self.generate_profile_feature(QgsLineString(point_1, point_2), current_profile_num))
                current_profile_dist += profile_delta
                current_profile_num += 1

        if self.debug:
            print("from ProfileGenerateHandle.generate_profiles profiles: {}".format(profiles))
        return profiles




    # return intersection point between 2 QgsPoint tuple represents segment, and x vertical line
    def get_intesection_point(self, x, segment):
        # vertical segment check
        # if segment[1].x() == segment(0).x():
        y_coord = (x - segment[0].x())/(segment[1].x() - segment[0].x())*(segment[1].y() - segment[0].y()) + segment[0].y()
        return QgsPoint(x, y_coord)

    def generate_profile_feature(self, line, profile_num):
        azimuth = self.mQgsDoubleSpinBox_azimuth.value()
        output_feat = QgsFeature()
        output_feat.setGeometry(line)
        output_feat.setFields(self.profile_fields)
        output_feat.setAttribute('prof_num', profile_num)
        output_feat.setAttribute('azimuth', azimuth)
        output_feat.setAttribute('pr_dist', self.profile_distance_spinBox.value())
        return output_feat


