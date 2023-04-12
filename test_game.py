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


    def test__get_neighbors(self):
        #Test the center cell
        neighbors = self.game._get_neighbors(1, 1)
        expected_neighbors = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
        self.assertCountEqual(neighbors, expected_neighbors)


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

    def test__reveal(self):
        self.game.board = np.array([
            [1, 1, 1],
            [1, -1, 1],
            [1, 1, 1]
        ])

        self.game.hidden_board = np.array([
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']
        ])

        #Revealing a non-bomb tile
        result = self.game._reveal(0, 0)
        self.assertEqual(result, 1)

        #Revealing a bomb tile and checking if revealing it ends the game
        result = self.game._reveal(1, 1)
        self.assertTrue(self.game.game_over)


        #Check the scoring system
        self.game.score = 0

        self.game.board = self.game.board = np.array([
            [0, 1, 1],
            [0, 1, -1],
            [0, 1, 1]
        ])

        self.game.hidden_board = np.array([
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']
        ])

        self.game._reveal(0,0)
        self.assertEqual(self.game.score, 1)

        self.game._reveal(1,1)
        self.assertEqual(self.game.score, 0)

        self.game._reveal(0,2)
        self.assertEqual(self.game.score, 1)

        self.game._reveal(1,2)
        self.assertEqual(self.game.score, -9)

    def test__reveal_zeroes(self):
        # Revealing 0s
        self.game.board = self.game.board = np.array([
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, 1]
        ])

        self.game.hidden_board = np.array([
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']
        ])

        self.game.expected_board = np.array([
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, '-']
        ])

        self.game._reveal(0, 0)
        self.assertTrue(np.array_equal(self.game.hidden_board, self.game.expected_board))

    def test__flag(self):
        #Test flagging a tile that has not been revealed
        self.game.hidden_board = np.array([
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']
        ])

        result = self.game._flag(0,0)
        self.assertEqual(self.game.hidden_board[0][0], 'F')
        self.assertEqual(result, True)

        #Test unflagging a flagged tile
        result = self.game._flag(0,0)
        self.assertEqual(self.game.hidden_board[0][0], '-')
        self.assertEqual(result, True)

        #Test flagging an already revealed tile
        self.game.hidden_board = np.array([
            [1, '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']
        ])
        result = self.game._flag(0,0)
        self.assertEqual(result, False)

        #Test flagging a bomb and scoring system
        self.game.board = self.game.board = np.array([
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, -1]
        ])
        self.game.hidden_board = np.array([
            ['0', '0', '0'],
            ['0', '1', '1'],
            ['0', '1', '-']
        ])

        #Flagging an already revealed tile
        self.game.score = 0
        self.game._flag(0,0)
        self.assertEqual(self.game.score, -1)

        #Flagging a bomb
        self.game._flag(2,2)
        self.assertEqual(self.game.score, 0)

        #Unflagging a bomb
        self.game._flag(2,2)
        self.assertEqual(self.game.score, -1)


    def test__make_move(self):
        pass

    def test__board_state(self):
        pass