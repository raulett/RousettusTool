# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\YandexDisk\Work\ProjectsRepositories\20210416_Rousettus\RousettusTool\UI\FlightPlanning\FlightPlan_test.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FlightPlan_test_form(object):
    def setupUi(self, FlightPlan_test_form):
        FlightPlan_test_form.setObjectName("FlightPlan_test_form")
        FlightPlan_test_form.resize(674, 639)
        FlightPlan_test_form.setMinimumSize(QtCore.QSize(600, 0))
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(FlightPlan_test_form)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_10 = QtWidgets.QLabel(FlightPlan_test_form)
        self.label_10.setMinimumSize(QtCore.QSize(70, 0))
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_6.addWidget(self.label_10)
        self.lineEdit = QtWidgets.QLineEdit(FlightPlan_test_form)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_6.addWidget(self.lineEdit)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(FlightPlan_test_form)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 80))
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setMinimumSize(QtCore.QSize(90, 20))
        self.label_4.setMaximumSize(QtCore.QSize(60, 20))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.profiles_mMapLayerComboBox = QgsMapLayerComboBox(self.groupBox_2)
        self.profiles_mMapLayerComboBox.setMinimumSize(QtCore.QSize(200, 22))
        self.profiles_mMapLayerComboBox.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.profiles_mMapLayerComboBox.setFont(font)
        self.profiles_mMapLayerComboBox.setObjectName("profiles_mMapLayerComboBox")
        self.horizontalLayout_2.addWidget(self.profiles_mMapLayerComboBox)
        self.mFeatureListComboBox = QgsFeaturePickerWidget(self.groupBox_2)
        self.mFeatureListComboBox.setObjectName("mFeatureListComboBox")
        self.horizontalLayout_2.addWidget(self.mFeatureListComboBox)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_4 = QtWidgets.QGroupBox(FlightPlan_test_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setMinimumSize(QtCore.QSize(0, 60))
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.DEM_mMapLayerComboBox = QgsMapLayerComboBox(self.groupBox_4)
        self.DEM_mMapLayerComboBox.setMinimumSize(QtCore.QSize(200, 22))
        self.DEM_mMapLayerComboBox.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.DEM_mMapLayerComboBox.setFont(font)
        self.DEM_mMapLayerComboBox.setObjectName("DEM_mMapLayerComboBox")
        self.horizontalLayout.addWidget(self.DEM_mMapLayerComboBox)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.warning_text_label = QtWidgets.QLabel(FlightPlan_test_form)
        self.warning_text_label.setMinimumSize(QtCore.QSize(200, 32))
        self.warning_text_label.setMaximumSize(QtCore.QSize(16777215, 32))
        self.warning_text_label.setText("")
        self.warning_text_label.setObjectName("warning_text_label")
        self.verticalLayout.addWidget(self.warning_text_label)
        self.warning_icon_label = QtWidgets.QLabel(FlightPlan_test_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.warning_icon_label.sizePolicy().hasHeightForWidth())
        self.warning_icon_label.setSizePolicy(sizePolicy)
        self.warning_icon_label.setMinimumSize(QtCore.QSize(32, 32))
        self.warning_icon_label.setMaximumSize(QtCore.QSize(32, 32))
        self.warning_icon_label.setText("")
        self.warning_icon_label.setObjectName("warning_icon_label")
        self.verticalLayout.addWidget(self.warning_icon_label)
        self.verticalLayout_5.addLayout(self.verticalLayout)
        self.groupBox_3 = QtWidgets.QGroupBox(FlightPlan_test_form)
        self.groupBox_3.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.comboBox_function = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_function.setObjectName("comboBox_function")
        self.comboBox_function.addItem("")
        self.comboBox_function.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_function, 1, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBox_3)
        self.label_14.setMinimumSize(QtCore.QSize(200, 0))
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 0, 0, 1, 1)
        self.flight_alt_spinBox = QtWidgets.QSpinBox(self.groupBox_3)
        self.flight_alt_spinBox.setMinimumSize(QtCore.QSize(80, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.flight_alt_spinBox.setFont(font)
        self.flight_alt_spinBox.setMaximum(999999)
        self.flight_alt_spinBox.setProperty("value", 90)
        self.flight_alt_spinBox.setObjectName("flight_alt_spinBox")
        self.gridLayout_2.addWidget(self.flight_alt_spinBox, 0, 1, 1, 1)
        self.down_deviation_spinbox = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        self.down_deviation_spinbox.setMinimum(-1000.0)
        self.down_deviation_spinbox.setMaximum(0.0)
        self.down_deviation_spinbox.setProperty("value", -2.0)
        self.down_deviation_spinbox.setObjectName("down_deviation_spinbox")
        self.gridLayout_2.addWidget(self.down_deviation_spinbox, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 3, 0, 1, 1)
        self.up_deviation_spinbox = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        self.up_deviation_spinbox.setMinimum(0.0)
        self.up_deviation_spinbox.setMaximum(1000.0)
        self.up_deviation_spinbox.setProperty("value", 5.0)
        self.up_deviation_spinbox.setObjectName("up_deviation_spinbox")
        self.gridLayout_2.addWidget(self.up_deviation_spinbox, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 3, 1, 1)
        self.flights_mult_spinBox = QtWidgets.QSpinBox(self.groupBox_3)
        self.flights_mult_spinBox.setEnabled(False)
        self.flights_mult_spinBox.setMinimumSize(QtCore.QSize(80, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.flights_mult_spinBox.setFont(font)
        self.flights_mult_spinBox.setProperty("value", 1)
        self.flights_mult_spinBox.setObjectName("flights_mult_spinBox")
        self.gridLayout_2.addWidget(self.flights_mult_spinBox, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setMinimumSize(QtCore.QSize(200, 0))
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.groupBox_3)
        self.spinBox.setMaximum(99999)
        self.spinBox.setProperty("value", 60)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout_2.addWidget(self.spinBox, 3, 3, 1, 1)
        self.verticalLayout_5.addWidget(self.groupBox_3)
        self.groupBox_5 = QtWidgets.QGroupBox(FlightPlan_test_form)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_11 = QtWidgets.QLabel(self.groupBox_5)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_7.addWidget(self.label_11)
        self.save_file_mQgsFileWidget = QgsFileWidget(self.groupBox_5)
        self.save_file_mQgsFileWidget.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_file_mQgsFileWidget.sizePolicy().hasHeightForWidth())
        self.save_file_mQgsFileWidget.setSizePolicy(sizePolicy)
        self.save_file_mQgsFileWidget.setObjectName("save_file_mQgsFileWidget")
        self.horizontalLayout_7.addWidget(self.save_file_mQgsFileWidget)
        self.comboBox = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox.setEnabled(False)
        self.comboBox.setMinimumSize(QtCore.QSize(180, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(180, 16777215))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.horizontalLayout_7.addWidget(self.comboBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.verticalLayout_5.addWidget(self.groupBox_5)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.show_graph_btn = QtWidgets.QPushButton(FlightPlan_test_form)
        self.show_graph_btn.setObjectName("show_graph_btn")
        self.horizontalLayout_8.addWidget(self.show_graph_btn)
        self.init_flight = QtWidgets.QPushButton(FlightPlan_test_form)
        self.init_flight.setObjectName("init_flight")
        self.horizontalLayout_8.addWidget(self.init_flight)
        self.pushButton_generate_flight = QtWidgets.QPushButton(FlightPlan_test_form)
        self.pushButton_generate_flight.setEnabled(True)
        self.pushButton_generate_flight.setObjectName("pushButton_generate_flight")
        self.horizontalLayout_8.addWidget(self.pushButton_generate_flight)
        self.pushButton_export = QtWidgets.QPushButton(FlightPlan_test_form)
        self.pushButton_export.setEnabled(True)
        self.pushButton_export.setObjectName("pushButton_export")
        self.horizontalLayout_8.addWidget(self.pushButton_export)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.retranslateUi(FlightPlan_test_form)
        QtCore.QMetaObject.connectSlotsByName(FlightPlan_test_form)

    def retranslateUi(self, FlightPlan_test_form):
        _translate = QtCore.QCoreApplication.translate
        FlightPlan_test_form.setWindowTitle(_translate("FlightPlan_test_form", "Form"))
        self.label_10.setText(_translate("FlightPlan_test_form", "Point name"))
        self.lineEdit.setText(_translate("FlightPlan_test_form", "tpN"))
        self.groupBox_2.setTitle(_translate("FlightPlan_test_form", "Survey profiles"))
        self.label_4.setText(_translate("FlightPlan_test_form", "flight_layer"))
        self.groupBox_4.setTitle(_translate("FlightPlan_test_form", "DEM layer"))
        self.groupBox_3.setTitle(_translate("FlightPlan_test_form", "Planning parameters"))
        self.comboBox_function.setItemText(0, _translate("FlightPlan_test_form", "adaptive_func"))
        self.comboBox_function.setItemText(1, _translate("FlightPlan_test_form", "regular_func"))
        self.label.setText(_translate("FlightPlan_test_form", "up deviation"))
        self.label_14.setText(_translate("FlightPlan_test_form", "Flight altitude"))
        self.flight_alt_spinBox.setSuffix(_translate("FlightPlan_test_form", " m"))
        self.label_2.setText(_translate("FlightPlan_test_form", "down deviation"))
        self.label_3.setText(_translate("FlightPlan_test_form", "Reg points dist"))
        self.label_6.setText(_translate("FlightPlan_test_form", "Flights multiplicity"))
        self.groupBox_5.setTitle(_translate("FlightPlan_test_form", "Save settings"))
        self.label_11.setText(_translate("FlightPlan_test_form", "path to result files"))
        self.comboBox.setItemText(0, _translate("FlightPlan_test_form", "*.waypoint (Pixhawk)"))
        self.show_graph_btn.setText(_translate("FlightPlan_test_form", "show_graph"))
        self.init_flight.setText(_translate("FlightPlan_test_form", "init flight"))
        self.pushButton_generate_flight.setText(_translate("FlightPlan_test_form", "generate_flight"))
        self.pushButton_export.setText(_translate("FlightPlan_test_form", "Export as flight"))
from qgsfeaturepickerwidget import QgsFeaturePickerWidget
from qgsfilewidget import QgsFileWidget
from qgsmaplayercombobox import QgsMapLayerComboBox
