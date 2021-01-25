# -*- coding: utf8 -*-
# rotate
# helper class for cuatro

version = 'rotate.v.1.0.0'

import numpy as np


class Rotate:

    def __init__(self):
        self.success = True

    def rotate(self, angles=None, arr=None):
        """
        angles: tuple of three floats (angles in radians)
        arr: numpy array of shape (n,m,3)"""
        a, b, g = angles
        self.rota = np.array([[1, 0, 0],
                              [0, np.cos(a), -np.sin(a)],
                              [0, np.sin(a), np.cos(a)]])
        self.rotb = np.array([[np.cos(b), 0, np.sin(b)],
                              [0, 1, 0],
                              [-np.sin(b), 0, np.cos(b)]])
        self.rotg = np.array([[np.cos(g), -np.sin(g), 0],
                              [np.sin(g), np.cos(g), 0],
                              [0, 0, 1]])
        self.rot = np.dot(self.rota, self.rotb)
        self.rot = np.dot(self.rot, self.rotg)
        newarr = np.matmul(arr, self.rot)
        return newarr


if __name__ == '__main__':
    print version