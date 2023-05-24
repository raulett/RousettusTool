from PyQt5.QtCore import QThread, pyqtSignal
from ...tools.FlightPlanningLib.FlightRouteGenerator import FlightRouteGenerator


class QThreadFlightRouteGenerator(QThread, FlightRouteGenerator):
    finish_signal = pyqtSignal()
    def __init__(self):
        super(QThread).__init__()

    def run(self):
        pass

    def set_a(self):
        self.run = self.a()

    def set_b(self):
        self.run = self.b()
