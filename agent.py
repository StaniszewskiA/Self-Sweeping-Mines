import random
from game import MinesweeperGame, actions

class QLearningAgent:
    def __init__(self, board_size, bombs, epsilon=0.1, alpha=0.5, gamma=0.9):
        self.board_size = board_size
        self.bombs = bombs
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.q_table = self._init_q_table()

    def _init_q_table(self):
        q_table = {}
        for i in range(self.board_size):
            for j in range(self.board_size):
                q_table[(i,j)] = {'R': 0, 'F': 0}
        return q_table

    def _choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            # Select a random action
            action = random.choice(actions[state])
        else:
            # Select the best actions based on Q values:
            q_values = self.q_table[str(state)]  # convert state to a string
            max_q_value = max(q_values.values())
            # In case of multiple max values, choose randomly
            max_actions = [a for a, q in q_values.items() if q == max_q_value]
            action = random.choice(max_actions)
        return action

    def _update_q_table(self, state, action, reward, next_state):
        old_q_value = self.q_table[state][action]
        next_q_values = self.q_table[next_state]
        next_max_q_value = max(next_q_values())
        new_q_value = (1 - self.alpha) * old_q_value + self.alpha * (reward + self.gamma * next_max_q_value)
        self.q_table[state][action] = new_q_value

    def train(self, episodes):
        for episode in range(episodes):
            #Reset the game
            game = MinesweeperGame(self.board_size, self.bombs)
            state = game.empty_board
            done = False

            while not done:
                #Choose an action
                action = self._choose_action(str(state))

                #Execute the action
                row, col, act = action
                if act == 'R':
                    game.reveal_tile(row, col)
                elif act == 'F':
                    game.flag_tile(row, col)

                next_state = game.empty_board
                reward = game.score

                #Update Q table
                self._update_q_table(str(state), action, reward, str(next_state))

                state = next_state

                #Check if the game is over
                done = game.game_over or game.winner

            print(f"Episode {episode + 1}: Score = {game.score}")

    def test(self, episodes):
        win_count = 0
        loss_count = 0
        for episode in range(episodes):
            #Reset the game
            game = MinesweeperGame(self.board_size, self.bombs)
            state = game.empty_board
            done = False

            while not done:
                #Choose an action
                q_values = self.q_table[str(state)]
                max_q_value = max(q_values.values())
                #In case of multiple max values, choose one randomly
                max_actions = [a for a, q in q_values.items() if q == max_q_value]
                action = random.choice(max_actions)

                # Execute the action
                row, col, act = action
                if act == 'R':
                    game.reveal_tile(row, col)
                elif act == 'F':
                    game.flag_tile(row, col)

                state = game.empty_board

                done = game.game_over or game.winner

            if game.winner:
                print(f"Episode {episode + 1}: WIN")
                win_count += 1
            else:
                print(f"Episode {episode + 1}: LOSS")
                loss_count += 1

def main():
    agent =  QLearningAgent(board_size=8, bombs=10)
    agent.train(episodes=10000)
    agent.test(episodes=3)

if __name__ == "__main__":
    main()
