# Part B
# File: partb.py
#
# TEAM The Dream Team

from operator import itemgetter

from watchurback import Board, BLACK, WHITE, Piece, get_enemy

WHITE_STRING = "white"
BLACK_STRING = "black"
INF = float("inf")


class Player:

    def __init__(self, colour_string: str):
        self.board: Board = Board.new_empty()
        self.colour: Piece

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
        score, move = MiniMax(self).minimax(3)
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

    def __init__(self, player: Player):
        self.player: Player = player
        self.enemy_colour: Piece = get_enemy(player.colour)
        # self.best_move = None
        # self.best_score = float('-inf')

    def minimax(self, depth: int):
        return self._minimax(self.player.board, depth, True)

    def _minimax(self, board: Board, depth: int, maximising: bool):
        if depth <= 0:
            return board.evaluation_function(self.player.colour if maximising else self.enemy_colour), None
        is_end = board.is_end()
        if isinstance(is_end, set):
            return 0, None
        elif is_end == self.player.colour:
            return INF, None
        elif is_end == self.enemy_colour:
            return -INF, None

        if maximising:
            best = (-INF, None)
            for move in board.get_valid_moves_b(self.player.colour):
                child = board.branch()
                child.move(move, self.player.colour)
                score, _ = self._minimax(child, depth - 1, False)
                best = max(best, (score, move), key=itemgetter(0))
                # print("Depth:",depth,"Score:",score,"Move:",move)
            return best
        else:
            best = (INF, None)
            for move in board.get_valid_moves_b(self.enemy_colour):
                child = board.branch()
                child.move(move, self.enemy_colour)
                score, _ = self._minimax(child, depth - 1, True)
                best = min(best, (score, move), key=itemgetter(0))
            return best

    # def minimax2(self):
    #     colour = self.player.colour
    #     # board = player.board  # current board
    #
    #     # nonlocal bestscore  #= float('-inf')
    #     # nonlocal bestmove
    #     # bestscore = float('-inf')
    #
    #     for piece in self.board.index(colour):
    #         moves = self.board.get_valid_moves(piece)
    #
    #         for move in moves:
    #             newboard = self.board.branch()
    #             newboard.move(piece, move)
    #
    #             if self.depth < MiniMax.current_depth:
    #                 MiniMax.current_depth += 1
    #                 score = MiniMax.min_play(newboard, player)
    #
    #             if score > bestscore:
    #                 MiniMax.bestmove = move
    #                 bestscore = score
    #
    #             else:
    #                 MiniMax.bestmove = moves[0]
    #
    #     return MiniMax.bestmove
    #
    # def min_play(self, board, player):
    #     colour = player.colour
    #
    #     # check if game is not over, to be implemented
    #     if board.is_win() == colour:
    #         return float('inf')  # evaluation_function(board)
    #     elif board.is_win() == get_enemy(colour):
    #         return float('-inf')  # -evalutation_fucntion(board)
    #
    #     bestscore = float('inf')
    #
    #     for piece in board.index(get_enemy(colour)):
    #         moves = board.get_valid_moves(get_enemy(colour))
    #
    #         for move in moves:
    #             newboard = board.branch()
    #             newboard.move(piece, move)
    #             score = MiniMax.max_play(newboard, player)
    #
    #             if score < bestscore:
    #                 MiniMax.bestmove = move
    #                 bestscore = score
    #
    #     return bestscore
    #
    # def max_play(self, board, player):
    #     if board.is_win() == player.colour:
    #         return float('inf')  # evaluation_function(board)
    #     elif board.is_win() == get_enemy(player.colour):
    #         return float('-inf')  # -evalutation_fucntion(board)
    #
    #     bestscore = float('-inf')
    #
    #     for piece in board.index(get_enemy(player.colour)):
    #         moves = board.get_valid_moves(get_enemy(player.colour))
    #
    #         for move in moves:
    #             newboard = board.branch()
    #             newboard.move(piece, move)
    #             score = MiniMax.min_play(newboard, player)
    #
    #             if score > bestscore:
    #                 MiniMax.bestmove = move
    #                 bestscore = score
    #
    #     return bestscore
