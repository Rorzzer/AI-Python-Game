import itertools
import math
import typing

from spatial_utils import Coord, PAIRS, add_direction
from watchurback import Board, BLACK, EMPTY, Piece, get_enemy, CORNER


class MassacreBoard(Board):
    def __init__(self, board: Board):
        self._board = board._board
        self._size = board._size
        self._index_white = board._index_white
        self._index_black = board._index_black

    def is_elimable(self, coord: Coord):
        """ a coord is potentially eliminatable if it is surrounded (axially) by EMPTY, CORNER, or by enemy """
        enemy = get_enemy(self.get_piece(coord))
        return self.is_surrounded(coord, [EMPTY, enemy, CORNER])

    def get_elimable(self, player: Piece):
        return [coord for coord in self.index(player) if self.is_elimable(coord)]

    def get_moves_til_elim_spec(self, target: Coord, killer1: Coord, killer2: Coord):
        """ gets (num moves, route for killer 1, route for killer 2) to kill target """

        targetPiece = self.get_piece(target)
        player = get_enemy(targetPiece)

        # assumes params are sane e.g. target is BLACK and killers are both WHITE cops
        def combined_flight_plan(dir_pair):
            pos1 = add_direction(target, dir_pair[0])
            pos2 = add_direction(target, dir_pair[1])
            if not self.is_inside(pos1) or not self.is_inside(pos2):
                return math.inf, []

            pos1piece = self.get_piece(pos1)
            pos2piece = self.get_piece(pos2)
            if targetPiece in [pos1piece, pos2piece]:
                # this pair aint gonna work
                return math.inf, []

            # route and distance for each killer to get into position
            if pos1piece == CORNER:
                (d1, r1) = (0, [])
            else:
                (d1, r1) = self.get_min_dist(killer1, pos1, True)
            if pos2piece == CORNER:
                # R2D2 would have been nicer but distance first is easier to sort
                (d2, r2) = (0, [])
            else:
                (d2, r2) = self.get_min_dist(killer2, pos2, True)
            return d1 + d2, r1, r2

        return min([combined_flight_plan(dir_pair) for dir_pair in PAIRS])

    def get_moves_til_elim_all(self, target: Coord):
        """ gets (num moves, route, route) for any possible enemy """
        enemies = self.index(get_enemy(
            self.get_piece(target)))
        return min([self.get_moves_til_elim_spec(target, k1, k2)
                    for (k1, k2)
                    in itertools.permutations(enemies, 2)])

    def get_min_moves_til_elim(self, player: Piece):
        return min([self.get_moves_til_elim_all(target) for target in self.get_elimable(player)])

    def execute_min_moves_til_elim(self, player: Piece):
        (dist, moves1, moves2) = self.get_min_moves_til_elim(player)
        # moves the furthest one first
        # in calculating moves, we assumed that the destination could be of friendly units
        # so we need to make sure move[1] is EMPTY to be a valid move
        avail_moves = [move for move in [moves1, moves2] if len(move) > 1 and self.get_piece(move[1])==EMPTY]
        min_move = min(avail_moves, key=len)[:2]
        self.move(min_move[0], min_move[1])
        return min_move


def print_massacre_step(moves: typing.List[Coord]):
    print(moves[0], '->', moves[1])


def on_action(action: str, board: Board):
    m_board = MassacreBoard(board)
    m_board.print_board()
    while not m_board.is_win():
        moves = m_board.execute_min_moves_til_elim(BLACK)
        print_massacre_step(moves)
        m_board.print_board()
