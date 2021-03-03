# -*- coding: utf8 -*-
# get2dcoords
# helper class for cuatro
# Alfredo Martin 2021

import numpy as np
from classes.rotate import Rotate

version = 'get2dcoords.v.1.0.0'


class Get2dcoords:
    """the instance of this class reorganizes polygons and colors into data that is ready to be rendered
    in 2d:
    ligt_pos: numpy array: position of the light
    polygons3d: numpy array of shape (n, m, 3) with n being the number of polygons and m the number of nodes
                per polygon
    rotor: Instance of Rotor class
    offset: tuple of three ints: offset (displacement in the positve z axis) of the giver 3d coords before being
                rendered
    screenpos: instance of screenpos class
                """

    def __init__(self, light_pos=(0., 0., 0.), offset=None, screenpos=None):
        """ Initiallizes the instance
        light_pos: position of the light source
        offset: tuple of three iints indicating where to translate the polygons before rendering
        screenpos: instance of screenpos class"""
        self.light_pos = np.array(light_pos)
        self.polygons3d = None
        self.rotor = Rotate()
        self.offset = offset
        self.screenpos = screenpos

    def get_polygons2d(self, polygons3d=None, colors=None, edge_colors=None, angles=None):
        """gets 2d coords from 3d coords and returns the 2d coords along the colors in the 2d drawing order
        polgons3d: numpy array of shape (n, m, 3) with n being the number of polygons and m the number of nodes per polygon
        colors: numpy array of shape (n, 3)
        edge_colors: numpy array of shape (n, 3)
        angles: tuple of three angles (in radians)
        returns tuple of coordinates, colors, edge_colors and shading factor:
            coordinates: numpy array of shape (n, m, 2)
            colors: numpy array of shape (n, 3)
            edge_colors: numpy array of shape (n, 3)
            shading: numpy array of shape (n, )"""
        # Rotate the polygons
        self.polygons3d = self.rotor.rotate(angles,  arr=polygons3d)
        # translate the poligons
        self.polygons3d += np.array(self.offset).reshape(1, 1, 3)
        # get the sorting indexing for the polygons
        centroids = self.polygons3d.mean(axis=(1,))
        centroid_vectors = centroids - self.screenpos.c.reshape(1, 3)
        distances2 = (centroid_vectors ** 2).sum(axis=1)
        indexes = np.argsort(-distances2)  # sorting in reverse order
        # calculate shading of each polygon (cosine of angle formed by the vector orthogonal to the surface and the
        # vector joining the centroid and the camera)
        orto_vectors1 = self.polygons3d[:, 1, :] - self.polygons3d[:, 0, :]
        orto_vectors2 = self.polygons3d[:, 2, :] - self.polygons3d[:, 0, :]
        orto_vectors = np.cross(orto_vectors1, orto_vectors2, axis=1)
        orto_vectors /= np.linalg.norm(orto_vectors, axis=1).reshape(-1, 1)
        light_vectors = centroids - self.light_pos.reshape(1, 3)
        light_vectors /= np.linalg.norm(light_vectors, axis=1).reshape(-1, 1)
        cosine = np.abs(np.matmul(light_vectors.reshape(-1, 1, 3), orto_vectors.reshape(-1, 3, 1)).flatten())
        # calculate 2d coordinates
        coords = self.screenpos.pos(self.polygons3d)
        # sort the arrays
        coords = np.take(coords, indexes, axis=0)
        colors = np.take(colors, indexes, axis=0)
        edge_colors = np.take(edge_colors, indexes, axis=0)
        cosine = np.take(cosine, indexes, axis=0)
        return coords, colors, edge_colors, cosine

if __name__ == '__main__':
    print(verson)
