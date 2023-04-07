from unittest import TestCase
from game import MinesweeperGame
import numpy as np

class TestMinesweeperGame(TestCase):

    def setUp(self):
        self.game = MinesweeperGame(3,1)

    def test__place_bombs(self):
        bomb_locations = self.game._place_bombs()
        num_bombs = len(bomb_locations)

        #Check that the number of bombs placed is correct
        self.assertEqual(num_bombs, 1)

        #Check that all bomb locations are valid
        for row, col in bomb_locations:
            self.assertLess(row, 3)
            self.assertLess(col, 3)
            self.assertEqual(self.game.board[row][col], -1)

        print("test__place_bombs passed")

    def test__get_neighbors(self):
        #Test the center cell
        neighbors = self.game._get_neighbors(1, 1)
        expected_neighbors = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
        self.assertCountEqual(neighbors, expected_neighbors)

        print("test__get_neighbors passed")

    def test__get_num_adjacent_bombs(self):
        #Ensure that the method doesn't count the bomb at given position as adjacent
        self.game.board = np.array([
            [0, 0, 0],
            [0, -1, 0],
            [0, 0, 0]
        ])
        num_adjacent_bombs = self.game._get_num_adjacent_bombs(1,1)
        self.assertEqual(num_adjacent_bombs, 0)

        # Ensure that the method count only the bombs at adjacent tiles
        self.game.board = np.array([
            [0, 0, -1],
            [-1, -1, -1],
            [-1, -1, -1]
        ])
        num_adjacent_bombs = self.game._get_num_adjacent_bombs(0, 0)
        self.assertEqual(num_adjacent_bombs, 2)

        # Ensure that the method checks every adjacent tiles
        self.game.board = np.array([
            [-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1]
        ])
        num_adjacent_bombs = self.game._get_num_adjacent_bombs(1,1)
        self.assertEqual(num_adjacent_bombs, 8)

        print("test__get_num_adjecent_bombs passed")

    def test__uncover(self):
        self.game.board = np.array([
            [0, 0, -1],
            [0, 1, 1],
            [0, 1, -1]
        ])

        #Check a tile with no adjacent bombs
        self.game._uncover(0,0)
        self.assertEqual(int(self.game.hidden_board[0][0]), 0)

        #Check a tile with adjacent bomb
        self.game._uncover(2, 1)
        self.assertEqual(int(self.game.hidden_board[2][1]), 1)

        #Check a tile with more adjacent bombs
        self.game._uncover(1, 2)
        self.assertEqual(int(self.game.hidden_board[1][2]), 2)

        # Check a tile with a bomb
        self.game._uncover(0, 2)
        self.assertEqual(self.game.hidden_board[0][2], '*')

        print("test__uncover passed")

    def test__make_move(self):
        pass