import watchurback

WHITE = 'white'
BLACK = 'black'
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
NONE = 'none'
corner1 = (0, 0)
corner2 = (7, 0)
corner3 = (0, 7)
corner4 = (7, 7)


def on_action(action: str, board: watchurback.BlankBoard):
    # TODO

    #piece = 0

    # WILL EVENTUALLY NEED A get_corners() method
    # def get_corners(...

    for ii in board.index_white:
        moves = board.get_valid_moves(ii)
        piece = 0
        # move_status = (piece, can_take(ii), is_vuln(ii), next_to_white(ii), avg_dist_to_black(ii))
        for jj in moves:
            print("Moving piece:", ii, " to:", jj)
            print("Can take: ",can_take_total(board, jj), " pieces")
            piece += 1
            #import pdb; pdb.set_trace()

    print('MASSACRE still being implemented.')


# def is_vuln()


def can_take_total(board: watchurback.BlankBoard, xy: tuple):
    x = xy[0]
    y = xy[1]
    total = 0

    # import pdb;
    # pdb.set_trace()

    if check_left(1, BLACK, board, x, y) and check_left(2, WHITE, board, x, y):
        total += 1

    if check_right(1, BLACK, board, x, y) and check_right(2, WHITE, board, x, y):
        total += 1

    if check_up(1, BLACK, board, x, y) and check_up(2, WHITE, board, x, y):
        total += 1

    if check_down(1, BLACK, board, x, y) and check_down(2, WHITE, board, x, y):
        total += 1

    return total


def is_vulnerable(board: watchurback.BlankBoard, xy: tuple):
    x = xy[0]
    y = xy[1]

    return True
    # return next_to(BLACK, board, x, y) and two_spaces_away(WHITE, board, x, y)


def check_left(distance, colour, board: watchurback.BlankBoard, x, y):
    # returns true if piece to the left

    if colour == BLACK:
        for ii in board.index_black:
            if ((x - distance), y) == (ii[0], ii[1]):
                return True
        return False
    elif colour == WHITE:
        for ii in board.index_white:
            if ((x - distance), y) == (ii[0], ii[1]):
                return True
        return False


def check_right(distance, colour, board: watchurback.BlankBoard, x, y):
    # returns true if piece to the right

    if colour == BLACK:
        for ii in board.index_black:
            if ((x + distance), y) == (ii[0], ii[1]):
                return True
        return False
    elif colour == WHITE:
        for ii in board.index_white:
            if ((x + distance), y) == (ii[0], ii[1]):
                return True
        return False


def check_up(distance, colour, board: watchurback.BlankBoard, x, y):
    # returns true if piece above

    if colour == BLACK:
        for ii in board.index_black:
            if (x, (y - distance)) == (ii[0], ii[1]):
                return True
        return False
    elif colour == WHITE:
        for ii in board.index_white:
            if (x, (y - distance)) == (ii[0], ii[1]):
                return True
        return False


def check_down(distance, colour, board: watchurback.BlankBoard, x, y):
    # returns true if piece below

    if colour == BLACK:
        for ii in board.index_black:
            if (x, (y + distance)) == (ii[0], ii[1]):
                return True
        return False

    elif colour == WHITE:
        for ii in board.index_white:
            if (x, (y + distance)) == (ii[0], ii[1]):
                return True
        return False

