import random

def print_board(board_size, bombs):
    bomb_positions = set()
    while len(bomb_positions) < bombs:
        pos = (random.randint(1, board_size), random.randint(1, board_size))
        bomb_positions.add(pos)

    one_position = set()
    for bomb_pos in bomb_positions:
        row, col = bomb_pos
        for i in range(max(1, row-1), min(board_size, row + 2)):
            for j in range(max(1, col-1), min(board_size, col + 2)):
                one_position.add((i, j))

    for row in range(1, board_size + 1):
        for col in range(1, board_size + 1):
            if (row, col) in bomb_positions:
                print("B", end="\t")
            elif (row, col) in one_position:
                print("1", end="\t")
            else:
                print("0", end="\t")
        print()

board_size = 9
bombs = 10

def main():
    print_board(board_size, bombs)

if __name__ == "__main__":
    main()