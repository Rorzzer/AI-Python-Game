import itertools

from spatial_utils import Coord, PAIRS, add_direction
from watchurback import Board, BLACK, WHITE, EMPTY, Piece, get_enemy

# WHITE = 'white'
# BLACK = 'black'
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


# currentpiece = (0,0)

class MassacreBoard(Board):
    def __init__(self, board: Board):
        self._board = board._board
        self._size = board._size
        self._index_white = board._index_white
        self._index_black = board._index_black

    def is_elimable(self, coord: Coord):
        """ a coord is eliminatable if it is surrounded (axially) by EMPTY """
        return self.is_surrounded(coord, EMPTY)

    def get_elimable(self, player: Piece):
        return [coord for coord in self.index(player) if self.is_elimable(coord)]

    def get_moves_til_elim_spec(self, target: Coord, killer1: Coord, killer2: Coord):
        """ gets (num moves, route for killer 1, route for killer 2) to kill target """

        # assumes params are sane e.g. target is BLACK and killers are both WHITE cops
        def combined_flight_plan(dir_pair):
            pos1 = add_direction(target, dir_pair[0])
            pos2 = add_direction(target, dir_pair[1])
            # route and distance for each killer to get into position
            (d1, r1) = self.get_min_dist(killer1, pos1, True)
            # R2D2 would have been nicer but distance first is easier to sort
            (d2, r2) = self.get_min_dist(killer2, pos2, True)
            return (d1 + d2, r1, r2)

        return min([combined_flight_plan(dir_pair) for dir_pair in PAIRS])

    def get_moves_til_elim_all(self, target: Coord):
        """ gets (num moves, route, route) for any possible enemy """
        enemies = self.index(get_enemy(
            self.get_piece(target)))
        return min([self.get_moves_til_elim_spec(target, k1, k2)
                    for (k1, k2)
                    in itertools.permutations(enemies, 2)])

    def get_min_moves_til_elim(self, player: Piece):
        return min([self.get_moves_til_elim_all(target) for target in self.index(player)])

    def execute_min_moves_til_elim(self, player: Piece):
        (dist, moves1, moves2) = self.get_min_moves_til_elim(player)
        # moves the furthest one first
        avail_moves = [move for move in [moves1,moves2] if len(move)>1]
        min_move = min(avail_moves, key=len)[:2]
        self.move(min_move[0], min_move[1])
        return min_move


def on_action(action: str, board: Board):
    m_board = MassacreBoard(board)
    while not m_board.is_win():
        m_board.execute_min_moves_til_elim(BLACK)
    m_board.print_board()

    # TODO
    counter = 0

    # WILL EVENTUALLY NEED A get_corners() method
    # def get_corners(...

    # for each white piece
    return
    for ii in board.index_white:
        # move_status = (piece, can_take(ii), is_vuln(ii), next_to_count(ii), avg_MHdist_to_black(ii))

        board.index_white.remove(ii)
        moves = board.get_valid_moves(ii)

        # for each move of each piece
        for jj in moves:
            print("\n\n\n", ii, "->", jj, "\n")
            newindexblack = list(board.index_black)
            print("Can take: ", can_elim_count(board, newindexblack, jj), " pieces")
            print("Is surrounded: ", is_surrounded(board, newindexblack, jj))
            print("Next to: ", next_to_count(WHITE, board, newindexblack, jj), " white pieces")
            print("Next to: ", next_to_count(BLACK, board, newindexblack, jj), " black pieces")

            # import pdb; pdb.set_trace()
        board.index_white.insert(0, ii)

    print('MASSACRE still being implemented.')


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
        for ii in board.__index_white:
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
        for ii in board.__index_white:
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
