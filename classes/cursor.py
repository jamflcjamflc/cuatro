# -*- coding: utf8 -*-
# cursor
# helper class for cuatro
# Alfredo Martin 2021

version = 'cursor.v.1.0.0'

import numpy as np
from rotate import Rotate


class Cursor:
    """the instance of this class defines a cube that acts as a cursor
    instance attributes:
    rotor: instance of Rotor class
    pos: tuple of two ints
    colors: tuple of two tuples of three ints
    edge_colors: tuple of two tuples of three ints
    size: int: size of the game
    width: int: size of the cube
    space: int: space beteen board positions"""

    def __init__(self, state=None, width=100, space=200,
                 colors=((255, 255, 255), (255, 255, 255)), edge_colors=((255, 0, 0), (0, 255, 0))):
        """state: instance of State class
        offset: list of int: offset in each of the three dimensions
        width: int: width of the checker
        space: int: space between the center of two adjacent checkers
        colors: tuple of colors for player 1 and player 2
        edge_colors: tuple of colors for edges in player 1 and player 2
        bcube3d: numpy array: unit cube
        polygons3d: numpy array: represents the polygons of the cube
        colors3d: numpy array: represents the colors of each polygn
        edge_colors3d: numpy array: represents the colors of the edges

        """
        self.rotor = Rotate()
        self.pos = (0, 0)  # tuple indicating the current position of the cursor
        self.colors = colors
        self.edge_colors = edge_colors
        self.size = state.size
        self.width = width
        self.space = space
        delta = space - width
        midpoint = self.size * space / 2
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
        # next we resize the cube
        self.bcube3d = np.array(cube)
        self.bcube3d *= np.array([self.width, self.width, self.width]).reshape(1, 1, 3)
        self.bcube3d += np.array([0., delta, delta]).reshape(1, 1, 3)
        self.bcube3d += np.array([0., -midpoint, -midpoint]).reshape(1, 1, 3)
        self.polygons3d = None
        self.colors3d = None
        self.edge_colors3d = None
        self.get_polygons3d(state)
        # translates the cube to its position

    def get_polygons3d(self, state):
        """this method creates the 3d polygons corresponding to the state of the game as long with the corresponding
        filling colors for each polygon and the color of the edges (both depending on the player they belong to).
        the self.polygons3d is a numpy array of shape (6, 4, 3)
        state: int: instance of state class"""
        self.polygons3d = []
        self.colors3d = []
        self.edge_colors3d = []
        player = state.next_turn
        index_tuple = (state.play[self.pos], self.pos[0], self.size - self.pos[1] - 1)
        self.polygons3d = (self.bcube3d + np.array(index_tuple) * self.space)
        self.colors3d = np.array([self.colors[player - 1] for _ in range(6)])
        self.edge_colors3d = np.array([self.edge_colors[player - 1] for _ in range(6)])


if __name__ == '__main__':
    print(version)

