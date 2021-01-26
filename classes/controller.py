# -*- coding: utf8 -*-
# controller
# helper class for cuatro
# Alfredo Martin 2021

import time
import numpy as np

version = 'controller.v.1.0.0'


class Controller:
    """controls the actions through the game pads
    instance attributes:
    size: int: size of the game
    num_joys: int: number of game pads plugged
    cursor_pos: tuple of two ints: current position of the cursor
    a: float: board rotation angle about the x axis
    b: float: board rotation angle about the y axis
    g: float: board rotation angle about the z axis
    max_alpha: float: maximum value for a (not used in this implementation)
    max_beta: float: maximum value for b
    cursor_shift: tuple of two ints: shift of the cursor commanded by the game pad
    old_cursor_shift: tuple of two ints: shift of the cursor commanded by the game pad
    buttons: tuple of four bool: last state of the buttons
    old_buttons: tuple of four bool: previous state of the buttons
    action: str: indication of action
    time_limit: time limit to hold a button pressed to activate the action when the button is programmed so

    """

    def __init__(self, size=5, num_joys=2, time_limit=1., max_alpha=3.14, max_beta=3.14):
        """initializes the controller class
        size: int: size of the board
        num_joys: int: number of game pads
        time_limit: float: time in seconds that an exit or reset button has to be pressed to be activated"""
        self.size = size
        self.num_joys = num_joys
        self.active_joy = 0
        self.cursor_pos = (0, 0)
        self.a = 0.
        self.b = 0.
        self.g = 0.
        self.max_alpha = max_alpha
        self.max_beta = max_beta
        self.cursor_shift = (0, 0)
        self.old_cursor_shift = (0, 0)
        self.buttons = (False, False, False, False)
        self.old_buttons = (False, False, False, False)
        self.action = 'no_action'
        self.reset_time = None
        self.time_limit = time_limit

    def get_action(self, joy):
        self.buttons = (joy.get_button(0), joy.get_button(1), joy.get_button(2), joy.get_button(3))
        if self.buttons != (False, False, False, False) and self.old_buttons != self.buttons:
            if self.buttons[1]:
                self.action = 'play'
            elif self.buttons[2]:
                self.action = 'reset_board'
                self.a = 0.
                self.b = 0.
        elif self.buttons != (False, False, False, False):
            if self.buttons[0]:  # button has to be pressed for more than one cycle
                if self.reset_time is None:
                    self.reset_time = time.time()
                else:
                    if time.time() > self.reset_time + self.time_limit:
                        self.action = 'exit_game'
                        self.reset_time = None
            elif self.buttons[3]:
                if self.reset_time is None:
                    self.reset_time = time.time()
                else:
                    if time.time() > self.reset_time + self.time_limit:
                        self.action = 'reset_game'
                        self.reset_time = None
        else:
            self.action = 'no_action'
            self.reset_time = None
        self.old_buttons = self.buttons

    def get_cursor_pos(self, joy):
        self.cursor_shift = joy.get_hat(0)
        if self.cursor_shift != self.old_cursor_shift and self.cursor_shift != (0, 0):  # the new position of the cursor
            if -np.pi / 4 <= self.a < np.pi / 4:  # front view
                self.cursor_pos = (max(0, min(self.cursor_pos[0] + self.cursor_shift[0], self.size - 1)),
                                   max(0, min(self.cursor_pos[1] - self.cursor_shift[1], self.size - 1)))
            elif -3 * np.pi / 4 <= self.a < -np.pi / 4:  # left view
                self.cursor_pos = (max(0, min(self.cursor_pos[0] + self.cursor_shift[1], self.size - 1)),
                                   max(0, min(self.cursor_pos[1] + self.cursor_shift[0], self.size - 1)))
            elif np.pi / 4 <= self.a < 3 * np.pi / 4:
                self.cursor_pos = (max(0, min(self.cursor_pos[0] - self.cursor_shift[1], self.size - 1)),
                                   max(0, min(self.cursor_pos[1] - self.cursor_shift[0], self.size - 1)))
            elif -3 * np.pi / 4 > self.a or self.a >= 3 * np.pi / 4:  # back view
                self.cursor_pos = (max(0, min(self.cursor_pos[0] - self.cursor_shift[0], self.size - 1)),
                                   max(0, min(self.cursor_pos[1] + self.cursor_shift[1], self.size - 1)))
        self.old_cursor_shift = self.cursor_shift

    def get_angles(self, joy):
        angle_a = joy.get_axis(4)
        angle_b = joy.get_axis(3)
        if angle_a > 0.5:
            self.a = max(-self.max_alpha, self.a - 0.05)
        elif angle_a < -0.5:
            self.a = min(self.max_alpha, self.a + 0.05)
        if angle_b > 0.5:
            self.b = max(-self.max_beta / 2, self.b - 0.05)
        elif angle_b < -0.5:
            self.b = min(0, self.b + 0.05)

    def get_status(self, joy):
        """updates all the actions from the given joystick
        joy: instance of pygame.joystick.Joystick class"""
        self.get_angles(joy)
        self.get_cursor_pos(joy)
        self.get_action(joy)


if __name__ == '__main__':
    print(version)
