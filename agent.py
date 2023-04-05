import random
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
        self.taken_actions = []

    def _init_q_table(self):
        #q_table made with dictionary comprehension
        q_table = {(i, j, action): 0 for i in range(self.board_size)
                   for j in range(self.board_size)
                   for action in self.actions}
        return q_table

    def _choose_action(self, state):
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

    def _update_q_table(self, state, action, reward, next_state, done):
        #Get the current Q-value for the state-action pair
        q_value = self.q_table.get((state[0], state[1], action), 0)

        #Calculate the maximum Q-value for the next state
        next_state_actions = [(next_state[0], next_state[1], action) for a in self.actions]
        next_state_q_values = [self.q_table.get(nsa, 0) for nsa in next_state_actions]
        max_next_state_q_value = max(next_state_q_values)

        #Update the Q-value for the state-action pair using Q-learning update rule
        new_q_value = q_value + self.alpha * (reward + self.gamma * max_next_state_q_value - q_value)
        self.q_table[(state[0], state[1], action)] = new_q_value

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
