import random
import unittest
from gameForAI import MinesweeperGame

class QLearningAgent:
    def __init__(self, board_size, bombs, actions, epsilon=0.1, alpha=0.5, gamma=0.9):
        self.board_size = board_size
        self.bombs = bombs
        self.epsilon = epsilon #Exploration rate
        self.alpha = alpha #Learning rate
        self.gamma = gamma #Discount factor
        self.actions = actions
        self.q_table = self._init_q_table()
        self.taken_actions = []

    def _init_q_table(self):
        #q_table made with dictionary comprehension
        q_table = {(i, j, action): 0 for i in range(self.board_size)
                   for j in range(self.board_size)
                   for action in self.actions}
        return q_table

    def _choose_action(self, state):
        state = tuple(state)
        #Explore with propability epsilon
        if random.random() < self.epsilon:
            #Preventing the agent from choosing the same action again
            return random.choice([a for a in self.actions if a not in self.taken_actions])
        #Otherwise, use the Q-table
        else:
            state_actions = [(state[0], state[1], a) for a in self.actions]
            q_values = [self.q_table.get(sa, 0) for sa in state_actions]
            max_q_value = max(q_values)
            # Preventing the agent from choosing the same action again
            max_actions = [a for a, q in zip(self.actions, q_values) if q == max_q_value and a not in self.taken_actions]
            if max_actions:
                action = random.choice(max_actions)
            else:
                action = random.choice([a for a in self.actions if a not in self.taken_actions])
            self.taken_actions.append(action)
            return action

    def _update_q_table(self, state, action, reward, next_state):
        #Update the Q-value for the given state-action pair with Q-Learning update rule
        sa = (state[0], state[1], action)
        max_q_next = max([self.q_table.get((next_state[0], next_state[1], a), 0) for a in self.actions])
        self.q_table[sa] += self.alpha * (reward + self.gamma * max_q_next - self.q_table[sa])

    def train_model(self, episodes):
        for i in range(episodes):
            game = MinesweeperGame(self.board_size, self.bombs)
            state = game.get_state()
            done = False
            while not done:
                action = self._choose_action(state)
                next_state, reward, done = game.step(action)
                self._update_q_table(state, action, reward, next_state)
                state = next_state

    def run_model(self, episodes):
        pass


def main():
    from test_agent import TestQLearningAgent
    #Creating a test suite
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite((TestQLearningAgent)))

    #Run the test suite
    runner = unittest.TextTestRunner()
    result = runner.run(suite)


if __name__ == "__main__":
    main()

    board_size = 9
    bombs = 10

    actions = []
    for i in range(10):
        for j in range(10):
            actions.extend([(i, j, 'R'), (i, j, 'F')])  #Append each tuple separately


    agent = QLearningAgent(board_size=board_size, bombs=bombs,actions=actions)
    agent.train_model(episodes=1)

