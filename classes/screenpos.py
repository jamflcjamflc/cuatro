# -*- coding: utf8 -*-
# board
# helper class for cuatro
# Alfredo Martin 2021

version = 'wscreenpos.v.1.0.0'

import numpy as np


class ScreenPos:
    """the instance of this class generates a 2d coordinates array from a 3d coordinates array given the position
    of the camera, its angle and the position of the projection screen.
    attributes of the instance:
    offset: numpy array: displacement to reposition the objects in 2d with respect to the horizon
    c: numpy array: position of the camera
    e: numpy array: position of the screen ahead the camera
    rot: numpy array: rotation matrix of the camera (this implementation does not rotate the camera)
    rotate_camera: bool: whether to rotate the camera or not
    """

    def __init__(self, c=(500., 0., 0.), t=(0., 0., 0.), e=(0., 0., 100.),
                 height=0, width=0, horizon=0.3):
        """initiallizes the instance
        c: tuple of three floats: position of the camera
        t: tuple of 3 floats: orientation of the camera (three angles in radians)
        e: tuple of three floats: position of the screen (in front of the camera but behind the scene)
        height: int: height of the screen
        width: int: width of the screen
        horizon: float: position of the horizon with respect to the height of the screen
        """
        self.offset = np.array([int(width / 2), int(horizon * height)]).reshape(1, 1, 2)
        self.c = np.array(c).reshape(1, 1, 3)
        self.e = np.array([[1., 0., 0., 0.],
                           [0., 1., 0., 0.],
                           [-e[0] / e[2], -e[1] / e[2], 0., -1 / e[2]],
                           [0., 0., 0., 1.]])
        rot1 = np.array([[1, 0, 0],
                         [0, np.cos(t[0]), -np.sin(t[0])],
                         [0, np.sin(t[0]), np.cos(t[0])]])
        rot2 = np.array([[np.cos(t[1]), 0, np.sin(t[1])],
                         [0, 1, 0],
                         [-np.sin(t[1]), 0, np.cos(t[1])]])
        rot3 = np.array([[np.cos(t[2]), -np.sin(t[2]), 0],
                         [np.sin(t[2]), np.cos(t[2]), 0],
                         [0, 0, 1]])
        if (np.array(t) == 0.0).sum() == 3:
            self.rotate_camera = True
        else:
            self.rotate_camera = False
        self.rot = np.dot(rot1, rot2)
        self.rot = np.dot(self.rot, rot3)

    def pos(self, arr=None):
        """arr: numpy array of shape (n,m,3) with:
                m: number of polygons
                n: the number of nodes in each polygon
        returns: b: numpy array of shape (n,m,2) containing integer 2d coordinates of the scene nodes in the
        screen"""
        if len(arr.shape) == 1:
            a = arr.reshape(1, 1, 3)
        elif len(arr.shape) == 2:
            a = arr.reshape(1, arr.shape[0], 3)
        else:
            a = np.copy(arr)
        n, m, _ = a.shape
        d = a - self.c  # shape (n,m,3)
        #d = np.matmul(d, self.rot)  # shape (n,m,3)
        if self.rotate_camera:
            d = np.matmul(d, self.rot)  # shape (n,m,3)
        ones = np.ones((n, m, 1))  # shape(n, m, 1)
        d = np.concatenate([d, ones], axis=2)  # shape (n, m, 4)
        f = np.matmul(d, self.e)  # shape (n,m,4)
        bx = f[:, :, 0] / f[:, :, 3]
        by = f[:, :, 1] / f[:, :, 3]
        bx = bx.reshape(n, m, 1)
        by = by.reshape(n, m, 1)
        b = np.concatenate([-by, bx], axis=2)  # shape (n,m,2) (y goes to x and x goes to y)
        b = b.astype('int32')
        b = self.offset + b
        return b

if __name__ == '__main__':
    print(version)
