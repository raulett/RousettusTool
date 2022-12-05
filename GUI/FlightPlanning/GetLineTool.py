import math

from PyQt5.QtCore import pyqtSignal, QPoint, Qt
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapCanvasSnappingUtils
from qgis.core import QgsSnappingUtils, QgsPointLocator
from PyQt5.QtGui import QCursor, QPixmap, QColor


# QgsMapTool is abstract. Need you to override methods
class GetLineTool(QgsMapTool):
    debug = 0

    line_found_signl = pyqtSignal(object)
    decline_signal = pyqtSignal()

    def __init__(self, canvas, current_layer):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.layer = current_layer
        self.r_band = QgsRubberBand(self.canvas)
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                       "      c None",
                                       ".     c #FF0000",
                                       "+     c #FFFFFF",
                                       "                ",
                                       "       +.+      ",
                                       "      ++.++     ",
                                       "     +.....+    ",
                                       "    +.     .+   ",
                                       "   +.   .   .+  ",
                                       "  +.    .    .+ ",
                                       "        .       ",
                                       " ... ...+... ...",
                                       "        .       ",
                                       "        .       ",
                                       "   +.   .   .+  ",
                                       "   ++.     .+   ",
                                       "    ++.....+    ",
                                       "        .       ",
                                       "        .       "]))

    def canvasPressEvent(self, event):
        pass

    def canvasMoveEvent(self, event):
        pass

    # event is QgsMapMouseEvent
    def canvasReleaseEvent(self, event):
        if event.button()==Qt.RightButton:
            self.deactivate()
            return

        click_x = event.pos().x()
        click_y = event.pos().y()



        if (self.layer != None):
            clicked_point = QPoint(click_x, click_y)

            map_snapper = QgsMapCanvasSnappingUtils(self.canvas)
            point_locator = map_snapper.snapToCurrentLayer(clicked_point, QgsPointLocator.Edge)
            line_points = point_locator.edgePoints()
            if len(line_points)>=2:
                self.r_band.reset()
                color = QColor(255, 0, 0)
                self.r_band.setColor(color)
                self.r_band.setWidth(2)
                self.r_band.addPoint(line_points[0])
                self.r_band.addPoint(line_points[1])
                self.r_band.show()
                if self.debug:
                    print("GetLineTool, line_points type: {}".format(type(line_points[0])))
                azimuth = line_points[0].azimuth(line_points[1])
                # tg = (line_points[0].y() - line_points[1].y())/(line_points[0].x() - line_points[1].x())
                # if self.debug:
                #     print("GetLineTool, tg = {}".format(tg))
                # azimuth = (180/math.pi)*math.atan(tg)
                if self.debug:
                    print(azimuth)
                self.line_found_signl.emit([azimuth])
                if self.debug:
                    print("point_locator.edgePoints_1: {}, point_locator.edgePoints_2: {}".format(point_locator.edgePoints()[0], point_locator.edgePoints()[1]))
                    # print("point_locator.point(): {}".format(point_locator.point()))
                    # print("current x: {}, current y: {}, btn: {}".format(clicked_point.x(), clicked_point.y(), event.button()))

    def activate(self):
        self.canvas.setCursor(self.cursor)

    def deactivate(self):
        self.canvas.setCursor(QCursor())
        self.r_band.reset()
        self.decline_signal.emit()

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True

    def add_flight_profiles_layer(self, azimuth, polygon):
        pass