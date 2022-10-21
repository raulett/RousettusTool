from qgis.core import QgsProject
import re
import os


#функционал для получения текущего имени проекта и пути к нему
def get_current_project_name():
    current_project_path = ''
    prj_full_path = ''
    prj_name = ''

    if QgsProject.instance().fileName() != '':
        prj_full_path = QgsProject.instance().fileName().replace('/', '\\')
    if re.match('geopackage', prj_full_path) != None:
        re.findall('projectName=(\w+)', prj_full_path)
        try:
            prj_name = re.findall('projectName=(\w+)', prj_full_path)[0]
        except:
            # TODO Написать логгинг ошибки, что если подстроки 'projectName=' вообще нет.
            pass
    else:
        prj_name = os.path.basename(QgsProject.instance().fileName()).split('.')[0]
    if QgsProject.instance().readPath("./") != './':
        current_project_path = QgsProject.instance().readPath("./").replace('/', '\\')



    return prj_name, current_project_path, prj_full_path

