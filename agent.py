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
        self.actions = actions
        self.q_table = self._init_q_table()

    def _init_q_table(self):
        #q_table made with dictionary comprehension
        q_table = {((i,j), action): 0 for i in range(self.board_size)
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
            state_actions = [((state[0], state[1]), a) for a in self.actions]
            q_values = [self.q_table.get(sa, 0) for sa in state_actions]
            max_q_value = max(q_values)
            max_actions = [a for a, q in zip(self.actions, q_values) if q == max_q_value]
            return random.choice(max_actions)

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

    agent = QLearningAgent(board_size, bombs, actions)
    """
    agent.train(episodes=10000)
    agent.test(episodes=3)
    agent._init_q_table()
    """
    state = ((0,0), 'R')
    action = agent._choose_action(state)
    print(action)

if __name__ == "__main__":
    main()
