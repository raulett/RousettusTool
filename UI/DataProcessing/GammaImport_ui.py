# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/raulett/store_vol/YandexDisk/Work/ProjectsRepositories/20210416_Rousettus/RousettusTool/UI/DataProcessing/GammaImport.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CalculateVariationWiget(object):
    def setupUi(self, CalculateVariationWiget):
        CalculateVariationWiget.setObjectName("CalculateVariationWiget")
        CalculateVariationWiget.resize(788, 583)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(CalculateVariationWiget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.line = QtWidgets.QFrame(CalculateVariationWiget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_3.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(CalculateVariationWiget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMaximumSize(QtCore.QSize(400, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.VariationImportDataType_comboBox = QtWidgets.QComboBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VariationImportDataType_comboBox.sizePolicy().hasHeightForWidth())
        self.VariationImportDataType_comboBox.setSizePolicy(sizePolicy)
        self.VariationImportDataType_comboBox.setMinimumSize(QtCore.QSize(150, 0))
        self.VariationImportDataType_comboBox.setMaximumSize(QtCore.QSize(150, 16777215))
        self.VariationImportDataType_comboBox.setObjectName("VariationImportDataType_comboBox")
        self.horizontalLayout_2.addWidget(self.VariationImportDataType_comboBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_4.setMinimumSize(QtCore.QSize(0, 200))
        self.groupBox_4.setMaximumSize(QtCore.QSize(16777215, 200))
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton.setMaximumSize(QtCore.QSize(16777215, 20))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_5.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton_2.setMaximumSize(QtCore.QSize(16777215, 15))
        self.radioButton_2.setChecked(False)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_5.addWidget(self.radioButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.frame = QtWidgets.QFrame(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout.addWidget(self.frame)
        self.verticalLayout_2.addWidget(self.groupBox_4)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.groupBox = QtWidgets.QGroupBox(CalculateVariationWiget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tableView = QtWidgets.QTableView(self.groupBox)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout_4.addWidget(self.tableView)
        self.horizontalLayout_3.addWidget(self.groupBox)

        self.retranslateUi(CalculateVariationWiget)
        QtCore.QMetaObject.connectSlotsByName(CalculateVariationWiget)

    def retranslateUi(self, CalculateVariationWiget):
        _translate = QtCore.QCoreApplication.translate
        CalculateVariationWiget.setWindowTitle(_translate("CalculateVariationWiget", "Import gamma data"))
        self.groupBox_2.setTitle(_translate("CalculateVariationWiget", "Gamma data"))
        self.label.setText(_translate("CalculateVariationWiget", "Choose data source"))
        self.groupBox_3.setTitle(_translate("CalculateVariationWiget", "import"))
        self.groupBox_4.setTitle(_translate("CalculateVariationWiget", "SaveTo"))
        self.radioButton.setText(_translate("CalculateVariationWiget", "Save to GPKG"))
        self.radioButton_2.setText(_translate("CalculateVariationWiget", "To Existig layer"))
        self.groupBox.setTitle(_translate("CalculateVariationWiget", "Importing Data"))
