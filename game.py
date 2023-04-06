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
        self.score = 0

    def _place_bombs(self):
        bomb_locations = random.sample(range(self.board_size * self.board_size), self.num_bombs)
        bomb_locations = [(i // self.board_size, i % self.board_size) for i in bomb_locations]

        for i, j in bomb_locations:
            self.board[i][j] = 1
        return bomb_locations

    def _get_neighbors(self, row, col):
        neighbors = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                r = row + i
                c = col + j
                if (
                    r < 0
                    or r >= self.board_size
                    or c < 0
                    or c >= self.board_size
                ):
                    continue
                neighbors.append((r,c))
        return neighbors

    def _get_num_adjacent_bombs(self, row, col):
        num_adjacent_bombs = 0
        for neighbor_row, neighbor_col in self._get_neighbors(row, col):
            if self.board[neighbor_row][neighbor_col] == 1:
                num_adjacent_bombs += 1
        return num_adjacent_bombs

    def _uncover(self, row, col):
        if self.hidden_board[row][col] != '-':
            #Cell has already been uncovered
            return

        if self.board[row][col] == 1:
            #Cell is a bomb
            self.hidden_board[row][col] = '*'
            self.game_over = True
            return

        num_adjacent_bombs = self._get_num_adjacent_bombs(row, col)
        if num_adjacent_bombs == 0:
            #Recursively uncover all neighbors
            self.hidden_board[row][col] = ' '
            neighbors = self._get_neighbors(row, col)
            for neighbor_row, neighbor_col in neighbors:
                self._uncover(neighbor_row, neighbor_col)

        else:
            self.hidden_board[row][col] = str(num_adjacent_bombs)

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