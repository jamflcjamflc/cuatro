# -*- coding: utf8 -*-
# front_cover
# helper class for cuatro
# Alfredo Martin 2021

import pygame
import time
import os

version = 'front_cover.v.1.0.0'


class Cover:
    """the instance of this class renders the front cover before the game starts
    instance attributes:
    image: pygame image: image to be shown
    music: pygame sound: sound to be played
    width: int: width of the image
    height: int: height of the image"""

    def __init__(self, cover_image=None, cover_music=None, screen_shape=None):
        """cover_image: filename for an image file
        cover_music: filename for a music file
        screen_shape: tuple of two ints (shape of the screen)"""
        if cover_image is not None:
            image = pygame.image.load(cover_image)
            rect = image.get_rect()
            width = rect[2]
            height = rect[3]
            width_factor = 0.9 * screen_shape[0] / width
            height_factor = screen_shape[1] * 0.9 / height
            scale_factor = min(width_factor, height_factor)
            self.image = pygame.transform.smoothscale(image, (int(width * scale_factor), int(height * scale_factor)))
            rect = self.image.get_rect()
            self.width = rect[2]
            self.height = rect[3]
        else:
            self.image = None
            self.width = None
            self.height = None
        if cover_music is not None:
            self.music = pygame.mixer.Sound(cover_music)
            self.music.set_volume(0.3)
        else:
            self.music = None

    def run_cover(self, screen, joysticks, clock):
        if self.music is not None:
            self.music.play(loops=-1)
        keep_menu = True
        start_time = time.time()
        while keep_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_menu = False
                    pygame.quit()
                    quit()
            if len(joysticks) > 0:
                keep_menu = not any([item.get_button(1) for item in joysticks])
            else:
                if time.time() - start_time > 3:
                    keep_menu = False
            if len(joysticks) > 0:
                change_config = any([item.get_button(0) for item in joysticks])
                if change_config:
                    with open(os.path.join('resources', 'os_mask.ini'), 'r') as f:
                        lines = f.readlines()
                        line = lines[0].rstrip('\r\n')
                        if line.upper() == 'TRUE':
                            line = 'false\n'
                        else:
                            line = 'true\n'
                    with open(os.path.join('resources', 'os_mask.ini'), 'w') as f:
                        f.write(line)
                    print('os_mask.ini changed to ' + line)
                    keep_menu = False
                    pygame.quit()
                    quit()
            screen.fill((255, 255, 255))
            if self.image is not None:
                rect = screen.get_rect()
                screen.blit(self.image, ((rect[2] - self.width) // 2, (rect[3] - self.height) // 2))
            pygame.display.update()
            clock.tick(20)
        if self.music is not None:
            self.music.stop()
        time.sleep(1)
        return

if __name__ == '__main__':
    print(version)
