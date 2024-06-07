# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/raulett/store_vol/YandexDisk/Work/ProjectsRepositories/20210416_Rousettus/RousettusTool/UI/FlightPlanning/RoutePlan.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RoutePlan_form(object):
    def setupUi(self, RoutePlan_form):
        RoutePlan_form.setObjectName("RoutePlan_form")
        RoutePlan_form.setEnabled(True)
        RoutePlan_form.resize(719, 626)
        RoutePlan_form.setMinimumSize(QtCore.QSize(600, 0))
        RoutePlan_form.setStyleSheet("font-size:10pt")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(RoutePlan_form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.method_name_horizontalLayout = QtWidgets.QHBoxLayout()
        self.method_name_horizontalLayout.setObjectName("method_name_horizontalLayout")
        self.label_6 = QtWidgets.QLabel(RoutePlan_form)
        self.label_6.setMinimumSize(QtCore.QSize(110, 30))
        self.label_6.setMaximumSize(QtCore.QSize(100, 30))
        self.label_6.setObjectName("label_6")
        self.method_name_horizontalLayout.addWidget(self.label_6)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.method_name_horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.method_name_horizontalLayout)
        self.groupBox = QtWidgets.QGroupBox(RoutePlan_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setToolTipDuration(1)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.line_2 = QtWidgets.QFrame(self.groupBox)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setMinimumSize(QtCore.QSize(80, 0))
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 0, 2, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setMinimumSize(QtCore.QSize(80, 0))
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.takeoff_point_ComboBox = QgsFeaturePickerWidget(self.groupBox)
        self.takeoff_point_ComboBox.setMinimumSize(QtCore.QSize(200, 25))
        self.takeoff_point_ComboBox.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.takeoff_point_ComboBox.setFont(font)
        self.takeoff_point_ComboBox.setObjectName("takeoff_point_ComboBox")
        self.gridLayout.addWidget(self.takeoff_point_ComboBox, 2, 1, 1, 1)
        self.TO_layer_warning_Label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(32)
        sizePolicy.setVerticalStretch(32)
        sizePolicy.setHeightForWidth(self.TO_layer_warning_Label.sizePolicy().hasHeightForWidth())
        self.TO_layer_warning_Label.setSizePolicy(sizePolicy)
        self.TO_layer_warning_Label.setMinimumSize(QtCore.QSize(32, 32))
        self.TO_layer_warning_Label.setMaximumSize(QtCore.QSize(32, 32))
        self.TO_layer_warning_Label.setToolTipDuration(-1)
        self.TO_layer_warning_Label.setText("")
        self.TO_layer_warning_Label.setObjectName("TO_layer_warning_Label")
        self.gridLayout.addWidget(self.TO_layer_warning_Label, 0, 3, 1, 1)
        self.TO_feature_Label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(32)
        sizePolicy.setVerticalStretch(32)
        sizePolicy.setHeightForWidth(self.TO_feature_Label.sizePolicy().hasHeightForWidth())
        self.TO_feature_Label.setSizePolicy(sizePolicy)
        self.TO_feature_Label.setMinimumSize(QtCore.QSize(32, 32))
        self.TO_feature_Label.setMaximumSize(QtCore.QSize(32, 32))
        self.TO_feature_Label.setToolTipDuration(-1)
        self.TO_feature_Label.setText("")
        self.TO_feature_Label.setObjectName("TO_feature_Label")
        self.gridLayout.addWidget(self.TO_feature_Label, 2, 3, 1, 1)
        self.takeoff_point_layer_ComboBox = QgsMapLayerComboBox(self.groupBox)
        self.takeoff_point_layer_ComboBox.setObjectName("takeoff_point_layer_ComboBox")
        self.gridLayout.addWidget(self.takeoff_point_layer_ComboBox, 0, 1, 1, 1)
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(187, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(RoutePlan_form)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 80))
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setMinimumSize(QtCore.QSize(90, 20))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.profiles_mMapLayerComboBox = QgsMapLayerComboBox(self.groupBox_2)
        self.profiles_mMapLayerComboBox.setMinimumSize(QtCore.QSize(200, 25))
        self.profiles_mMapLayerComboBox.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.profiles_mMapLayerComboBox.setFont(font)
        self.profiles_mMapLayerComboBox.setObjectName("profiles_mMapLayerComboBox")
        self.horizontalLayout_2.addWidget(self.profiles_mMapLayerComboBox)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_2.addWidget(self.checkBox)
        self.profile_layers_warning_label = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(32)
        sizePolicy.setVerticalStretch(32)
        sizePolicy.setHeightForWidth(self.profile_layers_warning_label.sizePolicy().hasHeightForWidth())
        self.profile_layers_warning_label.setSizePolicy(sizePolicy)
        self.profile_layers_warning_label.setMinimumSize(QtCore.QSize(32, 32))
        self.profile_layers_warning_label.setMaximumSize(QtCore.QSize(32, 32))
        self.profile_layers_warning_label.setText("")
        self.profile_layers_warning_label.setObjectName("profile_layers_warning_label")
        self.horizontalLayout_2.addWidget(self.profile_layers_warning_label)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.warning_icon_label = QtWidgets.QLabel(RoutePlan_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.warning_icon_label.sizePolicy().hasHeightForWidth())
        self.warning_icon_label.setSizePolicy(sizePolicy)
        self.warning_icon_label.setMinimumSize(QtCore.QSize(32, 32))
        self.warning_icon_label.setMaximumSize(QtCore.QSize(32, 32))
        self.warning_icon_label.setText("")
        self.warning_icon_label.setObjectName("warning_icon_label")
        self.horizontalLayout_5.addWidget(self.warning_icon_label)
        self.warning_text_label = QtWidgets.QLabel(RoutePlan_form)
        self.warning_text_label.setMinimumSize(QtCore.QSize(200, 32))
        self.warning_text_label.setMaximumSize(QtCore.QSize(16777215, 32))
        self.warning_text_label.setText("")
        self.warning_text_label.setObjectName("warning_text_label")
        self.horizontalLayout_5.addWidget(self.warning_text_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.groupBox_3 = QtWidgets.QGroupBox(RoutePlan_form)
        self.groupBox_3.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 0, 2, 1, 1)
        self.service_dist_spinBox = QtWidgets.QSpinBox(self.groupBox_3)
        self.service_dist_spinBox.setMinimumSize(QtCore.QSize(80, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.service_dist_spinBox.setFont(font)
        self.service_dist_spinBox.setMaximum(999999)
        self.service_dist_spinBox.setProperty("value", 1000)
        self.service_dist_spinBox.setObjectName("service_dist_spinBox")
        self.gridLayout_2.addWidget(self.service_dist_spinBox, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setMinimumSize(QtCore.QSize(200, 0))
        self.label_5.setMaximumSize(QtCore.QSize(140, 16777215))
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setMinimumSize(QtCore.QSize(200, 0))
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 1, 0, 1, 1)
        self.survey_dist_spinBox = QtWidgets.QSpinBox(self.groupBox_3)
        self.survey_dist_spinBox.setMinimumSize(QtCore.QSize(80, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.survey_dist_spinBox.setFont(font)
        self.survey_dist_spinBox.setMaximum(999999)
        self.survey_dist_spinBox.setProperty("value", 5000)
        self.survey_dist_spinBox.setObjectName("survey_dist_spinBox")
        self.gridLayout_2.addWidget(self.survey_dist_spinBox, 0, 1, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_2.addWidget(self.checkBox_2, 2, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        spacerItem5 = QtWidgets.QSpacerItem(20, 329, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem6)
        self.pushButton_generate_routes = QtWidgets.QPushButton(RoutePlan_form)
        self.pushButton_generate_routes.setEnabled(True)
        self.pushButton_generate_routes.setObjectName("pushButton_generate_routes")
        self.horizontalLayout_8.addWidget(self.pushButton_generate_routes)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.retranslateUi(RoutePlan_form)
        QtCore.QMetaObject.connectSlotsByName(RoutePlan_form)

    def retranslateUi(self, RoutePlan_form):
        _translate = QtCore.QCoreApplication.translate
        RoutePlan_form.setWindowTitle(_translate("RoutePlan_form", "Plan Route"))
        self.label_6.setText(_translate("RoutePlan_form", "Method title"))
        self.groupBox.setTitle(_translate("RoutePlan_form", "Takeoff point"))
        self.label_8.setText(_translate("RoutePlan_form", "Point name"))
        self.label_7.setText(_translate("RoutePlan_form", "Point layer"))
        self.groupBox_2.setTitle(_translate("RoutePlan_form", "Survey profiles"))
        self.label_4.setText(_translate("RoutePlan_form", "Initial profiles Layer"))
        self.checkBox.setText(_translate("RoutePlan_form", "selected only"))
        self.groupBox_3.setTitle(_translate("RoutePlan_form", "Planning parameters"))
        self.service_dist_spinBox.setSuffix(_translate("RoutePlan_form", " m"))
        self.label_5.setText(_translate("RoutePlan_form", "Distance limit, m"))
        self.label_9.setText(_translate("RoutePlan_form", "Service route limit, m"))
        self.survey_dist_spinBox.setSuffix(_translate("RoutePlan_form", " m"))
        self.checkBox_2.setText(_translate("RoutePlan_form", "Plan ring routes"))
        self.pushButton_generate_routes.setText(_translate("RoutePlan_form", "Generate Routes"))
from qgsfeaturepickerwidget import QgsFeaturePickerWidget
from qgsmaplayercombobox import QgsMapLayerComboBox
