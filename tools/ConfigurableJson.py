import json
from abc import abstractmethod


class ConfigurableJson:
    """
    Класс, предназначеный для сохранения и восстановления состояния полей формы Qt.
    """
    def __init__(self):
        self.section_name = None
        self.config = None
        self.configurable_children = []

    @abstractmethod
    def save_state(self) -> json:
        """
        Сохраняет состояние полей формы Qt.
        """
        pass

    @abstractmethod
    def load_state(self):
        """
        Восстанавливает состояние полей формы Qt.
        """
        pass
