# -*- coding: utf8 -*-
# cuatro
# helper class for cuatro
# Alfredo Martin 2021

import pygame

version = 'announcement.v.1.0.0'


class Announcement:
    """ the instance of this class shows an announcement for a specific amount of time
    instance attrbutes:
    t: int: how many iterations the text will be dysplayed
    color: color of the text
    text: pygame surface showing the text
    text_rect: pygame rect form the text
    active: bool: triggers instance destruction
    """

    def __init__(self, text, time, color):
        """text: str: text to be displayed
        time: int: how many iterations the text will be displayed
        color: tuple or three ints: color of the text
        pos: position to dysplay the text"""
        self.t = 0
        self.color = color
        self.time = time
        self.active = True
        style = pygame.font.SysFont('comicsans', 70)
        self.text = style.render(text, False, self.color)
        self.text_rect = self.text.get_rect()

    def update(self, screen):
        self.t += 1
        self.active = self.t <= self.time
        screen_rect = screen.get_rect()
        pos = ((screen_rect[2] / 2) - (self.text_rect[2] / 2), 0)
        screen.blit(self.text, pos)
        return None


if __name__ == '__main__':
    print(version)
