import numpy as np
import math, statistics

from qgis.core import QgsGeometry, QgsPoint, QgsPointXY

class AffilneTransform:
    debug = 0
    def __init__(self, rotation_angle):
        self.affine_shift = np.array([0,0], float)
        self.rotation_angle = rotation_angle
        self.rotation_matrix = np.matrix([[math.cos(rotation_angle), math.sin(rotation_angle)],
                                          [-1*math.sin(rotation_angle), math.cos(rotation_angle)]],
                                         float)

    def set_shift_vector(self, shift_vector):
        self.affine_shift[0] = shift_vector[0]
        self.affine_shift[1] = shift_vector[1]

    def shift_geom(self, geometry):
        result_points = 'Multipoint ('
        for vertex in geometry.vertices():
            point = QgsPoint()
            point.setX(vertex.x() + self.affine_shift[0])
            point.setY(vertex.y() + self.affine_shift[1])
            result_points = result_points + '{} {}, '.format(point.x(), point.y())
        result_points = result_points[:len(result_points) - 2] + ')'
        output_geom = QgsGeometry().fromWkt(result_points).convertToType(geometry.type())
        return output_geom

    def transform_geom(self, geometry):
        minX_val = statistics.median([vertex.x() for vertex in geometry.vertices()])
        minY_val = statistics.median([vertex.y() for vertex in geometry.vertices()])
        rotated_geometry = QgsGeometry(geometry)
        rotated_geometry.rotate(self.rotation_angle, QgsPointXY(minX_val, minY_val))
        for vertex in geometry.vertices():
            if self.debug == 1:
                print("from AffineTransform.transform_geom vertex: {}".format(vertex))

            rotated_arr = np.dot(self.rotation_matrix,
                                 np.array([vertex.x() - minX_val, vertex.y() - minY_val], float).reshape(2, 1))
            # rotated_arr = np.array(self.rotation_matrix.dot(np.array([vertex.x(), vertex.y()], float).reshape(2, 1)))
            if self.debug == 1:
                print("from AffineTransform.transform_geom rotated_lst: {}".format(rotated_arr))
                print("from AffineTransform.transform_geom rotated_lst type, and shape: {}".format(type(rotated_arr),
                                                                                                   rotated_arr.shape))
                print("from AffineTransform.transform_geom rotated_arr[0], {}".format(float(rotated_arr[0])))
            point = QgsPoint()
            point.setX(float(rotated_arr[0]) + minX_val)
            point.setY(float(rotated_arr[1]) + minY_val)
            if self.debug == 1:
                print("from AffineTransform.transform_geom current point: {}".format(point.asWkt()))
            result_points = result_points + '{} {}, '.format(point.x(), point.y())

        result_points = result_points[:len(result_points) - 2] + ')'
        output_geom = QgsGeometry().fromWkt(result_points).convertToType(geometry.type())
        if self.debug == 1:
            print("from AffineTransform.transform_geom result geometry: {}".format(output_geom.asWkt()))
        return output_geom