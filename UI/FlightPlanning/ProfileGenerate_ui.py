# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\raule\YandexDisk\Work\ProjectsRepositories\20210416_Rousettus\RousettusTool\UI\FlightPlanning\ProfileGenerate.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProfileGenerateWiget(object):
    def setupUi(self, ProfileGenerateWiget):
        ProfileGenerateWiget.setObjectName("ProfileGenerateWiget")
        ProfileGenerateWiget.resize(699, 670)
        ProfileGenerateWiget.setMinimumSize(QtCore.QSize(0, 460))
        ProfileGenerateWiget.setStyleSheet("font-size:10pt")
        self.verticalLayout = QtWidgets.QVBoxLayout(ProfileGenerateWiget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(ProfileGenerateWiget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_projectName = QtWidgets.QLineEdit(ProfileGenerateWiget)
        self.lineEdit_projectName.setEnabled(False)
        self.lineEdit_projectName.setMinimumSize(QtCore.QSize(0, 22))
        self.lineEdit_projectName.setObjectName("lineEdit_projectName")
        self.horizontalLayout_4.addWidget(self.lineEdit_projectName)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.groupBox = QtWidgets.QGroupBox(ProfileGenerateWiget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setMinimumSize(QtCore.QSize(220, 0))
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_7.addWidget(self.label_10)
        self.method_name_comboBox = QtWidgets.QComboBox(self.groupBox)
        self.method_name_comboBox.setMinimumSize(QtCore.QSize(200, 22))
        self.method_name_comboBox.setEditable(True)
        self.method_name_comboBox.setObjectName("method_name_comboBox")
        self.method_name_comboBox.addItem("")
        self.method_name_comboBox.addItem("")
        self.horizontalLayout_7.addWidget(self.method_name_comboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(220, 0))
        self.label_2.setMaximumSize(QtCore.QSize(160, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.label_layer_icon = QtWidgets.QLabel(self.groupBox)
        self.label_layer_icon.setMinimumSize(QtCore.QSize(24, 24))
        self.label_layer_icon.setMaximumSize(QtCore.QSize(24, 24))
        self.label_layer_icon.setText("")
        self.label_layer_icon.setObjectName("label_layer_icon")
        self.horizontalLayout_2.addWidget(self.label_layer_icon)
        self.mMapLayerComboBox = QgsMapLayerComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mMapLayerComboBox.sizePolicy().hasHeightForWidth())
        self.mMapLayerComboBox.setSizePolicy(sizePolicy)
        self.mMapLayerComboBox.setMinimumSize(QtCore.QSize(200, 22))
        self.mMapLayerComboBox.setObjectName("mMapLayerComboBox")
        self.horizontalLayout_2.addWidget(self.mMapLayerComboBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.mFeaturePickerWidget = QgsFeaturePickerWidget(self.groupBox)
        self.mFeaturePickerWidget.setMinimumSize(QtCore.QSize(0, 22))
        self.mFeaturePickerWidget.setObjectName("mFeaturePickerWidget")
        self.horizontalLayout_2.addWidget(self.mFeaturePickerWidget)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        self.checkBox.setMinimumSize(QtCore.QSize(260, 0))
        self.checkBox.setMaximumSize(QtCore.QSize(170, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_layerName = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_layerName.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_layerName.sizePolicy().hasHeightForWidth())
        self.lineEdit_layerName.setSizePolicy(sizePolicy)
        self.lineEdit_layerName.setMinimumSize(QtCore.QSize(80, 22))
        self.lineEdit_layerName.setObjectName("lineEdit_layerName")
        self.horizontalLayout.addWidget(self.lineEdit_layerName)
        self.mQgsProjectionSelectionWidget = QgsProjectionSelectionWidget(self.groupBox)
        self.mQgsProjectionSelectionWidget.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mQgsProjectionSelectionWidget.sizePolicy().hasHeightForWidth())
        self.mQgsProjectionSelectionWidget.setSizePolicy(sizePolicy)
        self.mQgsProjectionSelectionWidget.setMinimumSize(QtCore.QSize(150, 22))
        self.mQgsProjectionSelectionWidget.setObjectName("mQgsProjectionSelectionWidget")
        self.horizontalLayout.addWidget(self.mQgsProjectionSelectionWidget)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(ProfileGenerateWiget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(400, 200))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(9)
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)
        self.checkBox_overwrite = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_overwrite.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_overwrite.setFont(font)
        self.checkBox_overwrite.setChecked(True)
        self.checkBox_overwrite.setObjectName("checkBox_overwrite")
        self.gridLayout.addWidget(self.checkBox_overwrite, 5, 0, 1, 1)
        self.spinBox_first_num = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_first_num.setMinimumSize(QtCore.QSize(120, 22))
        self.spinBox_first_num.setMaximumSize(QtCore.QSize(80, 16777215))
        self.spinBox_first_num.setMaximum(10000)
        self.spinBox_first_num.setProperty("value", 1)
        self.spinBox_first_num.setObjectName("spinBox_first_num")
        self.gridLayout.addWidget(self.spinBox_first_num, 3, 1, 1, 1)
        self.pushButton_get_azimuth = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_get_azimuth.setEnabled(True)
        self.pushButton_get_azimuth.setMinimumSize(QtCore.QSize(0, 25))
        self.pushButton_get_azimuth.setToolTipDuration(1)
        self.pushButton_get_azimuth.setCheckable(False)
        self.pushButton_get_azimuth.setChecked(False)
        self.pushButton_get_azimuth.setFlat(False)
        self.pushButton_get_azimuth.setObjectName("pushButton_get_azimuth")
        self.gridLayout.addWidget(self.pushButton_get_azimuth, 0, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)
        self.spinBox_profile_len = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_profile_len.setMinimumSize(QtCore.QSize(120, 22))
        self.spinBox_profile_len.setMaximumSize(QtCore.QSize(80, 16777215))
        self.spinBox_profile_len.setMaximum(999999)
        self.spinBox_profile_len.setProperty("value", 100)
        self.spinBox_profile_len.setObjectName("spinBox_profile_len")
        self.gridLayout.addWidget(self.spinBox_profile_len, 1, 1, 1, 1)
        self.spinBox_Overlap_borders = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_Overlap_borders.setMinimumSize(QtCore.QSize(120, 22))
        self.spinBox_Overlap_borders.setMaximumSize(QtCore.QSize(80, 16777215))
        self.spinBox_Overlap_borders.setProperty("value", 5)
        self.spinBox_Overlap_borders.setObjectName("spinBox_Overlap_borders")
        self.gridLayout.addWidget(self.spinBox_Overlap_borders, 2, 1, 1, 1)
        self.profile_distance_spinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.profile_distance_spinBox.setMinimumSize(QtCore.QSize(0, 22))
        self.profile_distance_spinBox.setMaximum(10000)
        self.profile_distance_spinBox.setProperty("value", 100)
        self.profile_distance_spinBox.setObjectName("profile_distance_spinBox")
        self.gridLayout.addWidget(self.profile_distance_spinBox, 4, 1, 1, 1)
        self.spinBox_azimuth = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.spinBox_azimuth.setDecimals(4)
        self.spinBox_azimuth.setMinimum(-91.0)
        self.spinBox_azimuth.setMaximum(91.0)
        self.spinBox_azimuth.setObjectName("spinBox_azimuth")
        self.gridLayout.addWidget(self.spinBox_azimuth, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 3, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.groupBox_3 = QtWidgets.QGroupBox(ProfileGenerateWiget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setMinimumSize(QtCore.QSize(0, 22))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit_profiles_name = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_profiles_name.setEnabled(False)
        self.lineEdit_profiles_name.setMinimumSize(QtCore.QSize(0, 22))
        self.lineEdit_profiles_name.setObjectName("lineEdit_profiles_name")
        self.horizontalLayout_3.addWidget(self.lineEdit_profiles_name)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.frame = QtWidgets.QFrame(ProfileGenerateWiget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_5.addWidget(self.pushButton_3)
        self.pushButton_add_profiles = QtWidgets.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_add_profiles.setFont(font)
        self.pushButton_add_profiles.setObjectName("pushButton_add_profiles")
        self.horizontalLayout_5.addWidget(self.pushButton_add_profiles)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_5.addWidget(self.pushButton)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(ProfileGenerateWiget)
        QtCore.QMetaObject.connectSlotsByName(ProfileGenerateWiget)

    def retranslateUi(self, ProfileGenerateWiget):
        _translate = QtCore.QCoreApplication.translate
        ProfileGenerateWiget.setWindowTitle(_translate("ProfileGenerateWiget", "Form"))
        self.label_4.setText(_translate("ProfileGenerateWiget", "Save path"))
        self.groupBox.setTitle(_translate("ProfileGenerateWiget", "Border Poly"))
        self.label_10.setText(_translate("ProfileGenerateWiget", "Method name"))
        self.method_name_comboBox.setItemText(0, _translate("ProfileGenerateWiget", "magn"))
        self.method_name_comboBox.setItemText(1, _translate("ProfileGenerateWiget", "gamma"))
        self.label_2.setText(_translate("ProfileGenerateWiget", "Choose input polygon"))
        self.checkBox.setText(_translate("ProfileGenerateWiget", "Save poly with new metric CRS"))
        self.label.setText(_translate("ProfileGenerateWiget", "Poly name"))
        self.groupBox_2.setTitle(_translate("ProfileGenerateWiget", "Profile generation parameters"))
        self.label_6.setText(_translate("ProfileGenerateWiget", "Minimum profile lenght, m"))
        self.label_5.setText(_translate("ProfileGenerateWiget", "Profiles Azimuth, degree"))
        self.label_8.setText(_translate("ProfileGenerateWiget", "First profile number"))
        self.label_7.setText(_translate("ProfileGenerateWiget", "Overlap beyond polygon borders, m"))
        self.checkBox_overwrite.setText(_translate("ProfileGenerateWiget", "Overwrite profiles, if exists"))
        self.pushButton_get_azimuth.setToolTip(_translate("ProfileGenerateWiget", "choose line on current line or polygon layer"))
        self.pushButton_get_azimuth.setText(_translate("ProfileGenerateWiget", "Get azimuth"))
        self.label_9.setText(_translate("ProfileGenerateWiget", "Profile distance, m"))
        self.groupBox_3.setTitle(_translate("ProfileGenerateWiget", "Output"))
        self.label_3.setText(_translate("ProfileGenerateWiget", "Profile layer name"))
        self.lineEdit_profiles_name.setText(_translate("ProfileGenerateWiget", "survey_profiles"))
        self.pushButton_3.setText(_translate("ProfileGenerateWiget", "Plan flight"))
        self.pushButton_add_profiles.setText(_translate("ProfileGenerateWiget", "Generate profiles"))
        self.pushButton.setText(_translate("ProfileGenerateWiget", "Preview"))
from qgsfeaturepickerwidget import QgsFeaturePickerWidget
from qgsmaplayercombobox import QgsMapLayerComboBox
from qgsprojectionselectionwidget import QgsProjectionSelectionWidget
