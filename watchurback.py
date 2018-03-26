import typing

CORNER = 'X'
WHITE = 'O'
BLACK = '@'
EMPTY = '-'


class BlankBoard:
    board = []
    size = 0

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
        self.board[y][x] = piece

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
