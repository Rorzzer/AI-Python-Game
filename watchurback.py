import math
from typing import List, TextIO

from spatial_utils import Coord, Direction, add_direction, PAIRS

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
    _board: List[List[Piece]] = []
    _size: int = 0

    _index_white: List[Coord] = []
    _index_black: List[Coord] = []

    def index(self, player: Piece):
        if player == WHITE:
            return list(self._index_white)
        elif player == BLACK:
            return list(self._index_black)
        else:
            raise ValueError('Player is either WHITE(O) or BLACK(@). Received ' + player)

    @classmethod
    def new_empty(cls, size: int = 8):
        board = Board()
        board._size = size
        board._board = [[EMPTY for _ in range(size)] for _ in range(size)]
        board._board[0][0] = board._board[0][-1] = board._board[-1][0] = board._board[-1][-1] = CORNER
        return board

    @classmethod
    def from_file(cls, file: TextIO, size: int = None):
        first_line = file.readline().strip().split(' ')
        if size is None:
            size = len(first_line)
        board = Board.new_empty(size)
        board._set_row(0, first_line)
        for y in range(1, size):
            board._set_row(y, file.readline().strip().split(' '))
        return board

    def _set_row(self, y: int, line: List[Piece]):
        # if len(line) != self.size:
        # WARNING incorrect size!
        for x in range(self._size):
            self._set_cell(Coord(x, y), line[x])

    def _set_cell(self, coord: Coord, piece: Piece):
        cornerRange = [0, self._size - 1]
        if coord.x in cornerRange and coord.y in cornerRange:
            return
        # if piece not in [EMPTY, BLACK, WHITE]:
        # WARNING illegal piece
        self._board[coord.y][coord.x] = piece
        if piece == WHITE:
            self._index_white.append(coord)
        elif piece == BLACK:
            self._index_black.append(coord)
        elif piece == EMPTY:
            # suppress ValueError because remove is noisy when index doesnt exist
            from contextlib import suppress
            with suppress(ValueError):
                self._index_white.remove(coord)
            with suppress(ValueError):
                self._index_black.remove(coord)

    def is_cell_valid(self, coord: Coord):
        return self.is_inside(coord) and self.get_piece(coord) == EMPTY

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
        for row in self._board:
            print(' '.join(row))

    def get_min_dist(self, coord_from: Coord, coord_to: Coord, dest_empty: bool = False):
        """return a tuple (distance, route) of the shortest route from to to"""
        enemy = get_enemy(self.get_piece(coord_from))
        original_to_piece = self.get_piece(coord_to)
        if dest_empty:
            self._set_cell(coord_to, EMPTY)

        # adapted from http://eddmann.com/posts/using-iterative-deepening-depth-first-search-in-python/
        def dfs(inner_route: List[Coord], inner_depth: int):
            if inner_depth == 0:
                return
            if inner_route[-1] == coord_to:
                return inner_route
            valid_moves = self.get_valid_moves(inner_route[-1])
            # if suicidal, not a valid move UNLESS its the final destination
            if coord_to in valid_moves:
                return inner_route + [coord_to]
            # suicidal if surrounded by corner or enemy
            valid_moves = [move for move in valid_moves if not self.is_surrounded(move, [CORNER, enemy])]
            for move in valid_moves:
                if move not in inner_route:
                    next_route = dfs(inner_route + [move], inner_depth - 1)
                    if next_route:
                        return next_route
            # blank returns (as in above as well) means its a dead end of dfs
            return

        # it is possible that a route not exist so we limit to
        # 25 (just some arbitrary number)
        default = (math.inf, [])
        for depth in range(25):
            route = dfs([coord_from], depth)
            if route:
                default = (len(route) - 1, route)
                break
        if dest_empty:
            self._set_cell(coord_to, original_to_piece)
        return default

    def get_piece(self, coord: Coord):
        return self._board[coord.y][coord.x]

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

    def check(self, coord: Coord, direction: Direction, for_pieces: List[Piece]):
        """ :returns True if the piece to the $direction of $coord is a piece of type $for_piece """
        rel_coord = add_direction(coord, direction)
        if not self.is_inside(rel_coord):
            # default behaviour for check outside boundary should be False cuz nothingness is not the same as anything
            # not even EMPTY
            return False
        return self.get_piece(rel_coord) in for_pieces

    def can_elim(self, coord: Coord):
        player = self.get_piece(coord)
        if player not in [WHITE, BLACK]:
            # it breaks the law of physics to delete empty space without black holes
            return False
        return self.is_surrounded(coord, [get_enemy(player), CORNER])

    def is_surrounded(self, coord: Coord, by: List[Piece]):
        """ is coord surrounded by a type of piece """
        for dirs in PAIRS:
            if self.check(coord, dirs[0], by) and self.check(coord, dirs[1], by):
                return True
        return False

    def elim_all(self, player: Piece):
        for piece in self.index(player):
            if self.can_elim(piece):
                self._set_cell(piece, EMPTY)

    def is_inside(self, coord: Coord):
        return coord.x in range(self._size) and coord.y in range(self._size)

    def is_win(self, player: Piece = None):
        # u win if u have no enemy left
        if player is not None:
            if len(self.index(get_enemy(player))) == 0:
                return player
            else:
                return
        if self.is_win(WHITE):
            return WHITE
        else:
            return self.is_win(BLACK)
