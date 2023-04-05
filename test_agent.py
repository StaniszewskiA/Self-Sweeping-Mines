from unittest import TestCase
from agent import QLearningAgent

class TestQLearningAgent(TestCase):
    def setUp(self):
        self.agent = QLearningAgent(board_size=3, bombs=3, actions=[(0, 0), (0, 1), (1, 0), (1, 1)])
    def test__init_q_table(self):
        #Ensure that the q_table has the correct length
        expected_len = self.agent.board_size**2 * len(self.agent.actions)
        self.assertEqual(len(self.agent.q_table), expected_len, f"Expected {expected_len}, but got {len(self.agent.q_table)}")

        #Ensure that all q-values are initialized to 0
        for q_value in self.agent.q_table.values():
            self.assertEqual(q_value, 0)

        print("test__init_q_table passed")

    def test__choose_action(self):
        #Create a mock q_table with fixed q-values
        self.agent.q_table = {
            (0, 0, (0, 0)): 0.5,
            (0, 0, (0, 1)): 0.2,
            (0, 0, (1, 0)): 0.8,
            (0, 0, (1, 1)): 0.1,
        }

        #Ensure that the agent chooses the action with the highest Q-value when epsilon is 0
        state = (0,0)
        self.agent.epsilon = 0
        expected_action = (1,0)
        chosen_action = self.agent._choose_action(state)
        self.assertEqual(chosen_action, expected_action, f"Expected action {expected_action}, nut got {chosen_action}")

        #Ensure that the agent chooses a different action when called with a different state
        state = (1,0)
        #We still use epsilon equal to 0
        chosen_action2 = self.agent._choose_action(state)
        self.assertNotEqual(chosen_action, chosen_action2, f"Agent chose the same action despite having another state passed")

        #Ensure that the agent chooses a random action when epsilon is 1
        state = (0,0)
        self.agent.epsilon = 1
        chosen_action_rand = self.agent._choose_action(state)
        self.assertIn(chosen_action_rand, self.agent.actions, f"Expected a random action from {self.agent.actions}, but got {chosen_action_rand}")

        print("test__chose_action passed")

    def test__update_q_table(self):
        #Test the update of a single Q-value
        state = (0,0)
        action = (0,0)
        reward = 1
        next_state = (1,0)
        self.agent._update_q_table(state, action, reward, next_state)
        expected_q_value = self.agent.alpha * (reward + self.agent.gamma * 0 - 0)
        self.assertEqual(self.agent.q_table[(0, 0, (0,0))], expected_q_value)

        #Test the update of multiple Q-values
        self.agent.q_table = {
            (0, 0, (0, 0)): 0.5,
            (0, 0, (0, 1)): 0.2,
            (0, 0, (1, 0)): 0.8,
            (0, 0, (1, 1)): 0.1,
        }
        state = (0,0)
        action = (0,0)
        reward = 1
        next_state = (1,0)
        self.agent._update_q_table(state, action, reward, next_state)

        expected_q_values = {
            (0, 0, (0, 0)): 0.75,
            (0, 0, (0, 1)): 0.2,
            (0, 0, (1, 0)): 0.8,
            (0, 0, (1, 1)): 0.1,
        }

        #sa stands for station-action pair
        for sa, expected_q_value in expected_q_values.items():
            #assertAlmostEqual is a method of unittest.TestCase that checks if float values are equal up to x (5 in this case) decimal places
            self.assertAlmostEqual(self.agent.q_table[sa], expected_q_value, places=5)

        print("test__update_q_table passed")

    def test_train_model(self):
        pass

    def test_run_model(self):
        pass