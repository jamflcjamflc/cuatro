# -*- coding: utf8 -*-
# game
# helper class for cuatro
# Alfredo Martin 2021

import numpy as np

version = 'game.v.1.0.0'

class Game:
    """controls the 3d visualization of the current game state
    instance attributes:
    colors: tuple of 2 tuples containing 3 ints: colors of the cube faces for each player
    edge_colots: tuple of 2 tuples containing 3 ints: colors of the edges of the cubes
    winning_colors: tuple of 2 tuples containing 3 ints: colors to highlight the faces of the winning diag
    size: int: size of the game (number of cubes in each side of the board)
    width: int: measure of the edge oif the cube
    space: int: measure of the distance between the center of the cubes
    bcube3d: numpy array defining a unit cube
    polygons3d: numpy array defining all the cubes
    colors3d: numpy array defining the colors of all faces
    edgecolors3d: numpy array defining the colors of all edges
    """

    def __init__(self, state=None, width=100, space=200,
                 colors=((255, 0, 0), (0, 255, 0)), edge_colors=((255, 255, 255), (255, 255, 255))):
        """state: instance of State class
        offset: list of int: offset in each of the three dimensions
        width: int: width of the checker
        height: int: height of the checkers
        space: int: space: int: space between the center of two adjacent checkers
        state: instance of State class
        colors: tuple of colors for player 1 and player 2
        edge_colots: tuple of colors for edges in player 1 and player 2"""
        self.colors = colors
        self.winning_colors = tuple(tuple(int(self.colors[i][j] / 2) for j in range(3)) for i in range(2))
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
        # translates the cube to its position
        self.polygons3d = None
        self.colors3d = None
        self.edge_colors3d = None
        self.get_polygons3d(state)  # gives value to self.cubes3d


    def get_polygons3d(self, state):
        """this method creates the 3d polygons corresponding to the state of the game as long with the corresponding
        filling colors for each polygon and the color of the edges (both depending on the player they belong to)
        the self.polygons3d is a numpy array of shape (n, 4, 3) being n the number of polygons
        the self.colors3d is a numpy array of shape (n, 3)
        the self.edge_colors3d is a numpy array of shape (n, 3)
        state: instacne of State class"""
        self.polygons3d = []
        self.colors3d = []
        self.edge_colors3d = []
        for index, player in enumerate(np.nditer(state.state)):
            if player > 0:
                index_tuple = np.unravel_index(index, state.state.shape)
                numpy_tuple = np.array([index_tuple[2], index_tuple[0], self.size - index_tuple[1] - 1])
                self.polygons3d.append(self.bcube3d + numpy_tuple * self.space)
                if state.winner > 0:
                    if index_tuple in state.winning_diag:
                        self.colors3d.append([self.winning_colors[player - 1] for _ in range(6)])
                    else:
                        self.colors3d.append([self.colors[player - 1] for _ in range(6)])
                else:
                    self.colors3d.append([self.colors[player - 1] for _ in range(6)])
                self.edge_colors3d.append([self.edge_colors[player - 1] for _ in range(6)])
        if len(self.polygons3d) > 0:
            self.polygons3d = np.concatenate(self.polygons3d, axis=0)
            self.colors3d = np.array(self.colors3d).reshape(-1, 3)
            self.edge_colors3d = np.array(self.edge_colors3d).reshape(-1, 3)



if __name__ == '__main__':
    print(version)






