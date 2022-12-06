from ...UI.FlightPlanning.FlightPlan_prototype_ui import Ui_FlightPlan_form

from qgis.PyQt.QtWidgets import QDialog
from qgis.gui import QgsFileWidget
from qgis.utils import iface
from qgis.core import QgsMapLayerProxyModel, QgsCoordinateTransform, QgsCoordinateReferenceSystem, QgsProject, \
    QgsPoint, QgsPointXY, QgsGeometry, QgsFeature, QgsVectorLayer, QgsField, QgsFields, QgsVectorFileWriter, \
    QgsWkbTypes


from PyQt5.QtGui import QPixmap, QDoubleValidator
from PyQt5.QtCore import QLocale, QVariant

import os, math

from ...tools.Configurable import Configurable



class FlightPlanningHandle(Ui_FlightPlan_form, QDialog):
    debug = 0
    def __init__(self, progressBar=None, logger=None, main_window=None, parent=None):
        super(FlightPlanningHandle, self).__init__(parent)
        self.setupUi(self)
        self.module_tag = 'Fligh planning handler'
        self.main_window = main_window
        self.logger = logger


        self.flight_missions_save_path = os.path.join(self.main_window.current_project_path, "flights", "FlightMissions")
        self.flights_layers_save_path = os.path.join(self.flight_missions_save_path, 'layers')
        self.exported_flights_save_path = os.path.join(self.flight_missions_save_path, 'FM_export')

        self.initGui()

    def initGui(self):
        self.takeoff_point_layer_ComboBox.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.profiles_mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.LineLayer)
        self.DEM_mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.save_file_mQgsFileWidget.setStorageMode(QgsFileWidget().GetDirectory)
        self.save_file_mQgsFileWidget.setFilePath(self.flight_missions_save_path)
        self.update_warning_block()

        self.takeoff_point_layer_ComboBox.layerChanged.connect(self.update_takeoff_feats_combobox)
        self.profiles_mMapLayerComboBox.layerChanged.connect(self.update_profiles_combobox)
        self.DEM_mMapLayerComboBox.layerChanged.connect(self.update_dem_combobox)
        self.pushButton_get_to_point.clicked.connect(self.get_takeoff_point_from_layer)
        self.pushButton_generate_profiles.clicked.connect(self.handle_generate_flights_button)
        self.pushButton_export.clicked.connect(self.export_flights_handle)

        locale = QLocale(QLocale.English)
        validator = QDoubleValidator().setLocale(locale)
        self.lineEdit_lon.setValidator(validator)
        self.lineEdit_lat.setValidator(validator)
        self.lineEdit_alt.setValidator(validator)
        self.update_takeoff_feats_combobox()
        try:
            self.get_takeoff_point_from_layer()
        except:
            pass


    def update_takeoff_feats_combobox(self):
        self.takeoff_point_ComboBox.setLayer(self.takeoff_point_layer_ComboBox.currentLayer())
        self.update_warning_block()

    def update_profiles_combobox(self):
        self.update_warning_block()

    def update_dem_combobox(self):
        self.update_warning_block()

    def update_warning_block(self):
        takeoff_points_crs = None
        profiles_crs = None
        DEM_crs = None
        try:
            takeoff_points_crs = self.takeoff_point_layer_ComboBox.currentLayer().crs().authid()
        except:
            pass
        try:
            profiles_crs = self.profiles_mMapLayerComboBox.currentLayer().crs().authid()
        except:
            pass
        try:
            DEM_crs = self.DEM_mMapLayerComboBox.currentLayer().crs().authid()
        except:
            pass
        if (takeoff_points_crs == None) or (profiles_crs == None) or (DEM_crs == None):
            return
        if not (takeoff_points_crs == profiles_crs == DEM_crs):
            self.warning_icon_label.setPixmap(QPixmap(":/plugins/RousettusTool/resources/warning.png"))
            self.warning_icon_label.setToolTip('DEM, points and profiles CRS aren`t the same')
            self.warning_text_label.setText('DEM, points and Profiles CRS are different')
        else:
            self.warning_icon_label.setPixmap(QPixmap())
            self.warning_text_label.setText('')
            self.warning_icon_label.setToolTip('')

    def get_takeoff_point_from_layer(self):
        source_crs = self.takeoff_point_layer_ComboBox.currentLayer().crs()
        dest_crs = QgsCoordinateReferenceSystem("EPSG:4326")
        transformer = QgsCoordinateTransform(source_crs, dest_crs, QgsProject.instance())
        takeoff_point = self.takeoff_point_ComboBox.feature().geometry()
        takeoff_point.transform(transformer)
        if self.debug:
            print('from FlightPlanningHandle.get_takeoff_point_from_layer   transformed takeoff: {}'.format(takeoff_point))
        self.lineEdit_lon.setText(str(takeoff_point.asPoint().x()))
        self.lineEdit_lat.setText(str(takeoff_point.asPoint().y()))

    # todo Обработка нажатия кнопки сформировать слои полетов
    def handle_generate_flights_button(self):
        # transform takeoff point to profiles layer crs
        profiles_crs = self.profiles_mMapLayerComboBox.currentLayer().crs()
        takeoff_point_crs = QgsCoordinateReferenceSystem("EPSG:4326")
        transformer = QgsCoordinateTransform(takeoff_point_crs, profiles_crs, QgsProject.instance())
        to_point = QgsPoint(float(self.lineEdit_lon.text()), float(self.lineEdit_lat.text()))
        to_point_geom = QgsGeometry(to_point)
        to_point.transform(transformer)
        to_point_name = self.lineEdit.text()

        #find nearest profile to takeoff point
        profiles_feats = [feature for feature in self.profiles_mMapLayerComboBox.currentLayer().getFeatures()]
        profile_feat = profiles_feats[0]
        # rotate pofile around TO point
        vertices = [vertex for vertex in profile_feat.geometry().vertices()]
        azimuth = vertices[0].azimuth(vertices[len(vertices) - 1])
        rotated_feats = []
        for feat in profiles_feats:
            temp_profile_geom = feat.geometry()
            temp_profile_geom.rotate(-1 * azimuth, QgsPointXY(to_point))
            feat.setGeometry(temp_profile_geom)
            rotated_feats.append(feat)
        rotated_feats = sorted(rotated_feats, key= lambda profile: abs(to_point.x() - profile.geometry().vertexAt(0).x()))
        profile_feat = rotated_feats[0]
        if self.debug:
            print("from FlightPlanningHandle.handle_generate_flights_button nearest profile after rotate: {}, to_point is: {}".format(profile_feat.geometry(), to_point))
        # get profile number (attribute 0)
        profile_num = profile_feat.attribute(0)
        profile_dist = profile_feat.attribute(2)
        flights_mult = self.flights_mult_spinBox.value()

        self.flight_point_fields = QgsFields()
        self.flight_point_fields.append(QgsField('pt_num', QVariant.Int))
        self.flight_point_fields.append(QgsField('ALT', QVariant.Double))
        self.flight_point_fields.append(QgsField('to_point', QVariant.String))
        self.flight_point_fields.append(QgsField('toPntAlt', QVariant.Double))

        if to_point.y() < profile_feat.geometry().vertexAt(0).y():
            nearest_point = QgsPoint(profile_feat.geometry().vertexAt(0).x(), profile_feat.geometry().vertexAt(0).y())
            direction = [1]
        elif to_point.y() > profile_feat.geometry().vertexAt(1).y():
            nearest_point = QgsPoint(profile_feat.geometry().vertexAt(1).x(), profile_feat.geometry().vertexAt(1).y())
            direction = [-1]
        else:
            nearest_point = QgsPoint(profile_feat.geometry().vertexAt(0).x(), to_point.y())
            direction = [1, -1]


        self.create_folders_if_not_exist()
        for dir in direction:
            flight_features = self.generate_flight_features(dir, nearest_point, profile_feat.geometry(), profile_dist)


            layer_name = 'fm_p{}_f{}-{}_{}'.format(self.takeoff_point_ComboBox.feature().id(),
                                                                 profile_num,
                                                                 profile_num + 2 * flights_mult - 1,
                                                                  ('N' if dir == 1 else 'S'))
            layer_path = os.path.join(self.main_window.current_project_path, 'flights', 'flight_missions',
                                  'SHP', '{}.shp'.format(layer_name))
            qinst = QgsProject.instance()
            try:
                qinst.removeMapLayer(qinst.mapLayersByName(layer_name)[0].id())
            except:
                pass
            # if os.path.exists(layer_path):
            #     QgsVectorFileWriter.deleteShapeFile(layer_path)
            writer = QgsVectorFileWriter(layer_path, 'UTF-8', self.flight_point_fields, QgsWkbTypes.Point,
                                         self.profiles_mMapLayerComboBox.currentLayer().crs(), 'ESRI Shapefile')
            # temp_layer = QgsVectorLayer("Point", layer_name, "memory")
            temp_layer = self.add_flight_mission_layer(to_point_name, layer_name, layer_path)
            temp_layer.setCrs(self.profiles_mMapLayerComboBox.currentLayer().crs())
            # temp_layer.startEditing()
            # temp_layer.selectAll()
            # temp_layer.deleteSelectedFeatures()
            # temp_layer.commitChanges()
            temp_layer.startEditing()
            dem_data_provider = self.DEM_mMapLayerComboBox.currentLayer().dataProvider()
            for feature in flight_features:
                temp_flight_geom = feature.geometry()
                temp_flight_geom.rotate(azimuth, QgsPointXY(to_point))
                feature.setGeometry(temp_flight_geom)
                point = feature.geometry().asPoint()
                altitude_asl = dem_data_provider.sample(feature.geometry().asPoint(), 1)[0]
                if self.debug:
                    print('DEM ALTITUDE {} IN point {}'.format(altitude_asl, point))
                try:
                    to_point_alt = float(self.lineEdit_alt.text())
                except:
                    to_point_alt = dem_data_provider.sample(self.takeoff_point_ComboBox.feature().geometry().asPoint(), 1)[0]
                if self.debug:
                        print('DEM ALTITUDE {} IN point {}, to_point'.format(altitude_asl, point))
                altitude_agl = altitude_asl - to_point_alt + self.flight_alt_spinBox.value()
                feature.setAttribute('ALT', altitude_agl)
                feature.setAttribute('toPntAlt', to_point_alt)
                feature.setAttribute('to_point', to_point_name)
                # temp_provider.addFeature(feature)
                writer.addFeature(feature)
            temp_layer.updateExtents()
            temp_layer.commitChanges()
            del(writer)
            # writer = QgsVectorFileWriter.writeAsVectorFormat(temp_layer, r'F:\YandexDisk\Work\ProjectsRepositories\20210416_Rousettus\Test_project\flights\flight_missions\SHP\{}.shp'.format(layer_name), 'utf-8',
            #                                              self.profiles_mMapLayerComboBox.currentLayer().crs(),
            #                                              "ESRI Shapefile")




    #todo Сформировать список фичей для одного полета в плюс и в минус
    # direction == +1|-1 (на север или на юг)
    def generate_flight_features(self, direction, nearest_point_on_profile, profile_geometry, profile_dist):
        result_feats = []
        profile_dist_limit = self.survey_dist_spinBox.value()
        waypoint_distance = self.waypoint_dist_spinBox.value()
        flights_mult = self.flights_mult_spinBox.value()
        waypoint_quantity = (profile_dist_limit/(2*flights_mult))//waypoint_distance
        if self.debug:
            print("from FlightPlanningHandle.generate_flight_features nearest_point_on_profile is: {}".format(nearest_point_on_profile))
        nearest_point = QgsPoint(nearest_point_on_profile.x(), nearest_point_on_profile.y())
        point_number = 1
        counter = 0

        if self.debug:
            print("from FlightPlanningHandle.generate_flight_features nearest_point is: {}, profile {}".format(nearest_point, profile_geometry))

        if self.debug:
            print("from FlightPlanningHandle.generate_flight_features waypoint_quantity will be: {}".format(waypoint_quantity*flights_mult))
        for i in range(flights_mult):
            while counter < waypoint_quantity:
                point = nearest_point.clone()
                # if self.debug:
                #     print("from FlightPlanningHandle.generate_flight_features direct {})waypoint_distance: {}, counter: {}, direction: {}".format(point_number, waypoint_distance, counter, direction))
                point.setY(point.y() + (direction * counter * waypoint_distance))
                # if self.debug:
                #     print("from FlightPlanningHandle.generate_flight_features {})current_point {}, counter: {}".format(point_number, point, counter))
                point_feature = QgsFeature()
                point_feature.setGeometry(point)
                point_feature.setFields(self.flight_point_fields)
                point_feature.setAttribute('pt_num', point_number)
                point_feature.setAttribute('ALT', 0.0)
                result_feats.append(point_feature)
                counter +=1
                point_number +=1
                # if self.debug and (point_number//20 == 0):
                #     print("from FlightPlanningHandle.generate_flight_features there is {} features generated".format(len(result_feats)))

            nearest_point.setX(point.x()+profile_dist)
            nearest_point.setY(point.y())
            counter = 0

            while counter < waypoint_quantity:
                point = nearest_point.clone()
                # if self.debug:
                #     print("from FlightPlanningHandle.generate_flight_features reverse {})waypoint_distance: {}, counter: {}, direction: {}".format(point_number, waypoint_distance, counter, direction))
                point.setY(point.y() - (direction * counter * waypoint_distance))
                # if self.debug:
                #     print("from FlightPlanningHandle.generate_flight_features {})current_point {}, counter: {}".format(point_number, point, counter))
                point_feature = QgsFeature()
                point_feature.setGeometry(point)
                point_feature.setFields(self.flight_point_fields)
                point_feature.setAttribute('pt_num', point_number)
                point_feature.setAttribute('ALT', 0.0)
                result_feats.append(point_feature)
                counter += 1
                point_number += 1

                # if self.debug and (point_number//20 == 0):
                #     print("from FlightPlanningHandle.generate_flight_features there is {} features generated".format(len(result_feats)))

            nearest_point.setX(point.x() + profile_dist)
            nearest_point.setY(point.y())

        return result_feats

    def find_nearest(self):
        pass

    def add_flight_mission_layer(self, to_point_name, layer_name, layer_path):
        root = QgsProject.instance().layerTreeRoot()

        flight_group = root.findGroup('Flights')
        if flight_group == None:
            flight_group = root.addGroup('Flights')

        flight_mission_group = flight_group.findGroup('flight_missions')
        if flight_mission_group == None:
            flight_mission_group = flight_group.addGroup('flight_missions')

        to_point_group = flight_mission_group.findGroup(to_point_name)
        if to_point_group == None:
            to_point_group = flight_mission_group.addGroup(to_point_name)

        layer_tree = to_point_group.findLayer(layer_name)

        if layer_tree == None:
            layer = QgsVectorLayer(layer_path, layer_name, 'ogr')
            QgsProject.instance().addMapLayer(layer, False)
            to_point_group.addLayer(layer)

        else:
            layer = layer_tree.layer()

        return layer

    def create_folders_if_not_exist(self):
        prj_path = self.main_window.current_project_path
        curr_path = os.path.join(prj_path, 'flights', 'flight_missions')
        curr_path = [os.path.join(curr_path, 'SHP'), os.path.join(curr_path, 'WP')]
        for p in curr_path:
            if not os.path.exists(p):
                os.makedirs(p)

    # prototype Export current
    def export_flights_handle(self):
        layer = iface.mapCanvas().currentLayer()
        layer_name = layer.sourceName()
        save_path = os.path.join(self.main_window.current_project_path, 'flights', 'flight_missions',
                                 'WP')
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        lines = self.export_layer_as_mission(layer)
        file = open(save_path + '\\' +'{}.waypoints'.format(layer_name), 'w')
        for line in lines:
            file.write(line)
        file.close()




    def export_layer_as_mission(self, layer):
        lines = []
        commands = {'waypoint': 16, 'RTL': 20}
        source_crs = layer.crs()
        dest_crs = QgsCoordinateReferenceSystem("EPSG:4326")
        transformer = QgsCoordinateTransform(source_crs, dest_crs, QgsProject.instance())
        feats = [feat for feat in layer.getFeatures()]
        feats = sorted(feats, key = lambda feat:int(feat.attribute('pt_num')))
        lines.append('QGC WPL 110\n')
        lines.append('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(0, 1, 0, commands['waypoint'], 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1))
        counter = 1
        for feat in feats:
            geom = feat.geometry()
            geom.transform(transformer)
            lon = geom.asPoint().x()
            lat = geom.asPoint().y()
            alt = feat.attribute('ALT')
            lines.append('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(counter, 0, 3, commands['waypoint'],
                                                                                   0.0, 0.0, 0.0, 0.0,
                                                                                   lat, lon, alt, 1))
            counter +=1
        lines.append('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(counter, 0, 3, commands['RTL'],
                                                                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1))
        return lines









