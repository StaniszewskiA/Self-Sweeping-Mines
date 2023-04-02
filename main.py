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

board_size = 9
bombs = 10

def reveal_zeroes(board, empty_board, row, col, revealed_tiles):
    #Revealing 0's with DFS algorithm
    if empty_board[row][col] == '-':
        if board[row][col] != '0':
            empty_board[row][col] = board[row][col]
            revealed_tiles += 1
        else:
            empty_board[row][col] = '0'
            revealed_tiles += 1
            for r in range(max(0, row-1), min(row+2, len(board))):
                for c in range(max(0, col-1), min(col+2, len(board[0]))):
                    if (r != row or c != col) and board[r][c] == '0':
                        revealed_tiles = reveal_zeroes(board, empty_board, r, c, revealed_tiles)
                    elif (r != row or c != col) and board[r][c].isdigit():
                        empty_board[r][c] = board[r][c]
                        revealed_tiles += 1
    return revealed_tiles

def reveal_numbers(board, empty_board, row, col):
    if empty_board[row][col] == '-':
        if board[row][col] == '0':
            reveal_zeroes(board, empty_board, row, col)
        elif board[row][col] != 'B':
            empty_board[row][col] = board[row][col]

def main():
    board_size = 9
    bombs = 10
    board = generate_board(board_size, bombs)
    #Creating an empty board_size x board_size 2D array for player
    empty_board = [['-' for _ in range(board_size)] for _ in range(board_size)]
    revealed_tiles = 0

    while True:
        #Print the empty board for the player
        for row in empty_board:
            print(" ".join(row))
        try:
            coordY, coordX = map(int, input("Choose coordinates (separated by a space): ").split())
            if coordX == 0 or coordY == 0:
                print("Invalid input. Please choose coordinates within board size.")
                continue
            if board[coordX - 1][coordY - 1] == "B":
                print("Game over!")
                #Reveal the entire board
                for row in board:
                    print(" ".join(row))
                break
            elif board[coordX - 1][coordY - 1] == "0":
                print("Go on!")
                revealed_tiles = reveal_zeroes(board, empty_board, coordX - 1, coordY - 1, revealed_tiles)
            else:
                print("Go on!")
                empty_board[coordX - 1][coordY - 1] = board[coordX - 1][coordY - 1]
                revealed_tiles += 1
            if revealed_tiles == board_size**2 - bombs:
                print("Congratulations! You won!")
                # reveal the entire board
                for row in board:
                    print(" ".join(row))
                break
        except ValueError:
            print("Invalid input. Please enter two integers separated by a space.")
        except IndexError:
            print("Invalid input. Please choose coordinates within the board size.")

if __name__ == "__main__":
    main()
