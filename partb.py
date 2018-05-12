# Part B
# File: partb.py
#
# TEAM The Dream Team

import time
from operator import itemgetter

from watchurback import Board, BLACK, WHITE, Piece, get_enemy

WHITE_STRING = "white"
BLACK_STRING = "black"
INF = float("inf")


class Player:
    min_depth = 1
    max_depth = 10
    fast_mark = 0.4
    slow_mark = 2.2

    def __init__(self, colour_string: str):
        self.board: Board = Board.new_empty()
        self.colour: Piece
        self.target_depth = 2

        # input_file = open("/sample_files/massacre-sample-6.in")

        # loads the board
        # board = Board.from_file(input_file)
        # self.board = Board.from_file(input_file)

        # string is the human word, internally we store as piece char (@ or O)
        if colour_string == WHITE_STRING:
            self.colour = WHITE
        elif colour_string == BLACK_STRING:
            self.colour = BLACK
        self.enemy_colour: Piece = get_enemy(self.colour)

    def action(self, turns: int):

        # To place piece on board return a tuple (x, y)
        # To move a piece return nested tuple ((a, b), (c, d))
        # to forfeit turn return 'None'

        # if turns < 24:
        # move = tuple(map(int, input("move:").split(',')))
        # return move
        # else:
        #    return MiniMax(self, 10)
        start = time.time()
        # if self.board._phase == 1:
        #    self.target_depth = 1
        print("depth=", self.target_depth)
        if self.board._phase == 1:
            aggressive = 0.4
        else:
            if self.board.get_pieces_count(self.colour) / self.board.get_pieces_count(self.enemy_colour) > 1.2:
                aggressive = 0.8
            else:
                aggressive = 0.6
        score, move = MiniMax(self, aggressive).minimax(self.target_depth)
        end = time.time() - start
        if end < Player.fast_mark and self.target_depth < Player.max_depth:
            print("too fast, adding depth")
            self.target_depth += 1
        elif end > Player.slow_mark and self.target_depth > Player.min_depth:
            print("too slow, removing depth")
            self.target_depth -= 1
        self.board.move(move, self.colour)
        return move

    def update(self, action):

        # if action.turns < 24:
        #     return
        # else:
        #     self.board.move(action)
        # called by referee to update board and opponents move
        self.board.move(action, self.enemy_colour)
        return


# MINIMAX implementation

class MiniMax:

    def __init__(self, player: Player, aggressive: float):
        self.player: Player = player
        self.enemy_colour: Piece = get_enemy(player.colour)
        self.aggressive = aggressive
        # self.best_move = None
        # self.best_score = float('-inf')

    def minimax(self, depth: int):
        return self._minimax(self.player.board, depth, -INF, INF, True)

    def _minimax(self, board: Board, depth: int, alpha: float, beta: float, maximising: bool):
        if depth <= 0:
            return board.evaluate_detail(self.player.colour, self.enemy_colour, self.aggressive), None
        is_end = board.is_end()
        if isinstance(is_end, set):
            return 0, None
        elif is_end == self.player.colour:
            return INF, None
        elif is_end == self.enemy_colour:
            return -INF, None

        if maximising:
            best = (-INF, None)
            moves = []
            for move in board.get_valid_moves_b(self.player.colour):
                child = board.branch()
                score = child.move(move, self.player.colour)
                moves.append((score, child, move))
            moves.sort(key=itemgetter(0), reverse=True)
            for _, child, move in moves:
                score, _ = self._minimax(child, depth - 1, alpha, beta, False)
                best = max(best, (score, move), key=itemgetter(0))
                alpha = max(alpha, best[0])
                if beta <= alpha:
                    break
                # print("Depth:",depth,"Score:",score,"Move:",move)
            return best
        else:
            best = (INF, None)
            moves = []
            for move in board.get_valid_moves_b(self.enemy_colour):
                child = board.branch()
                score = child.move(move, self.enemy_colour)
                moves.append((score, child, move))
            moves.sort(key=itemgetter(0), reverse=True)
            for _, child, move in moves:
                score, _ = self._minimax(child, depth - 1, alpha, beta, True)
                best = min(best, (score, move), key=itemgetter(0))
                beta = min(beta, best[0])
                if beta <= alpha:
                    break
            return best

