import numpy as np
import math


class AffilneTransform:
    debug = 1
    def __init__(self, rotation_angle):
        self.affine_shift = np.array([0,0], float)
        self.rotation_matrix = np.matrix([[math.cos(rotation_angle), math.sin(rotation_angle)],
                                          [-1*math.sin(rotation_angle), math.cos(rotation_angle)]],
                                         float)

    def set_shift_vector(self, shift_vector):
        self.affine_shift[0] = shift_vector[0]
        self.affine_shift[1] = shift_vector[1]

    def transform_geom(self, geometry):
        pass
