import typing
from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


Coord = typing.Tuple[int, int]


def add(u: Coord, v: Coord):
    (ux, uy) = u
    (vx, vy) = v
    return ux + vx, uy + vy


def scale(u: Coord, factor: int):
    # optimise???
    if factor == 1:
        return u
    (x, y) = u
    return x * factor, y * factor


# coord helpers
def add_x(coord: Coord, x: int):
    return add(coord, (x, 0))


def add_y(coord: Coord, y: int):
    return add(coord, (0, y))


def add_direction(u: Coord, direction: Direction, how_much: int = 1):
    return add(u, scale(direction.value, how_much))
