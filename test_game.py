from unittest import TestCase
from game import MinesweeperGame
import numpy as np

class TestMinesweeperGame(TestCase):

    def setUp(self):
        self.game = MinesweeperGame(9,1)

    def test__generate_board(self):
        print("test__generate_board")
        #Check if two generated game boards aren't the same
        result1 = self.game._generate_board(9,1)
        result2 = self.game._generate_board(9,1)

        self.assertTrue(np.array_equal(result1, result2))

        print("Test passed")

    def test__place_bombs(self):
        print("test__place_bombs")
        bomb_locations = self.game._place_bombs()
        num_bombs = len(bomb_locations)

        #Check that the number of bombs placed is correct
        self.assertEqual(num_bombs, 1)

        #Check that all bomb locations are valid
        for row, col in bomb_locations:
            self.assertLess(row, 3)
            self.assertLess(col, 3)
            self.assertEqual(self.game.board[row][col], -1)

        print("Test passed")

    def test__get_neighbors(self):
        print("test__get_neighbors")
        #Test the center cell
        neighbors = self.game._get_neighbors(1, 1)
        expected_neighbors = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
        self.assertCountEqual(neighbors, expected_neighbors)

        print("Test passed")

    def test__get_num_adjacent_bombs(self):
        print("test__get_num_adjacent_bombs")
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

        print("Test passed")

    def test__reveal(self):
        print("test__reveal")
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
        print(f"Score after revealing a 1-tile {self.game.score}")

        #Revealing a bomb tile and checking if revealing it ends the game
        result = self.game._reveal(1, 1)
        self.assertTrue(self.game.game_over)
        print(f"Score after revealing a bomb tile {self.game.score}")

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

        print("Test passed")

    def test__reveal_zeroes(self):
        print("test__reveal_zeroes")
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

        print("Test passed")

    def test__flag(self):
        print("test__flag")
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
        print(f"Score after flagging an already flagged tile: {self.game.score}")
        self.assertEqual(self.game.score, -1)

        #Flagging a bomb
        self.game._flag(2,2)
        print(f"Score after flagging a bomb: {self.game.score}")
        self.assertEqual(self.game.score, 0)

        #Unflagging a bomb
        self.game._flag(2,2)
        print(f"Score after unflagging a bomb: {self.game.score}")
        self.assertEqual(self.game.score, -1)

        print("Test passed")

    def test__make_move(self):
        print("test__make_move")
        self.game.score = 0
        self.game.board = self.game.board = np.array([
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, -1]
        ])

        self.game.hidden_board = np.array([
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']
        ])

        #Reveal a zero tile
        action = (0,0,'R')

        self.game._make_move(action)

        self.assertEqual(int(self.game.hidden_board[0][0]), 0)
        self.assertEqual(int(self.game.hidden_board[0][1]), 0)
        self.assertEqual(int(self.game.hidden_board[0][2]), 0)
        self.assertEqual(int(self.game.hidden_board[1][0]), 0)
        self.assertEqual(int(self.game.hidden_board[2][0]), 0)

        #Reveal a non-zero tile
        action = (1,1,'R')

        self.game._make_move(action)
        self.assertEqual(int(self.game.hidden_board[1][1]), 1)

        #Flag a bomb
        action = (2,2,'F')

        self.game._make_move(action)
        self.assertEqual(self.game.hidden_board[2][2], 'F')

        #Unflag a bomb
        action = (2, 2,'F')

        self.game._make_move(action)
        self.assertEqual(self.game.hidden_board[2][2], '-')

        #Reveal a bomb
        action = (2,2,'R')

        self.game._make_move(action)
        self.assertEqual(self.game.hidden_board[2][2], '-')
        self.assertEqual(self.game.game_over, True)

        print("Test passed")

    def test__get_state(self):
        print("test__get_state")
        self.game.score = 0
        self.game.board = self.game.board = np.array([
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, -1]
        ])

        self.game.hidden_board = np.array([
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']
        ])

        #Checking return statement after making no moves
        lost, score, board = self.game._get_state()

        self.game.expected_board = np.array([
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']
        ])

        assert not lost
        self.assertEqual(score, 0)
        self.assertTrue(np.array_equal(board, self.game.expected_board))

        #Checking return statement after making a valid move
        action = (1,1,'R')
        self.game._make_move(action)
        lost, score, board = self.game._get_state()

        self.game.expected_board = np.array([
            ['-', '-', '-'],
            ['-', '1', '-'],
            ['-', '-', '-']
        ])

        assert not lost
        self.assertEqual(score, 1)
        self.assertTrue(np.array_equal(board, self.game.expected_board))

        #Checking return statement after losing a game
        action = (2,2,'R')
        self.game._make_move(action)
        lost, score, board = self.game._get_state()

        assert lost
        self.assertEqual(score, -9)
        self.assertTrue(np.array_equal(board, self.game.board))

        print("Test passed")

    def test__reset(self):
        pass