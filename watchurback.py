import math
import typing

CORNER = 'X'
WHITE = 'O'
BLACK = '@'
EMPTY = '-'

Coord = typing.Tuple[int, int]


# coord helpers
def dx(coord: Coord, dx: int):
    (x, y) = coord
    return (x + dx, y)


def dy(coord: Coord, dy: int):
    (x, y) = coord
    return (x, y + dy)


def north(coord: Coord, d: int = 1):
    return dy(coord, -d)


def south(coord: Coord, d: int = 1):
    return dy(coord, d)


def west(coord: Coord, d: int = 1):
    return dx(coord, -d)


def east(coord: Coord, d: int = 1):
    return dx(coord, d)


class BlankBoard:
    board = []
    size = 0

    index_white = []
    index_black = []

    def __init__(self, size: int = 8):
        self.size = size
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.board[0][0] = self.board[0][-1] = self.board[-1][0] = self.board[-1][-1] = CORNER

    def set_row(self, y: int, line: typing.List[str]):
        # if len(line) != self.size:
        # WARNING incorrect size!
        for x in range(self.size):
            self.set_cell((x, y), line[x])

    def set_cell(self, coord: Coord, piece: str):
        (x, y) = coord
        if (x == 0 or x == self.size - 1) and (y == 0 or y == self.size - 1):
            return
        # if piece not in [EMPTY, BLACK, WHITE]:
        # WARNING illegal piece
        self.board[y][x] = piece
        if piece == WHITE:
            self.index_white.append((x, y))
        elif piece == BLACK:
            self.index_black.append((x, y))
        elif piece == EMPTY:
            # suppress ValueError because remove is noisy when index doesnt exist
            from contextlib import suppress
            with suppress(ValueError):
                self.index_white.remove(coord)
            with suppress(ValueError):
                self.index_black.remove(coord)

    def is_cell_valid(self, coord: Coord):
        (x, y) = coord
        # here (x,y) may be dum values
        if x not in range(self.size) or y not in range(self.size):
            return False
        return self.board[y][x] == EMPTY

    def get_valid_moves(self, coord: Coord):
        valid = []
        # try walk, else then try jump
        for rel_func in [north, east, south, west]:
            # try walk
            rel_coord = rel_func(coord)
            if self.is_cell_valid(rel_coord):
                valid.append(rel_coord)
            else:
                # then try jump
                rel_coord = rel_func(coord, 2)
                if self.is_cell_valid(rel_coord):
                    valid.append(rel_coord)
        return valid

    def print_board(self):
        for row in self.board:
            print(' '.join(row))

    def get_min_dist(self, coord_from: Coord, coord_to: Coord):
        """return a tuple (route, distance) of the shortest route from to to"""

        # apapted from http://eddmann.com/posts/using-iterative-deepening-depth-first-search-in-python/
        def dfs(route, depth):
            if depth == 0:
                return
            if route[-1] == coord_to:
                return route
            for move in self.get_valid_moves(route[-1]):
                if move not in route:
                    next_route = dfs(route + [move], depth - 1)
                    if next_route:
                        return next_route

        # it is possible that a route not exist so we limit to
        # 25 (just some arbitrary number)
        for depth in range(25):
            route = dfs([coord_from], depth)
            if route:
                return (route, len(route) - 1)
        return ([], math.inf)

    def get_piece(self, coord: Coord):
        (x, y) = coord
        return self.board[y][x]

    def move(self, coord_from: Coord, coord_to: Coord, require_player: str = None):
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
        self.set_cell(coord_from, EMPTY)
        self.set_cell(coord_to, player)


def get_board_from_file(file: typing.TextIO, size: int = None):
    firstline = file.readline().strip().split(' ')
    if size is None:
        size = len(firstline)
    board = BlankBoard(size)
    board.set_row(0, firstline)
    for y in range(1, size):
        board.set_row(y, file.readline().strip().split(' '))
    return board
