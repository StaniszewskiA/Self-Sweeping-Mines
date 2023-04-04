import random
import numpy as np

import test_agent
from game import MinesweeperGame
import unittest


class QLearningAgent:
    def __init__(self, board_size, bombs, actions, epsilon=0.1, alpha=0.5, gamma=0.9):
        self.board_size = board_size
        self.bombs = bombs
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions
        self.q_table = self._init_q_table()

    def _init_q_table(self):
        #q_table made with dictionary comprehension
        q_table = {(i, j, action): 0 for i in range(self.board_size)
                   for j in range(self.board_size)
                   for action in self.actions}
        print(len(q_table))
        return q_table

    def _choose_action(self, state):
        #Explore with propability epsilon
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        #Otherwise, use the Q-table
        else:
            state_actions = [(state[0], state[1], a) for a in self.actions]
            q_values = [self.q_table.get(sa, 0) for sa in state_actions]
            max_q_value = max(q_values)
            max_actions = [a for a, q in zip(self.actions, q_values) if q == max_q_value]
            return random.choice(max_actions)

    def _update_q_table(self, state, action, reward, next_state, done):
        pass

    def train_model(self, episodes):
        pass

    def run_model(self, episodes):
        pass


def main():
    from test_agent import TestQLearningAgent
    #Creating a test suite
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite((TestQLearningAgent)))

    #Run the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    main()
