import itertools
import typing

from spatial_utils import Coord, PAIRS, add_direction, Direction
from watchurback import Board, BLACK, EMPTY, Piece, get_enemy, CORNER


class MassacreBoard(Board):
    def __init__(self, board: Board):
        self._board = board._board
        self._size = board._size
        self._index_white = board._index_white
        self._index_black = board._index_black

    def get_potential_elims(self, coord: Coord):
        """ a coord is potentially eliminatable if it is surrounded (axially) by EMPTY, CORNER, or by enemy """
        enemy = get_enemy(self.get_piece(coord))

        def get_stats(dir: Direction):
            inner_coord = add_direction(coord, dir)
            if not self.is_inside(inner_coord):
                return False, False
            is_corner = self.check(coord, dir, [CORNER])
            is_valid = self.check(coord, dir, [enemy, EMPTY])
            return is_corner, is_valid, inner_coord

        hard_elim = []  # need 2 to eliminate (includes potentially PLAYER already there)
        easy_elim = []  # need 1 to eliminate
        for dir in PAIRS:
            first_dir_stats = get_stats(dir[0])
            second_dir_stats = get_stats(dir[1])
            if first_dir_stats[0] and second_dir_stats[1]:
                easy_elim += second_dir_stats[2:3]
            elif first_dir_stats[1] and second_dir_stats[0]:
                easy_elim += first_dir_stats[2:3]
            elif first_dir_stats[1] and second_dir_stats[1]:
                # permutation
                hard_elim += [(first_dir_stats[2], second_dir_stats[2]),
                              (second_dir_stats[2], first_dir_stats[2])]
        return hard_elim, easy_elim

    def get_hunting_ground(self, player: Piece):
        """ :returns a set of places enemy will have to be to kill player"""
        hards = []
        easies = []
        for coord in self.index(player):
            (hard, easy) = self.get_potential_elims(coord)
            hards += hard
            easies += easy
        return hards, easies

    def get_min_moves_til_elim(self, player: Piece):
        enemies = self.index(get_enemy(player))
        (hard, easy) = self.get_hunting_ground(player)

        # hard
        def hard_moves_stats(target, k1, k2):
            (d1, r1) = self.get_min_dist(k1, target[0], True)
            (d2, r2) = self.get_min_dist(k2, target[1], True)
            return d1 + d2, r1, r2

        hard_moves = [hard_moves_stats(target, k1, k2)
                      for target in hard
                      for (k1, k2) in itertools.combinations(enemies, 2)]

        # easy
        easy_moves = [self.get_min_dist(killer, target)
                      for target in easy
                      for killer in enemies]

        return min(hard_moves + easy_moves)

    def execute_min_moves_til_elim(self, player: Piece):
        min_move_sequences = self.get_min_moves_til_elim(player)
        # moves the furthest one first
        # in calculating moves, we assumed that the destination could be of friendly units
        # so we need to make sure move[1] is EMPTY to be a valid move
        avail_moves = [move for move in min_move_sequences[1:] if len(move) > 1 and self.get_piece(move[1]) == EMPTY]
        min_move = min(avail_moves, key=len)[:2]
        self.move(min_move[0], min_move[1])
        return min_move


def print_massacre_step(moves: typing.List[Coord]):
    print(moves[0], '->', moves[1])


def on_action(action: str, board: Board):
    m_board = MassacreBoard(board)
    # m_board.print_board()
    while not m_board.is_win():
        moves = m_board.execute_min_moves_til_elim(BLACK)
        print_massacre_step(moves)
        # m_board.print_board()
