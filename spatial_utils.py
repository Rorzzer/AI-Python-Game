from collections import namedtuple
from enum import Enum

WHITE = 'white'
BLACK = 'black'
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
NONE = 'none'
NEXT_TO = 1
TWO_AWAY = 2
corner1 = (0, 0)
corner2 = (7, 0)
corner3 = (0, 7)
corner4 = (7, 7)

class Coord(namedtuple('Coord', ['x', 'y'])):
    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        # optimise???
        if other == 1:
            return self
        return Coord(self.x * other, self.y * other)

    def add_x(self, x: int):
        return self + Coord(x, 0)

    def add_y(self, y: int):
        return self + Coord(0, y)

    def is_adjacent(self, to):
        dx = abs(self.x - to.x)
        dy = abs(self.y - to.y)
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'


class Direction(Enum):
    UP = Coord(0, -1)
    DOWN = Coord(0, 1)
    LEFT = Coord(-1, 0)
    RIGHT = Coord(1, 0)


HORIZONTAL_PAIR = [Direction.LEFT, Direction.RIGHT]
VERTICAL_PAIR = [Direction.UP, Direction.DOWN]
PAIRS = [HORIZONTAL_PAIR, VERTICAL_PAIR]


def add_direction(coord: Coord, direction: Direction, how_much: int = 1):
    return coord + (direction.value * how_much)


def can_elim_count(board: Board, indexblack, xy: tuple):
    x = xy[0]
    y = xy[1]
    total = 0

    # import pdb;
    # pdb.set_trace()

    if check_left(NEXT_TO, BLACK, board, indexblack, x, y) and check_left(TWO_AWAY, WHITE, board, indexblack, x, y):
        indexblack.remove((x - 1, y))
        total += 1

    if check_right(NEXT_TO, BLACK, board, indexblack, x, y) and check_right(TWO_AWAY, WHITE, board, indexblack, x, y):
        indexblack.remove((x + 1, y))
        total += 1

    if check_up(NEXT_TO, BLACK, board, indexblack, x, y) and check_up(TWO_AWAY, WHITE, board, indexblack, x, y):
        indexblack.remove((x, y - 1))
        total += 1

    if check_down(NEXT_TO, BLACK, board, indexblack, x, y) and check_down(TWO_AWAY, WHITE, board, indexblack, x, y):
        indexblack.remove((x, y + 1))
        total += 1

    return total


def is_surrounded(board: Board, index, xy: tuple):
    # checks if a piece is surrounded after making the move
    x = xy[0]
    y = xy[1]

    return (((check_left(NEXT_TO, BLACK, board, index, x, y) and check_right(NEXT_TO, BLACK, board, index, x, y)) or
             (check_up(NEXT_TO, BLACK, board, index, x, y) and check_down(NEXT_TO, BLACK, board, index, x, y))) and
            can_elim_count(board, index, xy) < 3)


def next_to_count(colour, board: Board, indexblack, xy: tuple):
    # counts the number of neighbouring pieces of a certain colour
    x = xy[0]
    y = xy[1]
    total = 0

    if check_left(NEXT_TO, colour, board, indexblack, x, y):
        total += 1

    if check_right(NEXT_TO, colour, board, indexblack, x, y):
        total += 1

    if check_up(NEXT_TO, colour, board, indexblack, x, y):
        total += 1

    if check_down(NEXT_TO, colour, board, indexblack, x, y):
        total += 1

    if colour == WHITE:
        return total
    else:
        return total - can_elim_count(board, indexblack, xy)


def check_left(distance, colour, board: Board, indexblack, x, y):
    # returns true if piece to the left

    if colour == BLACK:
        for ii in indexblack:
            if ((x - distance), y) == (ii[0], ii[1]) or \
                    ((x - distance), y) == corner1 or \
                    ((x - distance), y) == corner3:
                return True
        return False
    elif colour == WHITE:
        for ii in board.index_white:
            if ((x - distance), y) == (ii[0], ii[1]) or \
                    ((x - distance), y) == corner1 or \
                    ((x - distance), y) == corner3:
                return True
        return False


def check_right(distance, colour, board: Board, indexblack, x, y):
    # returns true if piece to the right

    if colour == BLACK:
        for ii in indexblack:
            if ((x + distance), y) == (ii[0], ii[1]) or \
                    ((x + distance), y) == corner2 or \
                    ((x + distance), y) == corner4:
                return True
        return False
    elif colour == WHITE:
        for ii in board._index_white:
            if ((x + distance), y) == (ii[0], ii[1]) or \
                    ((x + distance), y) == corner2 or \
                    ((x + distance), y) == corner4:
                return True
        return False


def check_up(distance, colour, board: Board, indexblack, x, y):
    # returns true if piece above

    if colour == BLACK:
        for ii in indexblack:
            if (x, (y - distance)) == (ii[0], ii[1]) or \
                    (x, (y - distance)) == corner1 or \
                    (x, (y - distance)) == corner2:
                return True
        return False
    elif colour == WHITE:
        for ii in board.__index_white:
            if (x, (y - distance)) == (ii[0], ii[1]) or \
                    (x, (y - distance)) == corner1 or \
                    (x, (y - distance)) == corner2:
                return True
        return False


def check_down(distance, colour, board: Board, indexblack, x, y):
    # returns true if piece below

    if colour == BLACK:
        for ii in indexblack:
            if (x, (y + distance)) == (ii[0], ii[1]) or \
                    (x, (y + distance)) == corner3 or \
                    (x, (y + distance)) == corner4:
                return True
        return False

    elif colour == WHITE:
        for ii in board.__index_white:
            if (x, (y + distance)) == (ii[0], ii[1]) or \
                    (x, (y + distance)) == corner3 or \
                    (x, (y + distance)) == corner4:
                return True
        return False