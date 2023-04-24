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
    for i in range(board_size+1):
        for j in range(board_size+1):
            actions.extend([(i, j, 'R'), (i, j, 'F')])  #Append each tuple separately




