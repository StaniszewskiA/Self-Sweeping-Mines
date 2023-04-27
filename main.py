from dqn import Agent
import numpy as np
import game
import tensorflow

tensorflow.keras.utils.disable_interactive_logging()

board_size = 9
num_bombs = 15

if __name__ == "__main__":

    actions = []
    for i in range(board_size):
        for j in range(board_size):
            actions.extend([(i, j, 'R'), (i, j, 'F')])  #Append each tuple separately
    

    """
    Input layer - 
    """
    
    env = game.MinesweeperGame(board_size, num_bombs)
    n_games = 100

    agent = Agent(gamma=0.99, epsilon=1.0, alpha=0.0005, input_dims=81,
                  n_actions=len(actions), mem_size=100000, batch_size=5, epsilon_end=0.01)
    agent.load_model('dqn_model.h5')

    scores = []
    eps_history = []

    for i in range(n_games):
        done = False
        score = 0
        observation = env._reset(board_size,num_bombs)
        while not done:
            action = agent.choose_action(observation)
            env._make_move(actions[action])
            #observation_, score_, done, info = env._make_move(action)
            done, score_, observation_ = env._get_state()
            score = score_
            agent.remember(observation, action, score_, observation_, done)
            observation = observation_
            agent.learn()

        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[max(0, i-100):(i+1)])
        print('episode', i, "score %.2f" % score,
                'average score %.2f' % avg_score)

        if i % 10 == 0 and i > 0:
            agent.save_model()
    

