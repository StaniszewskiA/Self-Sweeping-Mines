import random
from colorama import Fore, Style

def generate_board(board_size, bombs):
    #Making an empty set of bombs
    bomb_positions = set()
    #Populating the set with bombs
    while len(bomb_positions) < bombs:
        pos = (random.randint(0, board_size-1), random.randint(0, board_size-1))
        bomb_positions.add(pos)

    #Making an empty dictionary of bombs' positions
    positions = {}
    #Populating the dictionary with indices of tiles adjecent to bombs
    for bomb_pos in bomb_positions:
        row, col = bomb_pos
        for i in range(max(0, row-1), min(board_size, row+2)):
            for j in range(max(0, col-1), min(board_size, col+2)):
                if (i,j) not in bomb_positions:
                    positions[(i,j)] = positions.get((i,j), 0) + 1

    # Create an empty 2D array to represent the board
    board = [[0 for _ in range(board_size)] for _ in range(board_size)]

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
                #We use CYAN as default color if printed number would somehow exceed our dictionary
                count = positions[pos]
                color = colors.get(count, Fore.CYAN)
                board[row][col] = f"{color}{count}{Style.RESET_ALL}"
            else: board[row][col] = '0'

    return board

board_size = 9
bombs = 10

def main():
    board = generate_board(board_size, bombs)
    for row in board:
        for item in row:
            print(item, end='\t')
        print()

if __name__ == "__main__":
    main()

