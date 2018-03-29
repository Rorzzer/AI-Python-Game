# Part A
# File: parta.py
#
# TEAM ...

import sys
from watchurback import Board
import a_massacre
import a_moves


def main(argv):
    # for testing purposes, input can be piped or in file in argv
    input_file = sys.stdin
    if len(argv) > 0:
        input_file = open(argv[0])

    # loads the board
    board = Board.from_file(input_file)
    # board.print_board()

    action = input_file.readline().strip().upper()
    actions = {
        'MOVES': a_moves.on_action,
        'MASSACRE': a_massacre.on_action
    }
    func = actions.get(action, default_action)
    func(action, board)


def default_action(action: str, board: Board):
    print('Unknown action command ' + action)
    print('Just have a look at the board:')
    board.print_board()


if __name__ == "__main__":
    main(sys.argv[1:])
