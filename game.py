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
        self.revealed_tiles = 0


    def _place_bombs(self):
        bomb_locations = random.sample(range(self.board_size * self.board_size), self.num_bombs)
        bomb_locations = [(i // self.board_size, i % self.board_size) for i in bomb_locations]

        for i, j in bomb_locations:
            self.board[i][j] = -1
        self.board = self.board.astype(int) #Cast to int
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
            if self.board[neighbor_row][neighbor_col] == -1:
                num_adjacent_bombs += 1
        return num_adjacent_bombs

    def _reveal(self, row, col):
        if self.hidden_board[row][col] == '-':
            if self.board[row][col] == -1:
                self.score -= 10
                self.game_over = True
                self.revealed_tiles += 1
                return self.board[row][col]
            elif self.board[row][col] == 0:
                #Reveal all the adjacent tiles with DFS algorithm
                self.score += 1
                self.revealed_tiles = self._reveal_zeroes(row, col, self.revealed_tiles)
            else:
                #Reveal the tile
                self.score += 1
                self.hidden_board[row][col] = str(self.board[row][col])
                self.revealed_tiles += 1
                return self.board[row][col]
        else:
            self.score -= 1
            print("This tile has already been revealed")
            return None

        if self.revealed_tiles == self.board_size ** 2 - self.num_bombs:
            #All non-bomb tiles have been revealed
            self.score += 10
            self.game_over = True

    def _reveal_zeroes(self, row, col, revealed_tiles):
        # Revealing 0's with DFS algorithm
        if self.hidden_board[row][col] == '-':
            if self.board[row][col] != 0:
                self.hidden_board[row][col] = self.board[row][col]
                revealed_tiles += 1
            else:
                self.hidden_board[row][col] = '0'
                revealed_tiles += 1
                for r in range(max(0, row - 1), min(row + 2, len(self.board))):
                    for c in range(max(0, col - 1), min(col + 2, len(self.board[0]))):
                        if (r != row or c != col) and self.board[r][c] == 0:
                            revealed_tiles = self._reveal_zeroes(r, c, revealed_tiles)
                        elif (r != row or c != col) and self.board[r][c] != -1:
                            self.hidden_board[r][c] = self.board[r][c]
                            revealed_tiles += 1
        return revealed_tiles

    def _flag(self, row, col):
        if self.hidden_board[row][col] == '-':
            self.hidden_board[row][col] = 'F'
            #Increase the score if flagged tile was a bomb
            if self.board[row][col] == -1:
                self.score += 1
            return True

        elif self.hidden_board[row][col] == 'F':
            self.hidden_board[row][col] = '-'
            #Decrease the score if unflagged tile was a bomb
            if self.board[row][col] == -1:
                self.score -= 1
            return True

        else:
            print("This tile has already been revealed and cannot be flagged")
            self.score -= 1
            return False

    def _make_move(self, action):
        row, col, move = action
        if move == 'R':
            self._reveal(row, col)
        elif move == 'F':
            self._flag(row, col)
        else:
            print("Invalid action")

    def _get_state(self):
        if not self.game_over:
            return self.game_over, self.score, self.hidden_board
        else:
            return self.game_over, self.score, self.board

    def _reset(self):
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

    print("Done")