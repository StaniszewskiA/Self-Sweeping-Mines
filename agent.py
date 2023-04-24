import random
import unittest
from game import MinesweeperGame

#class QLearningAgent:



def main():
    pass

if __name__ == "__main__":
    main()

    board_size = 9
    bombs = 10

    actions = []
    for i in range(10):
        for j in range(10):
            actions.extend([(i, j, 'R'), (i, j, 'F')])  #Append each tuple separately




