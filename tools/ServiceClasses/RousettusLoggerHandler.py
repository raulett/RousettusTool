# coding=utf-8
import logging
import os
import pathlib

from tools.AppSettings import AppSettings
from tools.ServiceClasses.LoggingListModel import LoggingListModel


class RousettusLoggerHandler:
    _instance = None

    def __init__(self):
        self.logger = logging.getLogger('rousettus')
        self.logger.setLevel(logging.DEBUG)
        self.logging_list_model = LoggingListModel()
        print(os.environ.get('ROUSETTUS_ROOT'))

        formatter = logging.Formatter("%(asctime)s\t%(levelname)s\t%(filename)s\t%(message)s")

        file_handler = logging.FileHandler(pathlib.Path(os.environ.get('ROUSETTUS_ROOT')) / 'rousettus.log',  mode='a')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.WARNING)
        log_list_handler = LoggerListHandler(self.logging_list_model)
        log_list_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(log_list_handler)
        self.set_log_level()

    def set_log_level(self):
        """
Slot to renew log list model log level. File log level is constant.
        """
        if AppSettings.get_settings().get_option('DEBUG', False):
            for handler in self.logger.handlers:
                if isinstance(handler, LoggerListHandler):
                    handler.setLevel(logging.DEBUG)
                    handler.setFormatter(logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s"
                                                           "\t%(filename)s\t%(lineno)s"))
        else:
            for handler in self.logger.handlers:
                if isinstance(handler, LoggerListHandler):
                    handler.setLevel(logging.INFO)
                    handler.setFormatter(logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s"))

    @classmethod
    def get_handler(cls):
        if cls._instance is None:
            cls._instance = RousettusLoggerHandler()
        return cls._instance

    def get_model(self):
        return self.logging_list_model


class LoggerListHandler(logging.Handler):
    def __init__(self, model: LoggingListModel):
        super().__init__()
        self.model = model

    def emit(self, record):
        self.model.add_data(self.format(record))