# -*- coding: utf8 -*-
# board
# helper class for cuatro
# Alfredo Martin 2021

version = 'board.v.1.0.0'

import numpy as np
from rotate import Rotate


class Board:
    """the instance of this class represents the board
    instance attributes:
    rotor: instance of Rotor class
    colors: tuple of two tuples of three ints
    edge_colors: tuple of two tuples of three ints
    size: int: size of the game
    width: int: size of the cube
    height: int: how much tall is the cube
    space: int: space beteen board positions
    midpoint: numpy array: midpoint of the board
    delta: int: space - width
    colors3d: numpy array
    polygons3d: numpy array
    edge_colors3d: numpy array

    """

    def __init__(self, state=None, width=100, space=200, height=10,
                 colors=((0, 0, 0), (150, 150, 150)), edge_colors=((255, 255, 255), (255, 255, 255))):
        """state: instance of State class
        offset: list of int: offset in each of the three dimensions
        width: int: width of the checker
        height: int: height of the checkers
        space: int: space between checkers
        color: tuple of tuples of 3 int: color of the polygons
        edge_colors: tuple of tuples of 3 int: color of the edges of the polygons"""
        self.rotor = Rotate()
        self.size = state.size
        self.width = width
        self.space = space
        self.height = height
        self.colors = colors
        self.edge_colors = edge_colors
        cube = []
        cube.append([[0., 0., 0.],
                     [0., 1., 0.],
                     [0., 1., 1.],
                     [0., 0., 1.]])
        cube.append([[1., 0., 0.],
                     [1., 1., 0.],
                     [1., 1., 1.],
                     [1., 0., 1.]])
        cube.append([[0., 0., 0.],
                     [1., 0., 0.],
                     [1., 0., 1.],
                     [0., 0., 1.]])
        cube.append([[0., 1., 0.],
                     [1., 1., 0.],
                     [1., 1., 1.],
                     [0., 1., 1.]])
        cube.append([[0., 0., 0.],
                     [1., 0., 0.],
                     [1., 1., 0.],
                     [0., 1., 0.]])
        cube.append([[0., 0., 1.],
                     [1., 0., 1.],
                     [1., 1., 1.],
                     [0., 1., 1.]])
        self.delta = self.space - self.width
        self.midpoint = self.size * self.space / 2.
        self.midpoint = np.array([0., -self.midpoint, -self.midpoint]).reshape(1, 1, 3)
        self.bcube3d = np.array(cube)
        self.bcube3d *= np.array([self.height, self.width, self.width]).reshape(1, 1, 3)
        self.bcube3d += np.array([-self.height, self.delta, self.delta]).reshape(1, 1, 3)
        # translates the cubes to its position
        self.polygons3d = None
        self.colors3d = None
        self.edge_colors3d = None
        self.get_polygons3d(0.)  # gives value to self.cubes3d

    def get_polygons3d(self, a):
        """this method creates the 3d polygons corresponding to the state of the game as long with the corresponding
        filling colors for each polygon and the color of the edges (both depending on the player they belong to)
        the self.polygons3d is a numpy array of shape (n, 4, 3) being n the number of polygons
        the self.colors3d is a numpy array of shape (n, 3)
        the self.edge_colors3d is a numpy array of shape (n, 3)
        """
        self.polygons3d = []
        self.colors3d = []
        self.edge_colors3d = []
        for i in range(self.size):
            for j in range(self.size):
                index_tuple = (0, i, j)
                self.polygons3d.append(self.bcube3d + self.midpoint + np.array(index_tuple) * self.space)
                self.colors3d.append([self.colors[0] for _ in range(6)])
                self.edge_colors3d.append([self.edge_colors[0] for _ in range(6)])
        # concatenate all the cubes
        self.polygons3d = np.concatenate(self.polygons3d, axis=0)
        self.colors3d = np.array(self.colors3d).reshape(-1, 3)
        self.edge_colors3d = np.array(self.edge_colors3d).reshape(-1, 3)


if __name__ == '__main__':
    print(version)
