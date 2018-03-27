import typing

CORNER = 'X'
WHITE = 'O'
BLACK = '@'
EMPTY = '-'


class BlankBoard:
    board = []
    size = 0

    index_white = []
    index_black = []

    def __init__(self, size: int = 8):
        self.size = size
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.board[0][0] = self.board[0][-1] = self.board[-1][0] = self.board[-1][-1] = CORNER

    def set_row(self, y: int, line: typing.List[str]):
        # if len(line) != self.size:
        # WARNING incorrect size!
        for x in range(self.size):
            self.set_cell(x, y, line[x])

    def set_cell(self, x: int, y: int, piece: str):
        if (x == 0 or x == self.size - 1) and (y == 0 or y == self.size - 1):
            return
        # if piece not in [EMPTY, BLACK, WHITE]:
        # WARNING illegal piece
        # also should not place anything on a non-empty cell
        self.board[y][x] = piece
        if piece == WHITE:
            self.index_white.append((x, y))
        elif piece == BLACK:
            self.index_black.append((x, y))

    def is_cell_valid(self, x: int, y: int):
        # here (x,y) may be dum values
        if x not in range(self.size) or y not in range(self.size):
            return False
        return self.board[y][x] == EMPTY

    def get_valid_moves(self, xy: tuple):
        valid = []
        # TODO ugly write better pls
        x = xy[0]
        y = xy[1]
        # north
        if self.is_cell_valid(x, y - 1):
            valid.append((x, y - 1))
        elif self.is_cell_valid(x, y - 2):
            valid.append((x, y - 2))

        # east
        if self.is_cell_valid(x + 1, y):
            valid.append((x + 1, y))
        elif self.is_cell_valid(x + 2, y):
            valid.append((x + 2, y))

        # south
        if self.is_cell_valid(x, y + 1):
            valid.append((x, y + 1))
        elif self.is_cell_valid(x, y + 2):
            valid.append((x, y + 2))

        # west
        if self.is_cell_valid(x - 1, y):
            valid.append((x - 1, y))
        elif self.is_cell_valid(x - 2, y):
            valid.append((x - 2, y))
        return valid

    def print_board(self):
        for row in self.board:
            print(' '.join(row))


def get_board_from_file(file: typing.TextIO, size: int = None):
    firstline = file.readline().strip().split(' ')
    if size is None:
        size = len(firstline)
    board = BlankBoard(size)
    board.set_row(0, firstline)
    for y in range(1, size):
        board.set_row(y, file.readline().strip().split(' '))
    return board
