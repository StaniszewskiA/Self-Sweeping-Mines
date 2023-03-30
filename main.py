import random
from colorama import Fore, Back, Style

def print_board(board_size, bombs):
    #Making an empty set of bombs
    bomb_positions = set()
    #Populating the set with bombs
    while len(bomb_positions) < bombs:
        pos = (random.randint(1, board_size), random.randint(1, board_size))
        bomb_positions.add(pos)

    #Making an empty dictionary of bombs' positions
    positions = {}
    #Populating the dictionary with indices of tiles adjecent to bombs
    for bomb_pos in bomb_positions:
        row, col = bomb_pos
        for i in range(max(1, row-1), min(board_size, row+2)):
            for j in range(max(1, col-1), min(board_size, col+2)):
                if (i,j) not in bomb_positions:
                    positions[(i,j)] = positions.get((i,j), 0) + 1

    for row in range(1, board_size + 1):
        for col in range(1, board_size + 1):
            pos = (row, col)
            if pos in bomb_positions:
                print("B", end="\t")
            elif pos in positions:
                count = positions[pos]
                if count == 1:
                    print(Fore.BLUE + "1", end="\t" + Style.RESET_ALL)
                elif count == 2:
                    print(Fore.GREEN + "2", end="\t" + Style.RESET_ALL)
                elif count == 3:
                    print(Fore.RED + "3", end="\t" + Style.RESET_ALL)
                elif count == 4:
                    print(Fore.MAGENTA + "4", end="\t" + Style.RESET_ALL)
            else:
                print("0", end='\t')
        print()

board_size = 9
bombs = 10

def main():
    print_board(board_size, bombs)

if __name__ == "__main__":
    main()