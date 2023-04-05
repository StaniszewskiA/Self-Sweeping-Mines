import random
import numpy as np
import unittest

class MinesweeperGame:
    def __init__(self, board_size, num_bombs):
        self.board_size = board_size
        self.num_bombs = num_bombs
        self.board = np.zeros((self.board_size, self.board_size))
        self.hidden_board = np.full((self.board_size, self.board_size), '-')
        self.bomb_locations = self._place_bombs()
        self.game_over = False

    def _place_bombs(self):
        bomb_locations = random.sample(range(self.board_size * self.board_size), self.num_bombs)
        bomb_locations = [(i // self.board_size, i % self.board_size) for i in bomb_locations]

        for i, j in bomb_locations:
            self.board[i][j] = 1
        return bomb_locations

    def _get_neighbors(self, row, col):
        pass

    def _get_num_adjecent_bombs(self, row, col):
        pass

    def _uncover(self, row, col):
        pass

    def _make_move(self, row, col, action):
        pass

    def _get_state(self):
        pass

def main():
    from test_game import TestMinesweeperGame
    #Creating a test suite
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite((TestMinesweeperGame)))

    #Run the test suite
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

if __name__ == "__main__":
    main()

    print("It works")