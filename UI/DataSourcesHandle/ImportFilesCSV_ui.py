# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\YandexDisk\Work\ProjectsRepositories\20210416_Rousettus\RousettusTool\UI\DataSourcesHandle\ImportFilesCSV.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(351, 415)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(150, 100))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_3 = QtWidgets.QFrame(self.widget)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBox = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_4.addWidget(self.checkBox)
        self.verticalLayout_2.addWidget(self.frame_3)
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setMinimumSize(QtCore.QSize(0, 40))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMinimumSize(QtCore.QSize(70, 0))
        self.label.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setMinimumSize(QtCore.QSize(80, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(80, 16777215))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout_2.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.widget)
        self.frame_2.setEnabled(True)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setMinimumSize(QtCore.QSize(70, 0))
        self.label_2.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.comboBox_2 = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_2.setMinimumSize(QtCore.QSize(80, 0))
        self.comboBox_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.frame_4 = QtWidgets.QFrame(self.widget)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.frame_4)
        self.label_3.setMinimumSize(QtCore.QSize(70, 0))
        self.label_3.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.comboBox_3 = QtWidgets.QComboBox(self.frame_4)
        self.comboBox_3.setMinimumSize(QtCore.QSize(80, 0))
        self.comboBox_3.setMaximumSize(QtCore.QSize(80, 16777215))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.horizontalLayout_5.addWidget(self.comboBox_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_5.addWidget(self.lineEdit_3)
        self.verticalLayout_2.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.frame_5)
        self.label_4.setMinimumSize(QtCore.QSize(70, 0))
        self.label_4.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.comboBox_4 = QtWidgets.QComboBox(self.frame_5)
        self.comboBox_4.setMinimumSize(QtCore.QSize(80, 0))
        self.comboBox_4.setMaximumSize(QtCore.QSize(80, 16777215))
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.horizontalLayout_6.addWidget(self.comboBox_4)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.frame_6 = QtWidgets.QFrame(self.widget)
        self.frame_6.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.frame_6)
        self.label_5.setMinimumSize(QtCore.QSize(70, 0))
        self.label_5.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        self.comboBox_5 = QtWidgets.QComboBox(self.frame_6)
        self.comboBox_5.setMinimumSize(QtCore.QSize(80, 0))
        self.comboBox_5.setMaximumSize(QtCore.QSize(80, 16777215))
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.horizontalLayout_7.addWidget(self.comboBox_5)
        self.verticalLayout_2.addWidget(self.frame_6)
        self.frame_8 = QtWidgets.QFrame(self.widget)
        self.frame_8.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.frame_8)
        self.label_6.setMinimumSize(QtCore.QSize(70, 0))
        self.label_6.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        self.comboBox_6 = QtWidgets.QComboBox(self.frame_8)
        self.comboBox_6.setMinimumSize(QtCore.QSize(80, 0))
        self.comboBox_6.setMaximumSize(QtCore.QSize(80, 16777215))
        self.comboBox_6.setObjectName("comboBox_6")
        self.comboBox_6.addItem("")
        self.horizontalLayout_8.addWidget(self.comboBox_6)
        self.verticalLayout_2.addWidget(self.frame_8)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Add"))
        self.pushButton_2.setText(_translate("Form", "Remove"))
        self.pushButton_3.setText(_translate("Form", "Set file type"))
        self.checkBox.setText(_translate("Form", "Date and time in the same field"))
        self.label.setText(_translate("Form", "DATETIME"))
        self.comboBox.setItemText(0, _translate("Form", "None"))
        self.lineEdit.setText(_translate("Form", "dd-mm-YYYYThh:mm:"))
        self.label_2.setText(_translate("Form", "DATE"))
        self.comboBox_2.setItemText(0, _translate("Form", "None"))
        self.label_3.setText(_translate("Form", "TIME"))
        self.comboBox_3.setItemText(0, _translate("Form", "None"))
        self.label_4.setText(_translate("Form", "TIME"))
        self.comboBox_4.setItemText(0, _translate("Form", "None"))
        self.label_5.setText(_translate("Form", "TIME"))
        self.comboBox_5.setItemText(0, _translate("Form", "None"))
        self.label_6.setText(_translate("Form", "TIME"))
        self.comboBox_6.setItemText(0, _translate("Form", "None"))
