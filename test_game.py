from unittest import TestCase
from  gameForAI import MinesweeperGame

class TestMinesweeperGame(TestCase):

    def test__place_bombs(self):
        game = MinesweeperGame(5, 3)
        bomb_locations = game._place_bombs()
        num_bombs = len(bomb_locations)

        #Check that the number of bobms placed is correct
        self.assertEqual(num_bombs, 3)

        #Check that all bomb locations are valid
        for row, col in bomb_locations:
            self.assertLess(row, 5)
            self.assertLess(col, 5)
            self.assertEqual(game.board[row][col], 1)

        print("test__place_bombs passed")

    def test__get_neighbors(self):
        pass

    def test__get_num_adjecent_bombs(self):
        pass

    def test__uncover(self):
        pass

    def test__make_move(self):
        pass

    def test__get_state(self):
        pass