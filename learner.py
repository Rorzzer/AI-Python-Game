
import referee
import random


class weights:
    def __init__(self):
        self.aggressive = random.random()
        self.weight1 = random.randint(1, 4)
        self.weight2 = random.randint(1, 6)
        self.weight3 = random.random()


wweight = weights()
bweight = weights()

for x in range(1, 5):
    winner = referee.main()

    if winner == 'W':
        winningweight = wweight
        bweight = weights()
        print(winningweight)

    elif winner == 'B':
        winningweight = bweight
        wweight = weights()
        print(winningweight)

