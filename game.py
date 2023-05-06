import random
from time import sleep
import numpy as np
import unittest


class MinesweeperGame:
    def __init__(self, board_size, num_bombs):
        self.board_size = board_size
        self.num_bombs = num_bombs
        self.board = None
        self.hidden_board = np.full((self.board_size, self.board_size), '-')
        #self.bomb_locations = self._place_bombs() do wyrzucenia
        self.game_over = False
        self.score = 0
        self.reward = 0
        self.revealed_tiles = 0
        self.score_table = {
            "reveal": 10,
            "flag_correct": 2,
            "flag_incorrect": -5,
            "unflag_bomb": -1,
            "unflag_empty": 0,
            "click_revealed": -5,
            "click_flagged": -5,
            "exploded": -2,
            "win": 20,
        }
        self.moves_taken = []


    def _generate_board(self, board_size, row, col):
        self.board = np.zeros((board_size, board_size), dtype=int)
        self._place_bombs(row, col)

        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x] != -1:
                    self.board[y][x] = self._get_num_adjacent_bombs(y, x)

        return self.board

    def _place_bombs(self, row, col):
        excluded_locations = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                r = row + i
                c = col + j
                if (
                        r < 0
                        or r >= self.board_size
                        or c < 0
                        or c >= self.board_size
                ):
                    continue
                excluded_locations.append(r*self.board_size+c)
        possible_locations = [i for i in range(self.board_size*self.board_size) if i not in excluded_locations]
        bomb_locations = random.sample(possible_locations, self.num_bombs+1)
        bomb_locations = [(i // self.board_size, i % self.board_size) for i in bomb_locations]

        bombs_placed = 0
        for i, j in bomb_locations:
            if i == row and j == col:
                continue
            self.board[i][j] = -1
            bombs_placed+=1
            if bombs_placed == self.num_bombs:
                break
        self.board = self.board.astype(int)  # Cast to int
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
                neighbors.append((r, c))
        return neighbors

    def _get_num_adjacent_bombs(self, row, col):
        num_adjacent_bombs = 0
        for neighbor_row, neighbor_col in self._get_neighbors(row, col):
            if self.board[neighbor_row][neighbor_col] == -1:
                num_adjacent_bombs += 1
        return num_adjacent_bombs

    def _reveal(self, row, col):
        if self.hidden_board[row][col] == '-':
            if self.revealed_tiles == 0:
                self.board = self._generate_board(self.board_size, row, col)
            if self.board[row][col] == -1:
                self.score += self.score_table["exploded"]
                self.reward = self.score_table["exploded"]
                print("Exploded on ",row,col)
                #print(self.board)
                #print(self.hidden_board)
                #print(self.moves_taken)
                self.game_over = True
                self.revealed_tiles += 1
                return self.board[row][col]
            else:
                if self.board[row][col] == 0:
                    # Reveal all the adjacent tiles with DFS algorithm
                    self.score += self.score_table["reveal"]
                    self.reward = self.score_table["reveal"]
                    print("Revealed tile ",row,col)
                    self.revealed_tiles = self._reveal_zeroes(row, col, self.revealed_tiles)
                else:
                    # Reveal the tile
                    self.score += self.score_table["reveal"]
                    self.reward = self.score_table["reveal"]
                    print("Revealed tile ",row,col)
                    self.hidden_board[row][col] = self.board[row][col]
                    self.revealed_tiles += 1
                    
                if self.revealed_tiles == self.board_size ** 2 - self.num_bombs:
                    # All non-bomb tiles have been revealed
                    self.score += self.score_table["win"]
                    self.reward = self.score_table["win"]
                    print("Game won!")
                    self.game_over = True
                return self.board[row][col]
        elif self.hidden_board[row][col] == 'F':
            self.score += self.score_table["click_flagged"]
            self.reward = self.score_table["click_flagged"]
            print("Clicked (reveal) on flaged tile ",row,col)
            return None
        else:
            self.score += self.score_table["click_revealed"]
            self.reward = self.score_table["click_revealed"]
            print("Clicked (reveal) on already revealed tile ",row,col)
            #print("This tile has already been revealed")
            return None

        
    

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
                        if (r != row or c != col) and self.board[r][c] == 0 and self.hidden_board[r][c] == "-":
                            revealed_tiles = self._reveal_zeroes(r, c, revealed_tiles)
                        elif (r != row or c != col) and self.board[r][c] != -1 and self.hidden_board[r][c] == "-":
                            self.hidden_board[r][c] = self.board[r][c]
                            revealed_tiles += 1
        return revealed_tiles

    def _flag(self, row, col):
        if self.hidden_board[row][col] == '-':
            self.hidden_board[row][col] = 'F'
            # Increase the score if flagged tile was a bomb
            if self.board[row][col] == -1:
                self.score += self.score_table["flag_correct"]
                self.reward = self.score_table["flag_correct"]
                print("Flagged correctly tile ",row,col)
            else:
                self.score += self.score_table["flag_incorrect"]
                self.reward = self.score_table["flag_incorrect"]
                print("Flagged incorrectly tile ",row,col)
            return True

        elif self.hidden_board[row][col] == 'F':
            self.hidden_board[row][col] = '-'
            # Decrease the score if unflagged tile was a bomb
            if self.board[row][col] == -1:
                self.score += self.score_table["unflag_bomb"]
                self.reward = self.score_table["unflag_bomb"]
                print("Unflagged bomb on tile ",row,col)
            else:
                self.score += self.score_table["unflag_empty"]
                self.reward = self.score_table["unflag_empty"]
                print("Unflagged empty tile ",row,col)

            return True

        else:
            #print("This tile has already been revealed and cannot be flagged")
            self.score += self.score_table["click_revealed"]
            self.reward = self.score_table["click_revealed"]
            print("Clicked (flag) on already revealed tile",row,col)
            return False

    def _make_move(self, action):
        row, col, move = action
        self.moves_taken.append(action)
        if move == 'R' or self.revealed_tiles == 0:
            self._reveal(row, col)
        else:
            self._flag(row, col)
        #print(self.hidden_board)
        #sleep(1)
        #return self.hidden_board, self.score, self.game_over


    def _get_state(self):
        if not self.game_over:
            float_board = self._convert(self.hidden_board.flatten())
            #return self.game_over, self.score, self.hidden_board.flatten()
        else:
            float_board = self._convert(self.board.flatten())
            #return self.game_over, self.score, self.board.flatten()
        return self.game_over, self.reward, float_board

    def _reset(self, board_size, num_bombs):
        self.board = None
        self.hidden_board = np.full((self.board_size, self.board_size), '-')
        self.revealed_tiles = 0
        self.game_over = False
        self.score = 0
        self.moves_taken = []
        float_board = self._convert(self.hidden_board.flatten())
        return float_board
    
    def _convert(self, board):
        float_board = np.zeros(81,)
        for i in range(len(board)):
            #print(board)
            try:
                float_board[i] = float(board[i])
            except:
                if board[i] == "-":
                    float_board[i] = -2
                elif board[i] == "F":
                    float_board[i] = -3
                else:
                    continue
            #print("step: ", i)
            #print(float_board)
        return float_board


def main():
    from test_game import TestMinesweeperGame
    # Creating a test suite
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite((TestMinesweeperGame)))

    # Run the test suite
    runner = unittest.TextTestRunner()
    result = runner.run(suite)


if __name__ == "__main__":
    main()

    #print("Done")
