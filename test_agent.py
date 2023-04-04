from unittest import TestCase
from game import MinesweeperGame
from agent import QLearningAgent

class TestQLearningAgent(TestCase):
    def setUp(self):
        self.agent = QLearningAgent(board_size=3, bombs=3, actions=[(0, 0), (0, 1), (1, 0), (1, 1)])
    def test__init_q_table(self):
        # Create a Q-learning agent
        board_size = 3
        bombs = 3
        actions = ['open', 'flag']
        agent = QLearningAgent(board_size, bombs, actions)

        # Verify the Q-table has the expected dimensions and values
        expected_q_table_size = board_size * board_size * len(actions)
        self.assertEqual(len(agent.q_table), expected_q_table_size)
        self.assertDictEqual(agent.q_table, {(i, j, action): 0 for i in range(board_size)
                                             for j in range(board_size)
                                             for action in actions})

    def test__choose_action(self):
        # Test with high epsilon, should choose random action
        self.agent.epsilon = 0.9
        state = (0, 0)
        action = self.agent._choose_action(state)
        self.assertIn(action, self.agent.actions)

        # Test with low epsilon, should choose best action
        self.agent.epsilon = 0.1
        state = (0, 0)
        # Set the Q-values for actions in the current state to test
        self.agent.q_table[(0, 0, (0, 0))] = 1
        self.agent.q_table[(0, 0, (0, 1))] = 2
        self.agent.q_table[(0, 0, (1, 0))] = 3
        self.agent.q_table[(0, 0, (1, 1))] = 2.5
        action = self.agent._choose_action(state)
        self.assertEqual(action, (1, 0))

        # Test when multiple actions have the same Q-value
        self.agent.epsilon = 0.0
        state = (1, 1)
        self.agent.q_table[(1, 1, (0, 0))] = 1
        self.agent.q_table[(1, 1, (0, 1))] = 2
        self.agent.q_table[(1, 1, (1, 0))] = 2
        self.agent.q_table[(1, 1, (1, 1))] = 1
        action = self.agent._choose_action(state)
        self.assertIn(action, [(0, 1), (1, 0)])

        #Set a fix Q-value

    def test__update_q_table(self):
        pass

    def test_train_model(self):
        pass

    def test_run_model(self):
        pass