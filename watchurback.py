import copy
import math
from random import shuffle
from typing import List, TextIO

from spatial_utils import Coord, Direction, add_direction, PAIRS

CORNER = 'X'
WHITE = 'O'
BLACK = '@'
EMPTY = '-'

Piece = str


def get_enemy(colour):
    if colour == WHITE:
        return BLACK
    elif colour == BLACK:
        return WHITE
    else:
        return colour


class Board:

    def __init__(self):
        self._board: List[List[Piece]] = []
        self._size: int = 0
        self._start: int = 0
        self._phase: int = 1
        self._p1_w_count: int = 0
        self._p1_b_count: int = 0
        self._turn: int = 0
        self._p2_turn: int = 0

        self._index_white: List[Coord] = []
        self._index_black: List[Coord] = []

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
        board._set_corners()
        return board

    def _set_corners(self):
        s = self._start
        e = self._size - s - 1
        for y, x in [(s, s), (s, e), (e, s), (e, e)]:
            self._board[y][x] = CORNER

    def shrink(self):
        s = self._start
        e = self._size - s - 1
        elim_list = [Coord(s + 1, s + 1), Coord(s + 1, e - 1), Coord(e - 1, s + 1), Coord(e - 1, e - 1)]
        for x in range(s, e + 1):
            elim_list += [Coord(s, x), Coord(e, x), Coord(x, s), Coord(x, e)]
        for coord in elim_list:
            piece = self.get_piece(coord)
            if piece == BLACK:
                self._index_black.remove(coord)
            elif piece == WHITE:
                self._index_white.remove(coord)
            self._board[coord.y][coord.x] = EMPTY
        self._start += 1
        self._set_corners()
        s += 1
        e -= 1
        # New corner squares eliminate nearby pieces
        # in order starting with the top-left new corner square and proceeding counter-clockwise
        # around the board.
        elim_list = [Coord(s + 1, s), Coord(s, s + 1), Coord(s, e - 1), Coord(s, e), Coord(e - 1, e), Coord(e, e - 1),
                     Coord(e, s + 1), Coord(e - 1, s)]
        for coord in elim_list:
            if self.can_elim(coord):
                self._set_cell(coord, EMPTY)

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
        cornerRange = [self._start, self._size - self._start - 1]
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

    def evaluate_detail(self, player: Piece):
        # this is very arbitrary
        enemy = get_enemy(player)
        return self.get_pieces_surrounded(enemy) - 0.3 * self.get_pieces_surrounded(player) \
               + 3 * self.get_pieces_count(player) - self.get_pieces_count(enemy) \
               + 0.1 * self.get_pieces_adj(player, False) \
               + 2 * self.middle_block_strategy(player, enemy)

    def middle_block_strategy(self, player: Piece, enemy: Piece):
        p_count = 0
        for x in [3, 4]:
            for y in [3, 4]:
                piece = self.get_piece(Coord(x, y))
                if piece == player:
                    p_count += 1
                elif piece == EMPTY:
                    pass
                elif piece == enemy:
                    p_count -= 1
                else:
                    return 0
        return p_count

    def get_pieces_count(self, player: Piece):
        return len(self.index(player))

    def get_pieces_surrounded(self, player: Piece):
        return len([piece for piece in self.index(player) if self.can_elim(piece)])

    def get_pieces_adj(self, player: Piece, incl_corner: bool = True):
        count_adj: int = 0
        enemy = get_enemy(player)
        adj_list = [enemy, CORNER] if incl_corner else [enemy]
        for piece in self.index(player):
            for dir in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                if self.check(piece, dir, adj_list):
                    count_adj += 1
        return count_adj

    def branch(self):
        return copy.deepcopy(self)

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

    def get_valid_moves_b(self, player: Piece):
        if self._phase == 1:
            # placing phase
            y_offset = 0 if player is WHITE else 2
            starting_zone = [Coord(x, y) for x in range(0, 8) for y in range(y_offset, y_offset + 6)]
            corners = [Coord(x, y) for x in [0, 7] for y in [0, 7]]
            invalid = corners + self._index_white + self._index_black
            starting_zone = [coord for coord in starting_zone if coord not in invalid]
            shuffle(starting_zone)
            return starting_zone  # + [None]
        elif self._phase == 2:
            # moving phase
            moves = []  # [None]
            for start in self.index(player):
                for end in self.get_valid_moves(start):
                    moves += [(start, end)]
            # shuffle(moves)
            return moves

    def print_board(self):
        s = self._start
        e = self._size - s
        for row in self._board[s:e]:
            print(' '.join(row[s:e]))

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

    def move_a(self, coord_from: Coord, coord_to: Coord, require_player: Piece = None, perform_elim: bool = True):
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

    def move(self, move, player: Piece, lawful: bool = True):
        self._turn += 1
        if self._phase == 2:
            self._p2_turn += 1
        if isinstance(move, tuple):
            c_from, c_to = move
            if isinstance(c_from, tuple):
                # this is a walk/jump move
                self._set_cell(c_from, EMPTY)
                self._set_cell(c_to, player)
            else:
                # this is a place move
                self._set_cell(move, player)
                if player == WHITE:
                    self._p1_w_count += 1
                elif player == BLACK:
                    self._p1_b_count += 1
        if lawful:
            if self._phase == 1 and self._p1_w_count == 12 and self._p1_b_count == 12:
                self._phase = 2
            pc = self.get_pieces_count(player)
            ec = self.get_pieces_count(get_enemy(player))
            self.elim_all(get_enemy(player))
            self.elim_all(player)
            if self._p2_turn in [128, 192, 224]:
                self.shrink()
            pc -= self.get_pieces_count(player)
            ec -= self.get_pieces_count(get_enemy(player))
            return ec - pc

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
        return coord.x in range(self._start, self._size - self._start) and coord.y in range(self._start,
                                                                                            self._size - self._start)

    def is_win(self, player: Piece = None):
        # part A: u win if u have no enemy left
        if player is not None:
            if len(self.index(get_enemy(player))) == 0:
                return player
            else:
                return
        # if player is None, then caller just wants to know if theres a winner or not doesnt care who
        if self.is_win(WHITE):
            return WHITE
        else:
            return self.is_win(BLACK)

    def is_end(self):
        # part B: The game ends if either player has fewer than 2 pieces remaining. In this case, the player
        # with 2 or more pieces remaining wins the game. If both players have fewer than 2 pieces
        # remaining as a result of the same turn (for example, due to multiple pieces being eliminated
        # during the shrinking of the board), then the game ends in a tie.
        if self._phase != 2:
            return None
        white_count = len(self._index_white)
        black_count = len(self._index_black)
        if white_count < 2 and black_count < 2:
            return {WHITE, BLACK}  # tie is represented by a set containing both W&B
        elif white_count < 2:
            return BLACK
        elif black_count < 2:
            return WHITE
        else:
            return None
