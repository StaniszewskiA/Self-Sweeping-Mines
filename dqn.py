import random
import unittest
from game import MinesweeperGame
from keras.layers import Dense, Activation
from keras.models import Sequential, load_model
from keras.optimizers import Adam
import numpy as np

class ReplayBuffer(object):
    def __init__(self, max_size, input_shape, n_actions, discrete=False):
        self.mem_size = max_size
        self.mem_cntr = 0
        self.discrete = discrete
        self.state_memory = np.zeroes((self.mem_size, input_shape))
        self.new_state_memory = np.zeros((self.mem_size, input_shape))
        dtype = np.int8 if self.discrete else np.float32
        self.action_memory = np.zeros((self.mem_size, n_actions), dtype=dtype)
        self.reward_memory = np.zeros(self.mem_size)
        self.terminal_memory = np.zeroes(self.mem_size, dtype=np.float32)

    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_cntr & self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.reward_memory[index] = reward
        self.terminal_memory[index] = 1 - int(done)
        if self.discrete:
            actions = np.zeroes(self.action_memory.shape[1])
            actions[action] = 1.0
            self.action_memory[index] = actions
        else:
            self.action_memory[index] = action
        self.mem_cntr += 1

    def sample_buffer(self, batch_size):
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, batch_size)

        states = self.state_memory[batch]
        states_ = self.new_state_memory[batch]
        rewards = self.reward_memory[batch]
        actions = self.action_memory[batch]
        terminal = self.terminal_memory[batch]

        return states, actions, rewards, states_, terminal

def build_dqn(lr,n_actions, input_dims, fc1_dims, fc2_dims):
    model = Sequential([
                Dense(fc1_dims, input_shape=(input_dims, )),
                Activation('relu'),
                Dense(fc2_dims),
                Activation('relu'),
                Dense(n_actions)])

    model.compile(optimizer=Adam(lr=lr), loss='mse')

    return model

"""
def build_dqn(lr, n_actions, input_dims):
    #Define the input shape
    input_layer = Input(shape=input_dims) 

    #Add three 2D convolutional layers with ReLU activation
    conv1 = Conv2D(filters=32, kernel_size=3, padding='same', activation='relu')(input_layer)
    conv1 = Conv2D(filters=64, kernel_size=3, padding='same', activation='relu')(conv1)
    conv1 = Conv2D(filters=64, kernel_size=3, padding='same', activation='relu')(conv2)

    #Flatten the output of the convolutional layers
    flatten = Flatten()(conv3)
    
    #Add 2 fully connected layers with ReLU activation
    dense1 = Dense(units=512, activation='relu')(flatten)
    dense2 = Dense(units=256, activation='relu')(dense1)

    #Add the output layer with linear activation
    output_layer = Dense(units=n_actions, activation='linear')(dense2)

    #Define the model
    model = Model(inputs=input_layer, outputs=output_layer)
    model.compile(optimizer=Adam(lr=lr), loss='mse)

    return model

"""

class Agent(object):
    def __init__(self, alpha, gamma, n_actions, epsilon, batch_size,
                input_dims, epsilon_dec=0.996, epsilon_end=0.01,
                mem_size=100000, fname='dqn_model.h5'):
        self.action = [i for i in range(n_actions)] #Tutaj trzeba będzie zmienić na nasze akcje w saperze
        self.n_actions = n_actions
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_end
        self.batch_size = batch_size
        self.model_file = fname

        self.memory = ReplayBuffer(mem_size, input_dims, n_actions,
                                    discrete=True)
        self.q_eval = build_dqn(alpha, n_actions, input_dims, 256, 256)
        self.actions_taken = set()

    def remember(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def choose_action(self, state):
        state = state[np.newaxis, :]
        rand = np.random.random()
        if rand < self.epsilon:
            action = np.random.choice([i for i in range(self.action) if i not in self.actions_taken])
        else:
            actions = self.q_eval.predict(state)
            action = np.argmax(actions)

        self.actions_taken.add(action)
        return action

    def learn(self):
        #Using Temporal Difference
        if self.memory.mem_cntr < self.batch_size:
            return
        state, action, reward, new_state, done = \
            self.memory.sample_buffer(self.batch_size)

        action_values = np.array(self.action_space, dtype=np.int8)
        action_indices = np.dot(action, action_values)

        q_eval = self.q_eval.predict(state)
        q_next = self.q_eval.predict(new_state)

        q_target = q_eval.copy()

        batch_index = np.arrange(self.batch_size, dtype=np.int32)

        q_target[batch_index, action_indices] = reward + \
                self.gamma*np.max(q_next, axis=1)*done

        _ = self.q_eval.fit(state, q_target, verbose=0)

        self.epsilon = self.epsilon*self.epsilon_dec if self.epsilon > \
                        self.epsilon_min else self.epsilon_min

    def save_model(self):
        self.q_eval.save(self.model_file)

    def load_model(self):
        self.q_eval = load_model(self.model_file)






