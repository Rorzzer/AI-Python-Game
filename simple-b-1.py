import time

import partb
import watchurback

player = partb.Player("white")
player.board = watchurback.Board.new_empty()
# player.board._phase = 2
enemy = partb.Player("black")
enemy.board = player.board.branch()
# enemy.board._phase = 2

turn = 0

start = time.time()
delta = start
print("Game start")
while [player, enemy][turn % 2].board.is_end() is None:
    [player, enemy][turn % 2].board.print_board()
    action = [player, enemy][turn % 2].action(turn)
    [enemy, player][turn % 2].update(action)
    now = time.time()
    print([player.colour, enemy.colour][turn % 2], action, "t=", now - start, 'd=', now - delta)
    print("turn", player.board._turn, player.board._p2_turn, "white", len(player.board.index('O')), "black",
          len(player.board.index('@')))
    print("w-score", player.board.evaluate_detail("O", "@", 0.7))
    delta = now
    turn += 1

player.board.print_board()
