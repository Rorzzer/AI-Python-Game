import watchurback


# white then black
def on_action(action: str, board: watchurback.BlankBoard):
    white_moves = 0
    for white in board.index_white:
        (x, y) = white
        moves = board.get_valid_moves(x, y)
        white_moves += len(moves)
    print(white_moves)

    black_moves = 0
    for black in board.index_black:
        (x, y) = black
        moves = board.get_valid_moves(x, y)
        black_moves += len(moves)
    print(black_moves)
