import watchurback

WHITE = 'white'
BLACK = 'black'

def on_action(action: str, board: watchurback.BlankBoard):
    # TODO

    piece = 0

    for ii in board.index_white:
        moves = board.get_valid_moves(ii)
        #move_status = (piece, can_take(ii), is_vuln(ii), next_to_white(ii), avg_dist_to_black(ii))
        can_take(board, ii)
        piece += 1
        # import pdb; pdb.set_trace()

    print('MASSACRE still being implemented.')

def is_vuln()

def can_take(board: watchurback.BlankBoard, xy: tuple):
    x = xy[0]
    y = xy[1]

    return next_to(BLACK, board, x, y) and two_spaces_away(WHITE, board, x, y)


def next_to(colour, board: watchurback.BlankBoard, x, y):
    # returns whether a piece is next to x,y
    if colour == BLACK:
        for ii in board.index_black:
            if ((x + 1 == ii[0] or x - 1 == ii[0]) and (y == ii[1])) or \
                ((y + 1 == ii[1] or y - 1 == ii[1]) and (x == ii[0])):
                return True
            else:
                return False
    elif colour == WHITE:
        for ii in board.index_white:
            if ((x + 1 == ii[0] or x - 1 == ii[0]) and (y == ii[1])) or \
                    ((y + 1 == ii[1] or y - 1 == ii[1]) and (x == ii[0])):
                return True
            else:
                return False
    else: return False


def two_spaces_away(colour, board: watchurback.BlankBoard, x, y):
    # returns whether a piece is 2 places away from x,y
    if colour == WHITE:
        for ii in board.index_white:
            if ((x + 2 == ii[0] or x - 2 == ii[0]) and (y == ii[1])) or \
                    ((y + 2 == ii[1] or y - 2 == ii[1]) and (x == ii[0])):
                return True
            else:
                return False
    elif colour == BLACK:
        for ii in board.index_black:
            if ((x + 2 == ii[0] or x - 2 == ii[0]) and (y == ii[1])) or \
                    ((y + 2 == ii[1] or y - 2 == ii[1]) and (x == ii[0])):
                return True
            else:
                return False
    else: return False