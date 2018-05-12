# Part A
# File: parta.py
#
# TEAM ...

import sys
from watchurback import Board


def main(argv):
    # loads the board
    board = Board.from_file(open("sample_files/shrinkyay.in"))
    board.print_board()
    board.shrink()
    board.print_board()
    board.shrink()
    board.print_board()
    board.shrink()
    board.print_board()


if __name__ == "__main__":
    main(sys.argv[1:])
