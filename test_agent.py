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

        print(len(self.agent.q_table))
        print("test__init_q_table passed")

    def test__choose_action(self):
        #Create a mock q_table with fixed q-values
        mock_q_table = {
            (0, 0, (0, 0)): 0.5,
            (0, 0, (0, 1)): 0.2,
            (0, 0, (1, 0)): 0.8,
            (0, 0, (1, 1)): 0.1,
        }
        self.agent.q_table = mock_q_table

        #Ensure that the agent chooses the action with the highest Q-value when epsilon is 0
        state = (0,0)
        self.agent.epsilon = 0
        expected_action = (1,0)
        chosen_action = self.agent._choose_action(state)
        self.assertEqual(chosen_action, expected_action, f"Expected action {expected_action}, nut got {chosen_action}")
        print(f"Chosen action: {chosen_action}")

        #Ensure that the agent chooses a different action when called with a different state
        state = (1,0)
        #We still use epsilon equal to 0
        chosen_action2 = self.agent._choose_action(state)
        self.assertNotEqual(chosen_action, chosen_action2, f"Agent chose the same action despite having another state passed")
        print(f"Chosen action 2: {chosen_action2}")

        #Ensure that the agent chooses a random action when epsilon is 1
        state = (0,0)
        self.agent.epsilon = 1
        chosen_action_rand = self.agent._choose_action(state)
        self.assertIn(chosen_action_rand, self.agent.actions, f"Expected a random action from {self.agent.actions}, but got {chosen_action_rand}")
        print(f"Chosen random action: {chosen_action_rand}")

        print("test__chose_action passed")

    def test__update_q_table(self):
        pass

    def test_train_model(self):
        pass

    def test_run_model(self):
        pass