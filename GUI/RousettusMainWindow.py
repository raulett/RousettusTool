import logging
import os
import re

import qgis.core
from qgis.PyQt.QtWidgets import QMainWindow, QDialog, QWidget
from qgis.core import *
from qgis.core import QgsProject
from qgis.core import QgsMessageLog

from ..UI.mainWindow_ui import Ui_MainWindow
from ..GUI.DataProcessing.VariationCalculateHandle import VariationCalculateHandle
from ..GUI.FlightPlanning.ProfileGenerateHandle import ProfileGenerateHandle
from ..GUI.FlightPlanning.FlighfPlanningHandle import FlightPlanningHandle
from ..tools.ServiceClasses.get_current_project_name import get_current_project_name
from ..tools.ServiceClasses.LoggerQgis import LoggerQgis

from PyQt5.QtCore import Qt

class RousettusMainWindow(QMainWindow, Ui_MainWindow, QDialog):
    debug = 1
    def __init__(self, enable_flags_dict, parent=None):
        """Constructor."""
        super(RousettusMainWindow, self).__init__(parent)
        """Enable and disable functions"""
        self.tab_exist_flags = {}
        self.setupUi(self)
        self.profile_generate_tab = None
        self.logger = LoggerQgis()
        self.enable_functions(enable_flags_dict)
        self.prj_name, self.current_project_path, self.prj_full_path = get_current_project_name()
        if (len(self.current_project_path.strip()) != 0):
            QgsMessageLog.logMessage("{}. {}".format('main', "project {} loaded".format(self.prj_name)),
                                     "Rousettus_Tool",
                                     level=Qgis.Info)
        self.initGui()

        #Минимизация окна
        # self.setWindowState(self.windowState() | Qt.WindowMinimized)



        #add events handler
        #TODO Борода не работает qgis.core.QgsProject.instance().readProject.connect(self.get_current_project_name)
        QgsProject.instance().readProject.connect(self.prj_changed)
        self.tabWidget.tabCloseRequested.connect(lambda index: self.closeTab(index))


        # add slots
        # pydevd.settrace('localhost', port=5566, stdoutToServer=True, stderrToServer=True, suspend=False)
        #self.actionVariation_calculate.triggered.connect(self.add_variation_calculate_tab)
        #self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.actionMake_Profiles.triggered.connect(self.add_profile_generate_tab)
        self.actionPlan_Flights.triggered.connect(self.add_flaght_planning_tab)


    def enable_functions(self, menu_flags):
        if menu_flags['data processing'][0]:
            self.data_processing_menu.setEnabled(True)
            if menu_flags['data processing'][1]['magnetic data'][0]:
                self.menuMagnetic_Data.setEnabled(True)
                if menu_flags['data processing'][1]['magnetic data'][1]['variation calculate'][0]:
                    self.actionVariation_calculate.setEnabled(True)

    # Add tabs functions
    def add_variation_calculate_tab(self):
        variation_calculate_widget = VariationCalculateHandle(self, self.progressBar)
        self.variation_calculate_tab = self.tabWidget.addTab(variation_calculate_widget, 'Variation Calculate')

    def add_flaght_planning_tab(self):
        if self.tab_exist_flags.get('Flight planning', 0) == 0:
            flight_planning_wiget = FlightPlanningHandle(self, logger=self.logger, main_window=self)
            self.tabWidget.addTab(flight_planning_wiget, 'Flight Planning')
            self.tab_exist_flags['Flight Planning'] = 1
        else:
            self.tabWidget.setCurrentWidget(self.tabWidget.findChild(QWidget, 'Flight Planning'))

    def add_profile_generate_tab(self):
        if self.debug:
            print ("called add_profile_function")
            print("current tab_exist_flags['Profile Generate'] = {}".
                  format(self.tab_exist_flags.get('Profile Generate', 0)))
        if self.tab_exist_flags.get('Profile Generate', 0) == 0:
            profile_generate_wiget = ProfileGenerateHandle(self, logger=self.logger, main_window=self)
            self.tabWidget.addTab(profile_generate_wiget, 'Profile Generate')
            self.tab_exist_flags['Profile Generate'] = 1
        else:
            self.tabWidget.setCurrentWidget(self.tabWidget.findChild(QWidget, 'Profile Generate'))

    def closeTab(self, currentIndex):
        if self.debug:
            print("closing wiget is {}, profile generate type is {}".format(self.tabWidget.tabText(currentIndex), type(self.tabWidget.tabText(currentIndex))))
        self.tab_exist_flags['{}'.format(self.tabWidget.tabText(currentIndex))] = 0
        self.tabWidget.removeTab(currentIndex)
        if self.debug:
            print("close_tab func, after delete = {}".format(self.tab_exist_flags))

    def initGui(self):
        self.label_prj_name.setText(self.prj_name)
        self.label_prj_path.setText(self.current_project_path)

    #slot for project changed signal
    def prj_changed(self):
        self.prj_name, self.current_project_path, self.prj_full_path = get_current_project_name()
        self.initGui()
        tab_widget_count = self.tabWidget.count()
        for i in range(tab_widget_count):
            self.tabWidget.widget(i).self.initGui()

        if (len(self.current_project_path.strip()) != 0):
            QgsMessageLog.logMessage("{}. {}".format('main', "project {} loaded".format(self.prj_name)),
                                     "Rousettus_Tool",
                                     level=Qgis.Info)






