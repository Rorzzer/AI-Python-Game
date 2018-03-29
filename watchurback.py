import math
from typing import List, TextIO

from spatial_utils import Coord, Direction, add_direction

CORNER = 'X'
WHITE = 'O'
BLACK = '@'
EMPTY = '-'

Piece = str


def get_enemy(player: Piece):
    if player == WHITE:
        return BLACK
    elif player == BLACK:
        return WHITE
    else:
        return player


class Board:
    __board: List[List[Piece]] = []
    __size: int = 0

    __index_white: List[Coord] = []
    __index_black: List[Coord] = []

    def index(self, player: Piece):
        if player == WHITE:
            return list(self.__index_white)
        elif player == BLACK:
            return list(self.__index_black)
        else:
            raise ValueError('Player is either WHITE(O) or BLACK(@). Received ' + player)

    def __init__(self, size: int = 8):
        self.__size = size
        self.__board = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.__board[0][0] = self.__board[0][-1] = self.__board[-1][0] = self.__board[-1][-1] = CORNER

    def _set_row(self, y: int, line: List[Piece]):
        # if len(line) != self.size:
        # WARNING incorrect size!
        for x in range(self.__size):
            self._set_cell((x, y), line[x])

    def _set_cell(self, coord: Coord, piece: Piece):
        (x, y) = coord
        if (x == 0 or x == self.__size - 1) and (y == 0 or y == self.__size - 1):
            return
        # if piece not in [EMPTY, BLACK, WHITE]:
        # WARNING illegal piece
        self.__board[y][x] = piece
        if piece == WHITE:
            self.__index_white.append((x, y))
        elif piece == BLACK:
            self.__index_black.append((x, y))
        elif piece == EMPTY:
            # suppress ValueError because remove is noisy when index doesnt exist
            from contextlib import suppress
            with suppress(ValueError):
                self.__index_white.remove(coord)
            with suppress(ValueError):
                self.__index_black.remove(coord)

    def is_cell_valid(self, coord: Coord):
        (x, y) = coord
        # here (x,y) may be dum values
        if x not in range(self.__size) or y not in range(self.__size):
            return False
        return self.__board[y][x] == EMPTY

    def get_valid_moves(self, coord: Coord):
        valid = []
        # try walk, else then try jump
        for direction in Direction:
            # try walk
            rel_coord = add_direction(coord, direction)
            if self.is_cell_valid(rel_coord):
                valid.append(rel_coord)
            else:
                # then try jump
                rel_coord = add_direction(coord, direction, 2)
                if self.is_cell_valid(rel_coord):
                    valid.append(rel_coord)
        return valid

    def print_board(self):
        for row in self.__board:
            print(' '.join(row))

    def get_min_dist(self, coord_from: Coord, coord_to: Coord):
        """return a tuple (route, distance) of the shortest route from to to"""

        # adapted from http://eddmann.com/posts/using-iterative-deepening-depth-first-search-in-python/
        def dfs(inner_route: List[Coord], inner_depth: int):
            if inner_depth == 0:
                return
            if inner_route[-1] == coord_to:
                return inner_route
            for move in self.get_valid_moves(inner_route[-1]):
                if move not in inner_route:
                    next_route = dfs(inner_route + [move], inner_depth - 1)
                    if next_route:
                        return next_route

        # it is possible that a route not exist so we limit to
        # 25 (just some arbitrary number)
        for depth in range(25):
            route = dfs([coord_from], depth)
            if route:
                return route, len(route) - 1
        return [], math.inf

    def get_piece(self, coord: Coord):
        (x, y) = coord
        return self.__board[y][x]

    def move(self, coord_from: Coord, coord_to: Coord, require_player: Piece = None, perform_elim: bool = True):
        """move piece and validate move"""
        # TODO still missing validation for walk/jump size
        player = self.get_piece(coord_from)
        if not player:
            # we cannot move nothing!
            return False
        if require_player and player is not require_player:
            return False
        if not self.is_cell_valid(coord_to):
            return False
        # preliminary tests passed, now move
        # set_cell deals with indexing so no worries here
        self._set_cell(coord_from, EMPTY)
        self._set_cell(coord_to, player)
        # eliminate the enemy's pieces first, then player's
        if perform_elim:
            self.elim_all(get_enemy(player))
            self.elim_all(player)

    def check(self, coord: Coord, direction: Direction, for_piece: Piece):
        """ :returns True if the piece to the $direction of $coord is a piece of type $for_piece """
        return self.get_piece(add_direction(coord, direction)) == for_piece

    def can_elim(self, coord: Coord):
        player = self.get_piece(coord)
        if player not in [WHITE, BLACK]:
            # it breaks the law of physics to delete empty space without black holes
            return False
        return self.is_surrounded(coord, get_enemy(player))

    def is_surrounded(self, coord: Coord, by: Piece):
        """ is coord surrounded by a type of piece """
        for dirs in [(Direction.UP, Direction.DOWN), (Direction.LEFT, Direction.RIGHT)]:
            if self.check(coord, dirs[0], by) and self.check(coord, dirs[1], by):
                return True
        return False

    def elim_all(self, player: Piece):
        for piece in self.index(player):
            if self.can_elim(piece):
                self._set_cell(piece, EMPTY)


def get_board_from_file(file: TextIO, size: int = None):
    first_line = file.readline().strip().split(' ')
    if size is None:
        size = len(first_line)
    board = Board(size)
    board._set_row(0, first_line)
    for y in range(1, size):
        board._set_row(y, file.readline().strip().split(' '))
    return board
