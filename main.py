from dqn import Agent
import numpy as np
import game
import tensorflow

tensorflow.keras.utils.disable_interactive_logging()
print(tensorflow.config.experimental.list_physical_devices('GPU'))

input()

board_size = 9
num_bombs = 20

def gen_action_list():
    actions = []
    for i in range(board_size):
        for j in range(board_size):
            actions.extend([(i, j, 'R'), (i, j, 'F')])  #Append each tuple separately

    return actions

if __name__ == "__main__":
    

    actions = gen_action_list()
    """
    Input layer - 
    """
    
    env = game.MinesweeperGame(board_size, num_bombs)
    n_games = 1000

    # gamma set to 0.0 from 0.99 for testing purposes
    agent = Agent(gamma=0.0, epsilon=1.0, alpha=0.0005, input_dims=81,
                  n_actions=len(actions), mem_size=100000, batch_size=256, epsilon_end=0.01)
    

    scores = []
    eps_history = []

    f = open("result.txt","r+")
    eps_before = f.readline()
    if eps_before == "":
        eps_before = 0
    f.close()
    
    print(eps_before)
    for i in range(n_games):
        taken_actions = []
        done = False
        score = 0
        observation = env._reset(board_size,num_bombs)
        moves_taken = 0
        while not done:
            action = agent.choose_action(observation)
            if moves_taken == 0 and action % 2 == 1:
                action -= 1
            env._make_move(actions[action])
            if action in taken_actions:
                  done = True
            moves_taken += 1
            #print("Moves taken: ", moves_taken)
            done, reward, observation_m, is_won = env._get_state()
            score += reward
            agent.remember(observation, action, reward, observation_, done)
            observation = observation_
            agent.learn()

        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[max(0, i-100):(i+1)])
        print('episode', i+int(eps_before), "score %.2f" % score,
                'average score %.2f' % avg_score, 'won:' % is_won)
        
        actions = gen_action_list()

        agent.refresh_actions()

        if i % 10 == 0 and i > 0:
            f = open("result.txt", "w+")
            f.write(str(i))
            f.close()
            agent.save_model()