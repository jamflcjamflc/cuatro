# -*- coding: utf8 -*-
# cuatro
# helper class for cuatro
# Alfredo Martin 2021

import pygame
import numpy as np
import os
import random

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (90, 30)  # positions the screen in a specific position of the monitor
from classes.screenpos import ScreenPos
from classes.board import Board
from classes.cursor import Cursor
from classes.engine import State
from classes.get2dcoords import Get2dcoords
from classes.game import Game
from classes.draw import Draw
from classes.front_cover import Cover
from classes.anouncement import Announcement
from classes.controller import Controller
import argparse
import time


def parse_args():
    parser = argparse.ArgumentParser(description="""argument parser""")
    parser.add_argument('--cover_image', type=str, default='cover.png')
    parser.add_argument('--logo_image', type=str, default='logo.png')
    parser.add_argument('--cover_music', type=str, default='main_music.wav')
    parser.add_argument('--game_music', type=str, default='main_music.wav')
    parser.add_argument('--play_sound', type=str, default='play.wav')
    parser.add_argument('--ilegal_sound', type=str, default='error.wav')
    parser.add_argument('--win_sound', type=str, default='win.wav')
    parser.add_argument('--background_color', type=tuple, default=(255, 255, 255))
    parser.add_argument('--board_colors', type=tuple, default=((20, 20, 20), (200, 200, 200)))
    parser.add_argument('--board_edge_colors', type=tuple, default=((0, 255, 0), (0, 255, 0)))
    parser.add_argument('--cursor_color_1', type=tuple, default=(255, 255, 255))
    parser.add_argument('--cursor_color_2', type=tuple, default=(255, 255, 255))
    parser.add_argument('--cursor_edge_color_1', type=tuple, default=(255, 0, 0))
    parser.add_argument('--cursor_edge_color_2', type=tuple, default=(0, 0, 255))
    parser.add_argument('--player_color_1', type=tuple, default=(255, 0, 0))
    parser.add_argument('--player_color_2', type=tuple, default=(0, 0, 255))
    parser.add_argument('--player_edge_color_1', type=tuple, default=(255, 255, 255))
    parser.add_argument('--player_edge_color_2', type=tuple, default=(255, 255, 255))
    parser.add_argument('--screen_width', type=int, default=None)
    parser.add_argument('--screen_height', type=int, default=None)
    parser.add_argument('--game_size', type=int, default=5)
    parser.add_argument('--game_win', type=int, default=4)
    parser.add_argument('--camera_pos', type=tuple, default=(600., 0., 0.))
    parser.add_argument('--camera_angle', type=tuple, default=(0., 0., 0.))
    parser.add_argument('--screen_pos', type=tuple, default=(0., 0., 600.))
    parser.add_argument('--light_pos', type=tuple, default=(500., 500., 0.))
    parser.add_argument('--horizon', type=float, default=0.3)
    parser.add_argument('--width_factor', type=float, default=0.35)
    parser.add_argument('--space_factor', type=float, default=0.7)
    parser.add_argument('--board_height', type=int, default=10)
    parser.add_argument('--offset', type=tuple, default=(0, 0, 2000))
    parser.add_argument('--max_shading', type=float, default=0.5)
    parser.add_argument('--max_alpha', type=float, default=3.2)
    parser.add_argument('--max_beta', type=float, default=1.6)
    parser.add_argument('--time_limit', type=float, default=1.0)
    parser.add_argument('--player1_name', type=str, default='red')
    parser.add_argument('--player2_name', type=str, default='blue')
    args = parser.parse_args()
    return args

def initiallize_game(n_joys):
    """initiallizes the game
    n_joys: number of game pads detected"""
    # initiallizing screen
    width = int(args.width_factor * args.screen_width / args.game_size)
    space = int(args.space_factor * args.screen_width / args.game_size)
    screen = pygame.display.set_mode((args.screen_width, args.screen_height))
    state = State(size=args.game_size, win=args.game_win, next_turn=random.randint(1, 2))
    screenpos = ScreenPos(c=args.camera_pos,
                          t=args.camera_angle,
                          e=args.screen_pos,
                          height=args.screen_height,
                          width=args.screen_width,
                          horizon=args.horizon)
    board = Board(state=state,
                  width=width,
                  space=space,
                  height=args.board_height,
                  colors=args.board_colors,
                  edge_colors=args.board_edge_colors)
    cursor = Cursor(state=state,
                    width=width,
                    space=space,
                    colors=(args.cursor_color_1, args.cursor_color_2),
                    edge_colors=(args.cursor_edge_color_1, args.cursor_edge_color_2))
    game = Game(state=state,
                width=width,
                space=space,
                colors=(args.player_color_1, args.player_color_2),
                edge_colors=(args.player_edge_color_1, args.player_edge_color_2))
    get2dcoords = Get2dcoords(light_pos=args.light_pos,
                              offset=args.offset,
                              screenpos=screenpos)
    drawer = Draw(max_shading=args.max_shading)
    cover = Cover(cover_image=os.path.join('.', 'images', args.cover_image),
                  cover_music=os.path.join('.', 'sounds', args.cover_music),
                  screen_shape=(args.screen_width, args.screen_height))
    controller = Controller(size=args.game_size,
                            num_joys=n_joys,
                            time_limit=args.time_limit,
                            max_alpha=args.max_alpha,
                            max_beta=args.max_beta)
    player = [args.player1_name, args.player2_name]
    announcements = []
    return screen, state, screenpos, board, cursor, game, get2dcoords, drawer, cover, \
           controller, player, announcements


