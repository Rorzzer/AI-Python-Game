import watchurback


# white then black
def on_action(action: str, board: watchurback.Board):
    # calculate white moves
    white_moves = 0
    for white in board.__index_white:
        moves = board.get_valid_moves(white)
        white_moves += len(moves)
    print(white_moves)

    # calculate black moves
    black_moves = 0
    for black in board.__index_black:
        moves = board.get_valid_moves(black)
        black_moves += len(moves)
    print(black_moves)
