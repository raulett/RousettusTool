import os.path
import datetime

from qgis.core import QgsMessageLog
from ...tools.get_current_project_name import get_current_project_name
from qgis.core import Qgis

# Massege levels:
# Qgis.Info - Information message.
# Qgis.Warning - Warning message.
# Qgis.Critical - Critical/error message.
# Qgis.Success - Used for reporting a successful operation.
# Qgis.NoLevel - No level.
class LoggerQgis:
    debug = 0
    def __init__(self):
        self.error_levels = ['INFO', 'WARNING', 'CRITICAL', 'SUCCESS', 'NOLEVEL']
        self.prj_name, self.current_project_path, self.prj_full_path = get_current_project_name()
        if self.debug:
            print("Logger: " + self.current_project_path)

    def log_msg(self, massage, module_tag, level=Qgis.Info):
        logfile_path = os.path.join(self.current_project_path, 'rousettus.log')
        try:
            with open(logfile_path, 'a') as logfile:
                logfile.write('{}\t{}\t{}\t{}\n'.format(datetime.datetime.now().strftime("%d.%m.%YT%H:%M:%S"),
                                                        module_tag,
                                                        self.error_levels[int(level)], massage))
        except OSError:
            QgsMessageLog.logMessage("Error opening file: {}".format(logfile_path), "Rousettus_Tool", level=Qgis.Critical)
        QgsMessageLog.logMessage("{}. {}".format(module_tag, massage), 'Rousettus_Tool', level=level)