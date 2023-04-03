import random
from colorama import Fore, Style
import numpy as np


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

#Define constants
BOARD_SIZE = 9
BOMBS = 10
EPSILON = 0.1 #EXPLORATION RATE
ALPHA = 0.5 #lEARNING RATE
GAMMA = 0.9 #dISCOUNT FACTOR
ACTIONS = [(i, j) for i in range(1, BOARD_SIZE+1) for j in range(1, BOARD_SIZE+1)] + ['f']

#Initialize Q-table
q_table = np.zeros((BOARD_SIZE**2, len(ACTIONS)))

def state_to_idx(state):
    return state[0]*BOARD_SIZE + state[1]

def idx_to_state(idx):
    return idx // BOARD_SIZE, idx % BOARD_SIZE

def choose_action(state, eps):
    # Choose action with epsilon-greedy policy
    if random.random() < eps:
        return random.choice(ACTIONS)
    else:
        idx = state_to_idx(state)
        q_values = q_table[idx]
        return ACTIONS[np.argmax(q_values)]

def update_q_table(state, action, reward, next_state):
    # Update Q-value of state-action pair
    idx = state_to_idx(state)
    next_idx = state_to_idx(next_state)
    q_values = q_table[idx]
    next_q_values = q_table[next_idx]
    if action == 'f':
        action_idx = len(ACTIONS) - 1
    else:
        action_idx = ACTIONS.index(action)
    q_values[action_idx] += ALPHA * (reward + GAMMA * np.max(next_q_values) - q_values[action_idx])
    q_table[idx] = q_values

def main():
    state = (0, 0)  # Starting state
    ACTIONS = []
    empty_board = [['-' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    revealed_tiles = 0
    memo = {}  # Memoization cache
    while True:
        board = generate_board(BOARD_SIZE, BOMBS)
        for row in board:
            print(" ".join(row))
        # Choose action
        action = choose_action(state, EPSILON)
        ACTIONS.append(action)
        # Perform action
        if action == 'f':
            coordY, coordX = idx_to_state(state_to_idx(state))
            if board[coordX][coordY] == 'B':
                reward = 1  # Flagged correctly
            else:
                reward = -1  # Flagged incorrectly or already flagged
            next_state = state  # Flagging doesn't change state
        else:
            coordY, coordX = action
            if board[coordX - 1][coordY - 1] == 'B':
                reward = -10  # Stepped on a bomb
                next_state = (0, 0)  # Reset to starting state
                ACTIONS = []  # Reset actions list
            else:
                revealed_tiles = reveal_zeroes(board, empty_board, coordX - 1, coordY - 1, revealed_tiles)
                next_state = (coordX - 1, coordY - 1)
                if revealed_tiles == BOARD_SIZE ** 2 - BOMBS:
                    reward = 10  # All tiles revealed
                    next_state = (0, 0)  # Reset to starting state
                    ACTIONS = []  # Reset actions list
                else:
                    reward = 0
        # Update Q-table
        update_q_table(state, action, reward, next_state)
        state = next_state

main()