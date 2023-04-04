import random
import numpy as np
from game import MinesweeperGame


class QLearningAgent:
    def __init__(self, board_size, bombs, actions, epsilon=0.1, alpha=0.5, gamma=0.9):
        self.board_size = board_size
        self.bombs = bombs
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.q_table = self._init_q_table()
        self.actions = actions

    def _init_q_table(self):
        pass

    def _choose_action(self, state):
        pass

    def _update_q_table(self, state, action, reward, next_state):
        pass

    def train(self, episodes):
        pass

    def test(self, episodes):
        pass

def main():
    board_size = 9
    bombs = 10
    actions = [(i, j, 'R') for i in range(board_size) for j in range(board_size)] + \
              [(i, j, 'F') for i in range(board_size) for j in range(board_size)]
    agent =  QLearningAgent(board_size, bombs, actions)
    agent.train(episodes=10000)
    agent.test(episodes=3)

if __name__ == "__main__":
    main()
