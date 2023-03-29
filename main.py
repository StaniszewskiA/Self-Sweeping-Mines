import random

def print_board(board_size, bombs):
    bomb_positions = set()
    while len(bomb_positions) < bombs:
        pos = (random.randint(1, board_size), random.randint(1, board_size))
        bomb_positions.add(pos)

    for row in range(1, board_size + 1):
        for col in range(1, board_size + 1):
            if (row, col) in bomb_positions:
                print("B", end="\t")
            else:
                print(" ", end="\t")
        print()

board_size = 9
bombs = 10

def main():
    print_board(board_size, bombs)

if __name__ == "__main__":
    main()