# -*- coding: utf8 -*-
# engine
# helper class for cuatro
# Alfredo Martin 2021

import numpy as np
import random
import copy
import time

version = 'engine.v.1.0.0'

class State:
    """instance attributes:
    size: int:  size of one side of the board (defines a cube that holds the game)
    win: int: how many items in a row constitute a win of the game
    state: numpy array or shape (size, sizel size): 3D matrix containing 0 if position is empty,
           1 for player one items and 2 for player 2 items
    winner: int: winner of the game (0 until one player has won, then 1 or 2)
    winning_diag: list of 'win' tuples of three ints (coordinates of the positions that constitute the win of the game
    nex_turn: int (1 or 2) player that will play next
    previous_turn: int (1 or 2) player that has played last
    play: numpy array of shape (size, size) containint ints. It contains how many plays have been performed on each
            of the 2d coordinates in the board. It marks the next third coordinate for each 2d coordinate play
    pl1: numpy array of shape (size, size, size) containing 1 if the position is occupied by an item of player 1 and
            0 otherwise
    pl2: numpy array of shape (size, size, size) containing 1 if the position is occupied by an item of player 2 and
            0 otherwise
    empty: numpy array of shape (size, size, size) containing 1 if the position is empty and 0 otherwise
    last_play: tuple of two ints containing the last play performed
    last_3dplay: tuple of three ints containing the last 3dplay performed
    game_over: bool: True if all the positions of the 3d board are occupied or one of the players have won and False
            otherwise
    diags: dictionary of lists of lists of 'win' tuples containing 3 ints. The key of the dictionary is a tuple with
            3 ints (coordinates of a 3dpos). the values are lists of diags (a diag is a list containing 'win'
            coordinates, which are tuples of three ints). All diags in a list contain the coordinate of the key.
    history: list of dicts. Each dict contains the history of a turn. The dictionary fields are 'turn', 'play',
            'play3d', 'offensive_score', 'defensive_score' and 'offensive_diag'
    valid_pos: list of tuples with 2 ints: list of all valid plays at this time
    valid_3dpos: list of tuples with 3 ints: list of all valid 3dplays at this time
    """

    def __init__(self, size=5, win=4, next_turn=1):
        """this method initiallizes the instance
        size: int: size of the board"""
        random.seed(time.time())
        self.size = size
        self.win = win
        self.state = np.zeros((self.size, self.size, self.size)).astype('int8')
        self.winner = 0
        self.winning_diag = None
        self.next_turn = next_turn
        self.previous_turn = 3 - next_turn
        self.play = np.array([[0 for _ in range(self.size)] for _ in range(self.size)])
        self.pl1 = None
        self.pl2 = None
        self.get_pl()
        self.last_play = None  # last play done
        self.last_3dplay = None
        self.valid_pos = None
        self.valid_3dpos = None
        self.get_valid_pos()
        self.game_over = False  # whether game is over or not
        self.history = []
        # get the diagonals of size self.win that cross very cell in the 3d board
        self.diags = dict()
        diags = []
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    self.diags[(i, j, k)] = []
                    diags += self.get_diags(i, j, k)
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    for diag in diags:
                        if (i, j, k) in diag:
                            self.diags[(i, j, k)].append(diag)
        #for key in self.diags.keys():  # todo eliminate the reformatted version after changes
            #self.old_diags[key] = [[tuple(diag[i][j] for i in range(self.win)) for j in range(3)] for diag in self.diags[key]]

    def get_valid_pos(self):
        """updates the valid_pos and valid_3dpos instance attributes
        """
        self.valid_pos = []
        self.valid_3dpos = []
        for i in range(self.size):
            for j in range(self.size):
                if self.play[i][j] < self.size:
                    self.valid_pos.append((i, j))
                    self.valid_3dpos.append((i, j, self.play[i][j]))

    def get_diags(self, i, j, k):
        """creates all the diagonals of self.win me"""
        diags = []
        diags.append([(i + a, j, k) if i + a < self.size else None for a in range(self.win)])
        diags.append([(i, j + a, k) if j + a < self.size else None for a in range(self.win)])
        diags.append([(i, j, k + a) if k + a < self.size else None for a in range(self.win)])
        diags.append([(i + a, j + a, k) if i + a < self.size and j + a < self.size else None for a in range(self.win)])
        diags.append([(i + a, j - a, k) if i + a < self.size and j - a > -1 else None for a in range(self.win)])
        diags.append([(i + a, j, k + a) if i + a < self.size and k + a < self.size else None for a in range(self.win)])
        diags.append([(i + a, j, k - a) if i + a < self.size and k - a > -1 else None for a in range(self.win)])
        diags.append([(i, j + a, k + a) if j + a < self.size and k + a < self.size else None for a in range(self.win)])
        diags.append([(i, j + a, k - a) if j + a < self.size and k - a > -1 else None for a in range(self.win)])
        diags.append([(i + a, j + a, k + a) if i + a < self.size and j + a < self.size and k + a < self.size else None for a in range(self.win)])
        diags.append([(i - a, j + a, k + a) if i - a > -1 and j + a < self.size and k + a < self.size else None for a in range(self.win)])
        diags.append([(i + a, j - a, k + a) if i + a < self.size and j - a > -1 and k + a < self.size else None for a in range(self.win)])
        diags.append([(i - a, j - a, k + a) if i - a > -1 and j - a > -1 and k + a < self.size else None for a in range(self.win)])
        diags = [diag for diag in diags if None not in diag]
        return diags

    def get_score(self, pos3d):
        """computes the score of playing in position pos for both the next_turn (offensive score) and the
        previous_turn (defensive score) and returns scores, best diag etc (#todo complete this)
        pos3d: tuple of three ints: (coordinates of the play)
        returns: score: tuple of:
                        offensive_score: float
                        num_offensive_score: int
                        defensive_score: float
                        num_defensive_score: int
                        best_diag: list of tuples containing 3 ints"""
        own_score = []
        other_score = []
        best_diag = None
        for diag in self.diags[pos3d]:
            own_score.append(0.)
            other_score.append(0.)
            for item in diag:
                if item in self.valid_3dpos:  # the position of item is reachable and it is empty
                    own_score[-1] += 0.5
                    other_score[-1] += 0.5
                else:  # the position of item is not reachable but may or may not be empty
                    if self.next_turn == 1:
                        if self.pl1[item]:  # the position of item is occupied by the current turn
                            own_score[-1] += 1  # the position of item is occupied by the current turn
                            other_score[-1] -= self.win
                        elif self.pl2[item]:  # the position of item is occupied by the def
                            own_score[-1] -= self.win
                            other_score[-1] += 1
                        else:  # the position of item is not occupied (and it is not reachable either)
                            own_score[-1] += 0.1
                            other_score[-1] += 0.1
                    if self.next_turn == 2:
                        if self.pl2[item]:  # the position of item is occupied by the current turn
                            own_score[-1] += 1  # the position of item is occupied by the current turn
                            other_score[-1] -= self.win
                        elif self.pl1[item]:  # the position of item is occupied by the def
                            own_score[-1] -= self.win
                            other_score[-1] += 1
                        else:  # the position of item is not occupied (and it is not reachable either)
                            own_score[-1] += 0.1
                            other_score[-1] += 0.1
                if own_score[-1] == max(own_score):
                    best_diag = [pos for pos in diag]  # make a copy of diag just in case

        offensive_score = max(own_score)
        num_offensive_score = own_score.count(offensive_score)
        defensive_score = max(other_score)
        num_defensive_score = other_score.count(defensive_score)
        return offensive_score, num_offensive_score, defensive_score, num_defensive_score, best_diag

    def get_best_score_play(self):
        """gets the play for which the score is the best
        returns: chosen_play: tuple of:
                                play: tuple of two ints
                                play3d: tuple of three ints
                                score: float
                                diag: list of tuples of tree ints
        """
        # initiallization
        o_scores = []
        n_o_scores = []
        d_scores = []
        n_d_scores = []
        diags = []
        centroid = np.array([(self.size - 1) / 2. for _ in range(3)])
        # getting list of scores
        for play, play3d in zip(self.valid_pos, self.valid_3dpos):
            o_score, n_o_score, d_score, n_d_score, diag = self.get_score(play3d)
            o_scores.append(o_score)
            n_o_scores.append(n_o_score)
            d_scores.append(d_score)
            n_d_scores.append(n_d_score)
            diags.append([item for item in diag])
        # eliminate everything that does not have the max score
        max_score = max(max(o_scores), max(d_scores))
        o_indexes = [i for i in range(len(o_scores)) if o_scores[i] == max_score]
        d_indexes = [i for i in range(len(d_scores)) if d_scores[i] == max_score]
        o_scores = [o_scores[i] for i in o_indexes]
        n_o_scores = [n_o_scores[i] for i in o_indexes]
        diags = [diags[i] for i in o_indexes]
        o_plays = [self.valid_pos[i] for i in o_indexes]
        o_plays3d = [self.valid_3dpos[i] for i in o_indexes]
        d_scores = [d_scores[i] for i in d_indexes]
        n_d_scores = [n_d_scores[i] for i in d_indexes]
        d_plays = [self.valid_pos[i] for i in d_indexes]
        d_plays3d = [self.valid_3dpos[i] for i in d_indexes]
        # Select the play
        if max_score == self.win - 0.5 and len(o_scores) > 0:  # this play is winner
            return o_plays[0], o_plays3d[0], o_scores[0], diags[0]
        if max_score == self.win - 0.5 and len(d_scores) > 0:  # this avoids a winner play
            return d_plays[0], d_plays3d[0], d_scores[0], None
        if len(o_scores) == 1 and len(d_scores) == 0:  # will play the best offensive move
            return o_plays[0], o_plays3d[0], o_scores[0], diags[0]
        if len(o_scores) == 0 and len(d_scores) == 1:  # will play the best defensive move
            return d_plays[0], d_plays3d[0], d_scores[0], None
        if len(o_scores) > 1 and len(d_scores) == 0:  # will play an offensive move but there is more than one
            # first select based on the number of diags giving the score
            max_n = max(n_o_scores)
            o_indexes = [i for i in range(len(n_o_scores)) if n_o_scores[i] == max_n]
            o_scores = [o_scores[i] for i in o_indexes]
            n_o_scores = [n_o_scores[i] for i in o_indexes]
            diags = [diags[i] for i in o_indexes]
            o_plays = [o_plays[i] for i in o_indexes]
            o_plays3d = [o_plays3d[i] for i in o_indexes]
            if len(o_scores) == 1:  # this is the best
                return o_plays[0], o_plays3d[0], o_scores[0], diags[0]
            else:  # there is more than one option that tied, chose the one more centered
                dists = [((np.array(play3d) - centroid) ** 2).sum() for play3d in o_plays3d]
                mindist = min(dists)
                o_indexes = [i for i in range(len(dists)) if dists[i] == mindist]
                o_scores = [o_scores[i] for i in o_indexes]
                diags = [diags[i] for i in o_indexes]
                o_plays = [o_plays[i] for i in o_indexes]
                o_plays3d = [o_plays3d[i] for i in o_indexes]
                index = random.randrange(len(o_indexes))
                return o_plays[index], o_plays3d[index], o_scores[index], diags[index]
        if len(o_scores) == 0 and len(d_scores) > 1:  # we will play an defensive move but there is more than one
            # first select based on the number of diags giving the score
            max_n = max(n_d_scores)
            d_indexes = [i for i in range(len(n_d_scores)) if n_d_scores[i] == max_n]
            d_scores = [d_scores[i] for i in d_indexes]
            d_plays = [d_plays[i] for i in d_indexes]
            d_plays3d = [d_plays3d[i] for i in d_indexes]
            if len(d_scores) == 1:  # this is the best
                return d_plays[0], d_plays3d[0], d_scores[0], None
            else: # there is more than one option that tied, chose the one more centered
                dists = [((np.array(play3d) - centroid) ** 2).sum() for play3d in d_plays3d]
                mindist = min(dists)
                d_indexes = [i for i in range(len(dists)) if dists[i] == mindist]
                d_scores = [d_scores[i] for i in d_indexes]
                d_plays = [d_plays[i] for i in d_indexes]
                d_plays3d = [d_plays3d[i] for i in d_indexes]
                index = random.randrange(len(d_indexes))
                return d_plays[index], d_plays3d[index], d_scores[index], None
        if len(o_scores) > 0 and len(d_scores) > 0:  # there are offensive and defensive scores tied
            # remove all options that do not have the maximum number of diags giving that score
            max_n = max(max(n_o_scores), max(n_d_scores))
            o_indexes = [i for i in range(len(n_o_scores)) if n_o_scores[i] == max_n]
            d_indexes = [i for i in range(len(n_d_scores)) if n_d_scores[i] == max_n]
            o_scores = [o_scores[i] for i in o_indexes]
            n_o_scores = [n_o_scores[i] for i in o_indexes]
            diags = [diags[i] for i in o_indexes]
            o_plays = [o_plays[i] for i in o_indexes]
            o_plays3d = [o_plays3d[i] for i in o_indexes]
            d_scores = [d_scores[i] for i in d_indexes]
            n_d_scores = [n_d_scores[i] for i in d_indexes]
            d_plays = [d_plays[i] for i in d_indexes]
            d_plays3d = [d_plays3d[i] for i in d_indexes]
            if len(o_scores) > 0 and len(d_scores) == 0:  # will play an offensive move
                if len(o_scores) == 1:  # there is only one option
                    return o_plays[0], o_plays3d[0], o_scores[0], diags[0]
                else:  # there there is more than one option, chose based on centrality
                    dists = [((np.array(play3d) - centroid) ** 2).sum() for play3d in o_plays3d]
                    mindist = min(dists)
                    o_indexes = [i for i in range(len(dists)) if dists[i] == mindist]
                    o_scores = [o_scores[i] for i in o_indexes]
                    diags = [diags[i] for i in o_indexes]
                    o_plays = [o_plays[i] for i in o_indexes]
                    o_plays3d = [o_plays3d[i] for i in o_indexes]
                    index = random.randrange(len(o_indexes))
                    return o_plays[index], o_plays3d[index], o_scores[index], diags[index]
            if len(o_scores) == 0 and len(d_scores) > 0:  # will play a defensive move
                if len(d_scores) == 1:  # we chose this one
                    return d_plays[0], d_plays3d[0], d_scores[0], None  # diags[0] is useless
                else:  # there are ties, chose based on centrality
                    dists = [((np.array(play3d) - centroid) ** 2).sum() for play3d in d_plays3d]
                    mindist = min(dists)
                    d_indexes = [i for i in range(len(dists)) if dists[i] == mindist]
                    d_scores = [d_scores[i] for i in d_indexes]
                    d_plays = [d_plays[i] for i in d_indexes]
                    d_plays3d = [d_plays3d[i] for i in d_indexes]
                    index = random.randrange(len(d_indexes))
                    return d_plays[index], d_plays3d[index], d_scores[index], None  # diags[0] is useless
            if len(o_scores) > 0 and len(d_scores) > 0:  # there are ties, play the offensive move
                if len(o_scores) == 1:  # there is only one option
                    return o_plays[0], o_plays3d[0], o_scores[0], diags[0]
                else:  # there there is more than one option, chose based on centrality
                    dists = [((np.array(play3d) - centroid) ** 2).sum() for play3d in o_plays3d]
                    mindist = min(dists)
                    o_indexes = [i for i in range(len(dists)) if dists[i] == mindist]
                    o_scores = [o_scores[i] for i in o_indexes]
                    diags = [diags[i] for i in o_indexes]
                    o_plays = [o_plays[i] for i in o_indexes]
                    o_plays3d = [o_plays3d[i] for i in o_indexes]
                    index = random.randrange(len(o_indexes))
                    return o_plays[index], o_plays3d[index], o_scores[index], diags[index]
            else:
                raise(ValueError, 'this should not have happened')
        else:
            raise (ValueError, 'this should not have happened')

    def get_pl(self):
        """tis method gets the state for each player"""
        self.pl1 = self.state == 1
        self.pl2 = self.state == 2
        self.empty = self.state == 0
        self.game_over = self.empty.sum() == 0

    def clone(self):
        """clone the current instance except the children (to make it faster)"""
        newself = copy.deepcopy(self)
        newself.children = []
        return newself

    def run_play(self, play=None):
        """update a state with a play. If play is none it will find the best play.
        if it is a play it will update the state if the play is valid
        play: tuple of two ints or None
        returns: success: bool (whether the state was updated or not)"""
        if self.game_over:
            return False
        if play is None:
            play, play3d, score, diag = self.get_best_score_play()
        if self.play[play] >= self.size:  # the play is ilegal
            return False
        play3d = (play[0], play[1], self.play[play])  # 3d position played
        offensive_score, num_offensive_score, defensive_score, num_defensive_score, best_diag = self.get_score(play3d)
        self.last_play = play  # last play in this state
        self.last_3dplay = play3d
        self.play[play] += 1  # updates play
        self.state[play3d] = self.next_turn  # updates state
        if self.next_turn == 1:  # update the position of the player in this turn
            self.pl1[play3d] = 1
        else:
            self.pl2[play3d] = 1
        self.empty[play3d] = 0  # update the empty states
        self.next_turn, self.previous_turn = self.previous_turn, self.next_turn  # swaps turns
        self.get_valid_pos()  # updates valid_pos and valid_3dpos
        if offensive_score == self.win - 0.5:  # updates winner
            self.winner = self.previous_turn
            self.winning_diag = best_diag
        # self.get_winner()  #todo eliminate after testing
        self.game_over = self.empty.sum() == 0 or self.winner > 0  # updates game over
        self.history.append({'turn': self.previous_turn, 'play':self.last_play, 'play3d': self.last_3dplay,
                             'offensive_score': offensive_score, 'defensive_score': defensive_score,
                             'best_diag': best_diag})
        print(self.history[-1])
        return True


if __name__ == '__main__':
    print(version)











