import random
import numpy as np
from colorama import Fore, Style

def generate_board(board_size, bombs):
    #Making an empty set of bombs
    bomb_positions = set()
    #Populating the set with bombs
    while len(bomb_positions) < bombs:
        pos = (random.randint(0, board_size - 1), random.randint(0, board_size - 1))
        bomb_positions.add(pos)

    #Making an empty dictionary of bombs' positions
    positions = {}
    #Populating the dictionary with indices of tiles adjecent to bombs
    for bomb_pos in bomb_positions:
        row, col = bomb_pos
        for i in range(max(0, row - 1), min(board_size, row + 2)):
            for j in range(max(0, col - 1), min(board_size, col + 2)):
                if (i, j) not in bomb_positions:
                    positions[(i, j)] = positions.get((i, j), 0) + 1

    #Create an empty 2D array to represent the board
    board = [['0' for _ in range(board_size)] for _ in range(board_size)]

    colors = {
        1: Fore.BLUE,
        2: Fore.GREEN,
        3: Fore.RED,
        4: Fore.MAGENTA,
        5: Fore.BLUE,
        6: Fore.GREEN,
        7: Fore.RED,
        8: Fore.MAGENTA
    }

    for row in range(board_size):
        for col in range(board_size):
            pos = (row, col)
            if pos in bomb_positions:
                board[row][col] = 'B'
            elif pos in positions:
                count = positions[pos]
                color = colors.get(count, Fore.CYAN)
                board[row][col] = f"{color}{count}{Style.RESET_ALL}"

    return board

class MinesweeperGame:
    def __init__(self, board_size=9, bombs=10):
        self.board_size = board_size
        self.bombs = bombs
        self.board = generate_board(board_size, bombs)
        self.empty_board = [[f'({i},{j})' for j in range(board_size)] for i in range(board_size)]
        self.revealed_tiles = 0
        self.flags = set()
        self.game_over = False
        self.winner = False
        self.score = 0

    def reveal_tile(self, row, col):
        if self.empty_board[row][col] == '-1':
            if self.board[row][col] == 'B':
                self.score -= 10
                self.game_over = True
                self.revealed_tiles += 1
            elif self.board[row][col] == '0':
                #Reveal all the adjecent tiles with DFS algorithm
                self.score +=1
                self.revealed_tiles = self._reveal_zeroes(row, col, self.revealed_tiles)
            else:
                # Reveal the tile
                self.score += 1
                self.empty_board[row][col] = self.board[row][col]
                self.revealed_tiles += 1
        else:
            self.score -= 1
            print("This tile has already been revealed.")

        if self.revealed_tiles == self.board_size ** 2 - self.bombs:
            #All non-bomb tiles have been revealed
            self.score = +10
            self.winner = True

    def flag_tile(self, row, col):
        if self.empty_board[row][col] == '-1':
            self.empty_board[row][col] = 'F'
            self.flags.add((row, col))
        elif self.empty_board[row][col] == 'F':
            self.empty_board[row][col] = '-1'
            self.flags.remove((row, col))
        else:
            self.score -= 1
            print("This tile has already been revealed.")

    def _reveal_zeroes(self, row, col, revealed_tiles):
        # Revealing 0's with DFS algorithm
        if self.empty_board[row][col] == '-1':
            if self.board[row][col] != '0':
                self.empty_board[row][col] = self.board[row][col]
                revealed_tiles += 1
            else:
                self.empty_board[row][col] = '0'
                revealed_tiles += 1
                for r in range(max(0, row - 1), min(row + 2, len(self.board))):
                    for c in range(max(0, col - 1), min(col + 2, len(self.board[0]))):
                        if (r != row or c != col) and self.board[r][c] == '0':
                            revealed_tiles = self._reveal_zeroes(r, c, revealed_tiles)
                        elif (r != row or c != col) and self.board[r][c].isdigit():
                            self.empty_board[r][c] = self.board[r][c]
                            revealed_tiles += 1
        return revealed_tiles

def main():

    game = MinesweeperGame()
    board = game.board
    empty = game.empty_board
    for row in empty:
        print(' '.join(row))
    for row in board:
        print(' '.join(row))


if __name__ == '__main__':
    main()