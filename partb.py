# Part B
# File: partb.py
#
# TEAM The Dream Team

import sys

import a_massacre
import a_moves
from watchurback import Board

WHITE = 'white'
BLACK = 'black'


class Player:

    def __init__(self, colour):
        if colour == WHITE:
            self.colour = WHITE
        elif colour == BLACK:
            self.colour = BLACK
        else:


    def action(self, turns):
        # To place piece on board return a tuple (x, y)

        # To move a piece return nested tuple ((a, b), (c, d))

        # to forfeit turn return 'None'


    def update(self, action):
        # called by referee to update board and opponents move