if __name__ == '__main__':
    # Initiallization
    args = parse_args()
    pygame.display.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.joystick.init()
    x_res, y_res = pygame.display.Info().current_w, pygame.display.Info().current_h
    x_res = int(0.9 * x_res)
    y_res = int(0.9 * y_res)
    if args.screen_width is None:
        args.screen_width = x_res
    if args.screen_height is None:
        args.screen_height = y_res
    clock = pygame.time.Clock()
    logo = pygame.image.load(os.path.join('.', 'images', args.logo_image))
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()
    # music and sounds
    print os.path.abspath(os.path.join('.', 'sounds', args.game_music))
    music = pygame.mixer.Sound(os.path.join('.', 'sounds', args.game_music))
    music.set_volume(0.3)
    play_sound = pygame.mixer.Sound(os.path.join('.', 'sounds', args.play_sound))
    play_sound.set_volume(0.1)
    ilegal_sound = pygame.mixer.Sound(os.path.join('.', 'sounds', args.ilegal_sound))
    ilegal_sound.set_volume(0.1)
    # initiallize game
    screen, state, screenpos, board, cursor, game, get2dcoords, drawer, cover, \
    controller, player, announcements = initiallize_game(len(joysticks))
    logo_rect = logo.get_rect()
    screen_rect = screen.get_rect()
    logo_pos = ((screen_rect[2] / 2) - (logo_rect[2] / 2), screen_rect[3] * args.horizon * 1.2)
    # cover
    cover.run_cover(screen, joysticks, clock)
    music.play(loops=-1)

    game_exit = False
    while not game_exit:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                game_exit = True
        clock.tick(20)
        screen.fill(args.background_color)
        screen.blit(logo, logo_pos)
        if len(joysticks) > 0 and (len(joysticks) == state.next_turn or state.game_over):  # the play is going to be made by a human
            # next we get actions (moving the game or playing) from the joystick
            if state.game_over and len(joysticks) == 1:  # figures out which joy to read based on state status
                joy_number = 0
            else:
                joy_number = state.next_turn - 1
            controller.get_status(joysticks[joy_number])
            cursor.pos = controller.cursor_pos
            if controller.action == 'exit_game':
                game_exit = True
            if controller.action == 'reset_game':
                if state.winner > 0:  # if previously there was a winner the music had stopped
                    music.play(loops=-1)
                screen, state, screenpos, board, cursor, game, get2dcoords, drawer, cover, \
                controller, player, announcements = initiallize_game(len(joysticks))
                cursor.pos = controller.cursor_pos
            if controller.action == 'play':
                if state.run_play(play=controller.cursor_pos):
                    controller.cursor_pos = cursor.pos = (0, 0)
                    if not state.game_over:
                        play_sound.play()
                else:
                    if not state.game_over:
                        ilegal_sound.play()
                # time.sleep(1)
        else:  # the play is being made by the engine state
            if not state.winner > 0 and not state.game_over:
                time.sleep(1)
                # state.run_play(play=state.get_best_score_play())  # todo remove after testing
                state.run_play()
                cursor.pos = controller.cursor_pos = (0, 0)
                play_sound.play()
        board.get_polygons3d(controller.a)
        cursor.get_polygons3d(state)
        game.get_polygons3d(state)

        if len(game.polygons3d) > 0 and state.winner == 0 and len(joysticks) > 0:  # showing everything
            polygons3d = np.concatenate([board.polygons3d, game.polygons3d, cursor.polygons3d], axis=0)
            colors = np.concatenate([board.colors3d, game.colors3d, cursor.colors3d], axis=0)
            edge_colors = np.concatenate([board.edge_colors3d, game.edge_colors3d, cursor.edge_colors3d], axis=0)
        elif state.winner > 0 or len(joysticks) == 0:  # not showing the cursor
            polygons3d = np.concatenate([board.polygons3d, game.polygons3d], axis=0)
            colors = np.concatenate([board.colors3d, game.colors3d], axis=0)
            edge_colors = np.concatenate([board.edge_colors3d, game.edge_colors3d], axis=0)
        else:  # game has not started so not showing the state of game
            polygons3d = np.concatenate([board.polygons3d, cursor.polygons3d], axis=0)
            colors = np.concatenate([board.colors3d, cursor.colors3d], axis=0)
            edge_colors = np.concatenate([board.edge_colors3d, cursor.edge_colors3d], axis=0)
        coords, colors, edge_colors, shading = get2dcoords.get_polygons2d(polygons3d=polygons3d,
                                                                          colors=colors,
                                                                          edge_colors=edge_colors,
                                                                          angles=(controller.a,
                                                                                  controller.b,
                                                                                  controller.g))
        if state.winner > 0:
            announcements.append(Announcement('The winner is ' + player[state.previous_turn - 1],
                                              time=200, color=(0, 0, 0)))
            music.stop()
        for announcement in announcements:
            announcement.update(screen)
        screen = drawer.draw(screen, coords, colors, edge_colors, shading)
        pygame.display.update()
        announcements = [announcement for announcement in announcements if announcement.active]
    pygame.quit()
    quit()
