# coding=utf-8
import json
import os.path
import pathlib

from PyQt5.QtCore import pyqtSignal, QObject


class AppSettings(QObject):
    """
    Синглтон. Объект для хранения настроек приложения. Они сохраняются в json файл в папке приложения. Экземпляр
    возвращается вызовом "get_settings".

    Singleton. An object for storing application settings. They are saved to a json file in the application folder.
    The instance is returned by calling "get_settings".
    """
    _instance = None
    app_settings_changed_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._settings = {}
        self.settings_file = pathlib.Path(os.getenv("ROUSETTUS_ROOT")) / 'rousettus_config.json'
        if self.settings_file.exists():
            with open(self.settings_file, 'r') as settings_file:
                self._settings = json.loads(settings_file.read())

    @classmethod
    def get_settings(cls):
        """
return single instance of class
        :return:
        """
        if cls._instance is None:
            cls._instance = AppSettings()

        return cls._instance

    def set_option(self, option: dict, value):
        """

        :param option:
        :param value:
        """
        self._settings[option] = value
        self.app_settings_changed_signal.emit()

    def get_option(self, option: str, default=None):
        return self._settings.get(option, default)

    def store_settings(self):
        """
save settings call
        """
        with open(self.settings_file, 'w') as settings_file:
            settings_file.write(json.dumps(self._settings))
