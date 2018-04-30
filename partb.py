# Part B
# File: partb.py
#
# TEAM The Dream Team

import sys

import watchurback
from watchurback import Board

WHITE = 'O'
BLACK = '@'


class Player:

    def __init__(self, colour):
        self.board = Board.new_empty()


        # input_file = open("/sample_files/massacre-sample-6.in")

        # loads the board
        # board = Board.from_file(input_file)
        # self.board = Board.from_file(input_file)

        # if colour == WHITE:
        #     self.colour = WHITE
        # elif colour == BLACK:
        #     self.colour = BLACK

    def action(self, Turns):

        # To place piece on board return a tuple (x, y)
        # To move a piece return nested tuple ((a, b), (c, d))
        # to forfeit turn return 'None'

        # nonlocal turns
        turns = Turns

        if turns < 24:
            # move = tuple(map(int, input("move:").split(',')))
            # return move
        else:
            return watchurback.MiniMax(self, 10)

    def update(self, action):

        # if action.turns < 24:
        #     return
        # else:
        #     self.board.move(action)
        # called by referee to update board and opponents move
        return
