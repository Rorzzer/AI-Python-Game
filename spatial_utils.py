from collections import namedtuple
from enum import Enum


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
        dx = abs(self.x-to.x)
        dy=abs(self.y-to.y)
        return (dx==1 and dy==0) or (dx==0 and dy==1)



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
