from collections import namedtuple


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


UP = Coord(0, -1)
DOWN = Coord(0, 1)
LEFT = Coord(-1, 0)
RIGHT = Coord(1, 0)

ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

HORIZONTAL_PAIR = [LEFT, RIGHT]
VERTICAL_PAIR = [UP, DOWN]
PAIRS = [HORIZONTAL_PAIR, VERTICAL_PAIR]


def add_direction(coord: Coord, direction: Coord, how_much: int = 1):
    # extremely slow (from profiling)
    # return coord + (direction.value * how_much)
    x, y = coord
    dx, dy = direction
    return Coord(x + dx * how_much, y + dy * how_much)
