import time

import partb
import watchurback

board = "sample_files/massacre-sample-5.in"

player = partb.Player("white")
player.board = watchurback.Board.from_file(open(board))
player.board._phase = 2
enemy = partb.Player("black")
enemy.board = player.board.branch()
enemy.board._phase = 2

turn = 0

while [player, enemy][turn % 2].board.is_end() is None:
    [player, enemy][turn % 2].board.print_board()
    time.sleep(1)
    action = [player, enemy][turn % 2].action(turn)
    [enemy, player][turn % 2].update(action)
    print([player.colour, enemy.colour][turn % 2], action)
    turn += 1

player.board.print_board()
