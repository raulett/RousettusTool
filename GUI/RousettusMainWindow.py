import os
import configparser

from qgis.PyQt.QtWidgets import QMainWindow, QWidget
from qgis.core import *
from qgis.core import QgsProject
from qgis.core import QgsMessageLog

from ..UI.mainWindow_ui import Ui_MainWindow
from ..GUI.DataProcessing.VariationCalculateHandle import VariationCalculateHandle
from ..GUI.FlightPlanning.ProfileGenerateHandle import ProfileGenerateHandle
# from ..GUI.FlightPlanning.FlighfPlanningHandle import FlightPlanningHandle
from ..GUI.FlightPlanning.FlightPlanningRenewHandle import FlightPlanningHandle
from ..GUI.FlightPlanning.RoutePlanHandle import RoutePlanHandle
from ..tools.get_current_project_name import get_current_project_name
from ..tools.ServiceClasses.LoggerQgis import LoggerQgis
from ..GUI.Help.AboutHandle import AboutHandle
from ..tools.Configurable import Configurable


class RousettusMainWindow(QMainWindow, Ui_MainWindow, Configurable):
    debug = 1

    def __init__(self, enable_flags_dict, parent=None):
        """Constructor."""
        super(RousettusMainWindow, self).__init__(parent)
        self.current_project_path = None
        """Enable and disable functions"""
        self.tab_exist_flags = {}
        self.setupUi(self)
        self.profile_generate_tab = None
        # todo debug logger
        # self.logger = None
        self.logger = LoggerQgis()

        self.enable_functions(enable_flags_dict)
        # todo debug project name

        # инициализация конфига
        self.plugin_path = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-1])
        self.rousettus_config_file = os.path.join(self.plugin_path, 'config.ini')
        self.rousettus_config = configparser.ConfigParser()
        self.load_config()

        # self.prj_name, self.current_project_path, self.prj_full_path = '', '', ''
        # if (self.current_project_path != '') and (len(self.current_project_path.strip()) != 0):
        #     QgsMessageLog.logMessage("{}. {}".format('main', "project {} loaded".format(self.prj_name)),
        #                              "Rousettus_Tool",
        #                              level=Qgis.Info)
        self.initGui()

        # Минимизация окна
        # self.setWindowState(self.windowState() | Qt.WindowMinimized)

        # add events handler
        # TODO Борода не работает qgis.core.QgsProject.instance().readProject.connect(self.get_current_project_name)
        QgsProject.instance().readProject.connect(self.prj_changed)
        self.tabWidget.tabCloseRequested.connect(lambda index: self.closeTab(index))

        # add slots
        # pydevd.settrace('localhost', port=5566, stdoutToServer=True, stderrToServer=True, suspend=False)
        # self.actionVariation_calculate.triggered.connect(self.add_variation_calculate_tab)
        # self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.actionMake_Profiles.triggered.connect(self.add_profile_generate_tab)
        self.actionPlan_routes.triggered.connect(self.add_route_plan_tab)
        self.actionAbout_Rousettus.triggered.connect(self.show_about)
        self.actionplan_test.triggered.connect(self.add_flight_generate_tab)

        # Add config events
        # self.closeEvent.connect(self.store_config)

    def enable_functions(self, menu_flags):
        if menu_flags['data processing'][0]:
            self.data_processing_menu.setEnabled(True)
            if menu_flags['data processing'][1]['magnetic data'][0]:
                self.menuMagnetic_Data.setEnabled(True)
                if menu_flags['data processing'][1]['magnetic data'][1]['variation calculate'][0]:
                    self.actionVariation_calculate.setEnabled(True)

    def show_about(self):
        about_dialog = AboutHandle(self)
        about_dialog.show()

    # Add tabs functions
    # TODO make general function for adding tab (call signal name = "user" button.clicked.connect(lambda: calluser(name)))
    def add_tab(self, tab_class, tab_name, section_name):
        pass

    def add_variation_calculate_tab(self):
        variation_calculate_widget = VariationCalculateHandle(self, self.progressBar)
        self.variation_calculate_tab = self.tabWidget.addTab(variation_calculate_widget, 'Variation Calculate')

    # TODO add route plan tab
    def add_route_plan_tab(self):
        tab_name = 'Route Plan'
        section_name = 'route_plan'
        if self.debug:
            print(r'self.tab_exist_flags.get("Route Plan", 0) == 0 ', self.tab_exist_flags.get(tab_name, 0) == 0)
        if self.tab_exist_flags.get(tab_name, 0) == 0:
            if self.debug:
                print("RousettusMain current config: ", self.rousettus_config)
            route_plan_wiget = RoutePlanHandle(main_window=self, config=self.rousettus_config)
            self.tabWidget.addTab(route_plan_wiget, tab_name)
            self.tab_exist_flags[tab_name] = 1
            self.tabWidget.setCurrentWidget(route_plan_wiget)
            if 'TABS' not in self.rousettus_config:
                # print('TABS not in config')
                self.rousettus_config['TABS'] = {}
            if isinstance(self.tabWidget.currentWidget(), Configurable) and \
                    (self.tabWidget.currentWidget().section_name is not None):
                self.rousettus_config['TABS'][self.tabWidget.currentWidget().section_name] = str(True)
        else:
            for i in range(self.tabWidget.count()):
                if self.debug:
                    print("self.tabWidget.widget(i).section_name ", i, self.tabWidget.widget(i).section_name,
                          'section_name ', section_name)
                    print("self.tabWidget.widget(i).section_name == section_name ",
                          self.tabWidget.widget(i).section_name == section_name)
                if self.tabWidget.widget(i).section_name == section_name:
                    self.tabWidget.setCurrentWidget(self.tabWidget.setCurrentIndex(i))
                    break
            if self.debug:
                print("self.tabWidget.count() ", self.tabWidget.count())

    def add_flight_generate_tab(self):
        tab_name = 'Flight Plan'
        section_name = 'flight_plan'
        if self.debug:
            print(r'self.tab_exist_flags.get("Flight Plan", 0) == 0 ', self.tab_exist_flags.get(tab_name, 0) == 0)
        if self.tab_exist_flags.get(tab_name, 0) == 0:
            flight_planning_widget = FlightPlanningHandle(main_window=self).set_config(self.rousettus_config)
            self.tabWidget.addTab(flight_planning_widget, tab_name)
            self.tab_exist_flags[tab_name] = 1
            self.tabWidget.setCurrentWidget(flight_planning_widget)
            if 'TABS' not in self.rousettus_config:
                # print('TABS not in config')
                self.rousettus_config['TABS'] = {}
            if isinstance(self.tabWidget.currentWidget(), Configurable) and \
                    (self.tabWidget.currentWidget().section_name is not None):
                self.rousettus_config['TABS'][self.tabWidget.currentWidget().section_name] = str(True)
        else:
            for i in range(self.tabWidget.count()):
                if self.debug:
                    print("self.tabWidget.widget(i).section_name ", i, self.tabWidget.widget(i).section_name,
                          'section_name ', section_name)
                    print("self.tabWidget.widget(i).section_name == section_name ",
                          self.tabWidget.widget(i).section_name == section_name)
                if self.tabWidget.widget(i).section_name == section_name:
                    self.tabWidget.setCurrentWidget(self.tabWidget.setCurrentIndex(i))
                    break

    def add_flaght_planning_tab(self):
        if self.tab_exist_flags.get('Flight planning', 0) == 0:
            flight_planning_widget = FlightPlanningHandle(self, logger=self.logger, main_window=self)
            self.tabWidget.addTab(flight_planning_widget, 'Flight Planning')
            self.tab_exist_flags['Flight Planning'] = 1
            self.tabWidget.setCurrentWidget(flight_planning_widget)
        else:
            self.tabWidget.setCurrentWidget(self.tabWidget.findChild(QWidget, 'Flight Planning'))

    def add_profile_generate_tab(self):
        if self.tab_exist_flags.get('Profile Generate', 0) == 0:
            # print('tabs in config: ', 'TABS' in self.rousettus_config)
            if 'TABS' not in self.rousettus_config:
                # print('TABS not in config')
                self.rousettus_config['TABS'] = {}
            profile_generate_widget = ProfileGenerateHandle(self, logger=self.logger,
                                                            main_window=self,
                                                            config=self.rousettus_config)
            self.tabWidget.addTab(profile_generate_widget, 'Profile Generate')
            self.tab_exist_flags['Profile Generate'] = 1
            self.tabWidget.setCurrentWidget(profile_generate_widget)
            if isinstance(self.tabWidget.currentWidget(), Configurable) and \
                    (self.tabWidget.currentWidget().section_name is not None):
                self.rousettus_config['TABS'][self.tabWidget.currentWidget().section_name] = str(True)
        else:
            self.tabWidget.setCurrentWidget(self.tabWidget.findChild(QWidget, 'Profile Generate'))
            # TODO Не работает активация таба, починить. Find child возвращает 0
            print(self.tabWidget.findChild(QWidget, 'Profile Generate'))

    def add_tab(self, tab_class, tab_name):
        section_name = tab_class.section_name
        if self.debug:
            print("current tab_exist_flags = {}".format(self.tab_exist_flags))
        if self.tab_exist_flags.get(section_name, 0):
            for i in range(self.tabWidget.count()):
                if self.tabWidget.widget(i).section_name == tab_class.section_name:
                    self.tabWidget.setCurrentWidget(self.tabWidget.setCurrentIndex(i))
                    break
        else:
            tab_widget = tab_class(main_window=self)
            if isinstance(tab_widget, Configurable):
                self.add_saving_children(tab_widget.get_config())
            self.tabWidget.addTab(tab_widget, tab_name)
            self.tab_exist_flags[section_name] = 1
            self.tabWidget.setCurrentWidget(tab_widget)
            if 'TABS' not in self.config.keys():
                self.config['TABS'] = {}
            if section_name not in self.config['TABS'].keys():
                self.config['TABS'][section_name] = {}
            if section_name:
                self.config['TABS'][section_name]['is_open'] = True

    def closeTab(self, currentIndex):
        if self.debug:
            print("closing wiget is {}, profile generate type is {}".format(self.tabWidget.tabText(currentIndex),
                                                                            type(self.tabWidget.tabText(currentIndex))))
        self.tab_exist_flags['{}'.format(self.tabWidget.tabText(currentIndex))] = 0
        if isinstance(self.tabWidget.currentWidget(), Configurable):
            self.rousettus_config['TABS'][self.tabWidget.currentWidget().section_name] = str(False)
            self.tabWidget.widget(currentIndex).store_config()
        self.tabWidget.widget(currentIndex).close()
        self.tabWidget.removeTab(currentIndex)
        if self.debug:
            print("close_tab func, after delete = {}".format(self.tab_exist_flags))
        self.store_config()
        QgsProject.instance().write()

    def initGui(self):
        # print('Main window init gui')
        # print('main window before get current path')
        self.prj_name, self.current_project_path, self.prj_full_path = get_current_project_name()
        # print('main window prj name {}, current path {}, prj_full_path {}'.format(self.prj_name,
        #                                                                           self.current_project_path,
        #                                                                           self.prj_full_path))
        self.label_prj_name.setText(self.prj_name)
        self.label_prj_name.setToolTip(self.prj_name)
        width = self.label_prj_name.fontMetrics().boundingRect(self.label_prj_name.text()).width()
        self.label_prj_name.setFixedWidth(width + 5)

        self.label_prj_path.setText(self.current_project_path)
        self.label_prj_path.setToolTip(self.current_project_path)

    # slot for project changed signal
    def prj_changed(self):
        self.initGui()
        tab_widget_count = self.tabWidget.count()
        for i in range(tab_widget_count):
            self.tabWidget.widget(i).initGui()

        if (len(self.current_project_path.strip()) != 0):
            QgsMessageLog.logMessage("{}. {}".format('main', "project {} loaded".format(self.prj_name)),
                                     "Rousettus_Tool",
                                     level=Qgis.Info)

    # Config store and load
    # load config function
    def load_config(self):
        # if False:
        #     print('in load_config func')
        self.rousettus_config.read(self.rousettus_config_file)
        # print(self.rousettus_config)
        # if False and 'TABS' in self.rousettus_config:
        #     print('try to get TABS, profile_generate: ', self.rousettus_config['TABS'].getboolean("profile_generate", fallback = False))
        if 'TABS' in self.rousettus_config and self.rousettus_config['TABS'].getboolean("profile_generate",
                                                                                        fallback=False):
            self.add_profile_generate_tab()
        if 'TABS' in self.rousettus_config and self.rousettus_config['TABS'].getboolean("flight_plan",
                                                                                        fallback=False):
            self.add_flight_generate_tab()
        if 'TABS' in self.rousettus_config and self.rousettus_config['TABS'].getboolean("route_plan", fallback=False):
            self.add_route_plan_tab()

    # store config
    def store_config(self):
        for tab_index in range(self.tabWidget.count()):
            self.tabWidget.widget(tab_index).store_config()
        with open(self.rousettus_config_file, 'w') as config_file:
            self.rousettus_config.write(config_file)
        # if self.debug:
        #     print('config sections: ', self.rousettus_config.sections())

    def closeEvent(self, *args, **kwargs):
        # print('close call')
        self.store_config()
        QgsProject.instance().write()
