# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/raulett/store_vol/YandexDisk/Work/ProjectsRepositories/20210416_Rousettus/RousettusTool/UI/Help/AboutWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogAbout(object):
    def setupUi(self, DialogAbout):
        DialogAbout.setObjectName("DialogAbout")
        DialogAbout.resize(280, 170)
        DialogAbout.setMinimumSize(QtCore.QSize(280, 160))
        self.formLayout = QtWidgets.QFormLayout(DialogAbout)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(DialogAbout)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_Author = QtWidgets.QLabel(DialogAbout)
        self.label_Author.setMinimumSize(QtCore.QSize(120, 0))
        self.label_Author.setText("")
        self.label_Author.setObjectName("label_Author")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_Author)
        self.label_2 = QtWidgets.QLabel(DialogAbout)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_email = QtWidgets.QLabel(DialogAbout)
        self.label_email.setMinimumSize(QtCore.QSize(120, 0))
        self.label_email.setText("")
        self.label_email.setObjectName("label_email")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_email)
        self.label_3 = QtWidgets.QLabel(DialogAbout)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_version = QtWidgets.QLabel(DialogAbout)
        self.label_version.setMinimumSize(QtCore.QSize(120, 0))
        self.label_version.setText("")
        self.label_version.setObjectName("label_version")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_version)
        self.button_Close = QtWidgets.QPushButton(DialogAbout)
        self.button_Close.setMaximumSize(QtCore.QSize(80, 16777215))
        self.button_Close.setObjectName("button_Close")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.button_Close)

        self.retranslateUi(DialogAbout)
        QtCore.QMetaObject.connectSlotsByName(DialogAbout)

    def retranslateUi(self, DialogAbout):
        _translate = QtCore.QCoreApplication.translate
        DialogAbout.setWindowTitle(_translate("DialogAbout", "Rousettus about"))
        self.label.setText(_translate("DialogAbout", "Author:"))
        self.label_2.setText(_translate("DialogAbout", "email:"))
        self.label_3.setText(_translate("DialogAbout", "Version:"))
        self.button_Close.setText(_translate("DialogAbout", "Close"))
