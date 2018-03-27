import watchurback

WHITE = 'white'
BLACK = 'black'
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


def on_action(action: str, board: watchurback.BlankBoard):
    # TODO

    counter = 0
    # WILL EVENTUALLY NEED A get_corners() method
    # def get_corners(...

    # for each white piece
    for ii in board.index_white:
        # move_status = (piece, can_take(ii), is_vuln(ii), next_to_count(ii), avg_MHdist_to_black(ii))

        board.index_white.remove(ii)
        moves = board.get_valid_moves(ii)

        # for each move of each piece
        for jj in moves:
            print(ii, "->", jj)
            print("Can take: ", can_elim_count(board, jj), " pieces")
            print("Is surrounded: ", is_surrounded(board, jj))
            print("Next to: ", next_to_count(WHITE, board, jj), " white pieces")
            print("Next to: ", next_to_count(BLACK, board, jj), " black pieces")

            # import pdb; pdb.set_trace()
        board.index_white.insert(0, ii)

    print('MASSACRE still being implemented.')


def can_elim_count(board: watchurback.BlankBoard, xy: tuple):
    x = xy[0]
    y = xy[1]
    total = 0

    # import pdb;
    # pdb.set_trace()

    if check_left(NEXT_TO, BLACK, board, x, y) and check_left(TWO_AWAY, WHITE, board, x, y):
        total += 1

    if check_right(NEXT_TO, BLACK, board, x, y) and check_right(TWO_AWAY, WHITE, board, x, y):
        total += 1

    if check_up(NEXT_TO, BLACK, board, x, y) and check_up(TWO_AWAY, WHITE, board, x, y):
        total += 1

    if check_down(NEXT_TO, BLACK, board, x, y) and check_down(TWO_AWAY, WHITE, board, x, y):
        total += 1

    return total


def is_surrounded(board: watchurback.BlankBoard, xy: tuple):
    # checks if a piece is surrounded after making the move
    x = xy[0]
    y = xy[1]

    return (((check_left(NEXT_TO, BLACK, board, x, y) and check_right(NEXT_TO, BLACK, board, x, y)) or
             (check_up(NEXT_TO, BLACK, board, x, y) and check_down(NEXT_TO, BLACK, board, x, y))) and
            can_elim_count(board, xy) < 3)


def next_to_count(colour, board: watchurback.BlankBoard, xy: tuple):
    # counts the number of neighbouring pieces of a certain colour
    x = xy[0]
    y = xy[1]
    total = 0

    if check_left(NEXT_TO, colour, board, x, y):
        total += 1

    if check_right(NEXT_TO, colour, board, x, y):
        total += 1

    if check_up(NEXT_TO, colour, board, x, y):
        total += 1

    if check_down(NEXT_TO, colour, board, x, y):
        total += 1

    if colour == WHITE:
        return total
    else:
        return total - can_elim_count(board, xy)


def check_left(distance, colour, board: watchurback.BlankBoard, x, y):
    # returns true if piece to the left

    if colour == BLACK:
        for ii in board.index_black:
            if ((x - distance), y) == (ii[0], ii[1]) or \
                    ((x - distance), y) == corner1 or \
                    ((x - distance), y) == corner3:
                return True
        return False
    elif colour == WHITE:
        for ii in board.index_white:
            if ((x - distance), y) == (ii[0], ii[1]) or \
                    ((x - distance), y) == corner1 or \
                    ((x - distance), y) == corner3:
                return True
        return False


def check_right(distance, colour, board: watchurback.BlankBoard, x, y):
    # returns true if piece to the right

    if colour == BLACK:
        for ii in board.index_black:
            if ((x + distance), y) == (ii[0], ii[1]) or \
                    ((x + distance), y) == corner2 or \
                    ((x + distance), y) == corner4:
                return True
        return False
    elif colour == WHITE:
        for ii in board.index_white:
            if ((x + distance), y) == (ii[0], ii[1]) or \
                    ((x + distance), y) == corner2 or \
                    ((x + distance), y) == corner4:
                return True
        return False


def check_up(distance, colour, board: watchurback.BlankBoard, x, y):
    # returns true if piece above

    if colour == BLACK:
        for ii in board.index_black:
            if (x, (y - distance)) == (ii[0], ii[1]) or \
                    (x, (y - distance)) == corner1 or \
                    (x, (y - distance)) == corner2:
                return True
        return False
    elif colour == WHITE:
        for ii in board.index_white:
            if (x, (y - distance)) == (ii[0], ii[1]) or \
                    (x, (y - distance)) == corner1 or \
                    (x, (y - distance)) == corner2:
                return True
        return False


def check_down(distance, colour, board: watchurback.BlankBoard, x, y):
    # returns true if piece below

    if colour == BLACK:
        for ii in board.index_black:
            if (x, (y + distance)) == (ii[0], ii[1]) or \
                    (x, (y + distance)) == corner3 or \
                    (x, (y + distance)) == corner4:
                return True
        return False

    elif colour == WHITE:
        for ii in board.index_white:
            if (x, (y + distance)) == (ii[0], ii[1]) or \
                    (x, (y + distance)) == corner3 or \
                    (x, (y + distance)) == corner4:
                return True
        return False
