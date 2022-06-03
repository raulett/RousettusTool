import logging
import os
import re

import qgis.core
from qgis.PyQt.QtWidgets import QMainWindow, QDialog
from qgis.core import *
from qgis.core import QgsProject
from qgis.core import QgsMessageLog

from ..UI.mainWindow_ui import Ui_MainWindow
from ..GUI.DataProcessing.VariationCalculateHandle import VariationCalculateHandle
from ..GUI.FlightPlanning.ProfileGenerateHandle import ProfileGenerateHandle
from ..tools.ServiceClasses.get_current_project_name import get_current_project_name
from ..tools.ServiceClasses.LoggerQgis import LoggerQgis

class RousettusMainWindow(QMainWindow, Ui_MainWindow, QDialog):

    def __init__(self, enable_flags_dict, parent=None):
        """Constructor."""
        super(RousettusMainWindow, self).__init__(parent)
        """Enable and disable functions"""
        self.setupUi(self)
        self.enable_functions(enable_flags_dict)
        self.prj_name, self.current_project_path, self.prj_full_path = get_current_project_name()
        if (len(self.current_project_path.strip()) != 0):
            QgsMessageLog.logMessage("{}. {}".format('main', "project {} loaded".format(self.prj_name)),
                                     "Rousettus_Tool",
                                     level=Qgis.Info)
        self.logger = LoggerQgis()
        self.initGui()



        #add events handler
        #TODO Борода не работает qgis.core.QgsProject.instance().readProject.connect(self.get_current_project_name)
        QgsProject.instance().readProject.connect(self.prj_changed)


        # add slots
        # pydevd.settrace('localhost', port=5566, stdoutToServer=True, stderrToServer=True, suspend=False)
        #self.actionVariation_calculate.triggered.connect(self.add_variation_calculate_tab)
        #self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.actionMake_Profiles.triggered.connect(self.add_profile_generate_tab)


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

    def add_profile_generate_tab(self):
        profile_generate_wiget = ProfileGenerateHandle(self, logger=self.logger, main_window=self)
        self.profile_generate_tab = self.tabWidget.addTab(profile_generate_wiget, 'Profile Generate')

    def closeTab(self, currentIndex):
        self.tabWidget.removeTab(currentIndex)

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





