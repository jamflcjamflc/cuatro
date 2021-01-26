# -*- coding: utf8 -*-
# draw
# helper class for cuatro
# Alfredo Martin 2021

import pygame

version = 'draw.v.1.0.0'


class Draw:
    """the instance of this class draws a set of polygons in the screen  and applies shading
    instance attributes:
    max_shading: float: maximum ratio of shading applied"""

    def __init__(self, max_shading=0.1):
        """initiallizes the instance
        max_shading: float: percentage of the color that is shaded when not directly illuminated"""
        self.max_shading = max_shading

    def draw(self, screen, arr, colors, edge_colors, shading):
        """
        draws a set of polygons into the screen
        screen: pygame screen object
        arr: numpy array of shape (n, m, 3) containing n polygons of m edges
        clors: numpy array of shape(n, 3) containing rgb color codes for n polygons
        edge_colors: numpy array of shape (n, 3) containing rgb edge color codes for n polygons
        returns screen"""
        pcolors = (colors * (1 - self.max_shading) + colors * self.max_shading * shading.reshape(-1, 1)).astype('int16')
        for polygon, color, edge_color in zip(arr, pcolors, edge_colors):
            coords = [tuple(node) for node in polygon]
            color_rgb = tuple(color)
            edge_color_rgb = tuple(edge_color)
            pygame.draw.polygon(screen, color_rgb, coords)
            pygame.draw.polygon(screen, edge_color_rgb, coords, 1)
        return screen

if __name__ == '__main__':
    print(version)
