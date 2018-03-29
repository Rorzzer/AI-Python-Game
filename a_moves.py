from watchurback import Board, WHITE, BLACK


# white then black
def on_action(action: str, board: Board):
    # calculate white moves
    white_moves = 0
    for white in board.index(WHITE):
        moves = board.get_valid_moves(white)
        white_moves += len(moves)
    print(white_moves)

    # calculate black moves
    black_moves = 0
    for black in board.index(BLACK):
        moves = board.get_valid_moves(black)
        black_moves += len(moves)
    print(black_moves)
