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

start = time.time()
delta = start
print("Game start")
while [player, enemy][turn % 2].board.is_end() is None:
    [player, enemy][turn % 2].board.print_board()
    time.sleep(1)
    action = [player, enemy][turn % 2].action(turn)
    [enemy, player][turn % 2].update(action)
    now = time.time()
    print([player.colour, enemy.colour][turn % 2], action, "t=", now - start, 'd=', now - delta)
    delta = now
    turn += 1

player.board.print_board()
