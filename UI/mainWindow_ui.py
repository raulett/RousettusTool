# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\YandexDisk\Work\ProjectsRepositories\20210416_Rousettus\RousettusTool\UI\mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 688)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(-1, 2, -1, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalFrame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalFrame.sizePolicy().hasHeightForWidth())
        self.horizontalFrame.setSizePolicy(sizePolicy)
        self.horizontalFrame.setMinimumSize(QtCore.QSize(100, 0))
        self.horizontalFrame.setObjectName("horizontalFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.horizontalFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.label_prj_name = QtWidgets.QLabel(self.horizontalFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_prj_name.sizePolicy().hasHeightForWidth())
        self.label_prj_name.setSizePolicy(sizePolicy)
        self.label_prj_name.setMinimumSize(QtCore.QSize(0, 0))
        self.label_prj_name.setMaximumSize(QtCore.QSize(300, 16777215))
        self.label_prj_name.setText("")
        self.label_prj_name.setScaledContents(True)
        self.label_prj_name.setObjectName("label_prj_name")
        self.horizontalLayout.addWidget(self.label_prj_name)
        self.line = QtWidgets.QFrame(self.horizontalFrame)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.label_prj_path = QtWidgets.QLabel(self.horizontalFrame)
        self.label_prj_path.setToolTip("")
        self.label_prj_path.setText("")
        self.label_prj_path.setScaledContents(True)
        self.label_prj_path.setObjectName("label_prj_path")
        self.horizontalLayout.addWidget(self.label_prj_path)
        self.verticalLayout.addWidget(self.horizontalFrame)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.data_processing_menu = QtWidgets.QMenu(self.menubar)
        self.data_processing_menu.setEnabled(False)
        self.data_processing_menu.setObjectName("data_processing_menu")
        self.menuMagnetic_Data = QtWidgets.QMenu(self.data_processing_menu)
        self.menuMagnetic_Data.setEnabled(False)
        self.menuMagnetic_Data.setObjectName("menuMagnetic_Data")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setEnabled(False)
        self.menu_3.setObjectName("menu_3")
        self.menuFligft_Planning = QtWidgets.QMenu(self.menubar)
        self.menuFligft_Planning.setObjectName("menuFligft_Planning")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.exitButton = QtWidgets.QAction(MainWindow)
        self.exitButton.setObjectName("exitButton")
        self.DBsettingsButton = QtWidgets.QAction(MainWindow)
        self.DBsettingsButton.setObjectName("DBsettingsButton")
        self.action_CSV = QtWidgets.QAction(MainWindow)
        self.action_CSV.setObjectName("action_CSV")
        self.OpenPrjButton = QtWidgets.QAction(MainWindow)
        self.OpenPrjButton.setObjectName("OpenPrjButton")
        self.actionVariation_calculate = QtWidgets.QAction(MainWindow)
        self.actionVariation_calculate.setEnabled(False)
        self.actionVariation_calculate.setObjectName("actionVariation_calculate")
        self.actionMake_Profiles = QtWidgets.QAction(MainWindow)
        self.actionMake_Profiles.setObjectName("actionMake_Profiles")
        self.actionPlan_Flights = QtWidgets.QAction(MainWindow)
        self.actionPlan_Flights.setObjectName("actionPlan_Flights")
        self.actionAbout_Rousettus = QtWidgets.QAction(MainWindow)
        self.actionAbout_Rousettus.setObjectName("actionAbout_Rousettus")
        self.menuMagnetic_Data.addAction(self.actionVariation_calculate)
        self.data_processing_menu.addAction(self.menuMagnetic_Data.menuAction())
        self.menu_2.addAction(self.OpenPrjButton)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.exitButton)
        self.menu_3.addAction(self.DBsettingsButton)
        self.menuFligft_Planning.addAction(self.actionMake_Profiles)
        self.menuFligft_Planning.addAction(self.actionPlan_Flights)
        self.menuHelp.addAction(self.actionAbout_Rousettus)
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.data_processing_menu.menuAction())
        self.menubar.addAction(self.menuFligft_Planning.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RousettusTool"))
        self.label_2.setText(_translate("MainWindow", "Project name:"))
        self.data_processing_menu.setTitle(_translate("MainWindow", "Data Processing"))
        self.menuMagnetic_Data.setTitle(_translate("MainWindow", "Magnetic Data"))
        self.menu_2.setTitle(_translate("MainWindow", "File"))
        self.menu_3.setTitle(_translate("MainWindow", "Settings"))
        self.menuFligft_Planning.setTitle(_translate("MainWindow", "Fligft Planning"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.exitButton.setText(_translate("MainWindow", "Выйти"))
        self.DBsettingsButton.setText(_translate("MainWindow", "Database settings"))
        self.action_CSV.setText(_translate("MainWindow", "из файла CSV"))
        self.OpenPrjButton.setText(_translate("MainWindow", "Открыть проект"))
        self.actionVariation_calculate.setText(_translate("MainWindow", "Variation calculate"))
        self.actionMake_Profiles.setText(_translate("MainWindow", "Make Profiles"))
        self.actionPlan_Flights.setText(_translate("MainWindow", "Plan Flights"))
        self.actionAbout_Rousettus.setText(_translate("MainWindow", "About Rousettus"))
