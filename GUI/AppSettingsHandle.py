# coding=utf-8
from PyQt5.QtWidgets import QDialog

from UI.Settings.AppSettingsDialog_ui import Ui_AppSettingsDialog
from tools.AppSettings import AppSettings


class AppSettingsHandle(Ui_AppSettingsDialog, QDialog):
    """
Hendle for settings dialog window
    """
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.settings = AppSettings.get_settings()
        self.debug_checkBox.setChecked(self.settings.get_option('DEBUG', False))

        self.buttonBox.accepted.connect(self.ok_button_pushed)

    def ok_button_pushed(self):
        self.settings.set_option('DEBUG', (self.debug_checkBox.isChecked()))
        self.settings.store_settings()