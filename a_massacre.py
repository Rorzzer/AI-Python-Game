import watchurback


def on_action(action: str, board: watchurback.BlankBoard):
    # TODO
    for ii in board.index_white:
        moves = board.get_valid_moves(ii)
        # import pdb; pdb.set_trace()

    print('MASSACRE Not yet implemented.')
