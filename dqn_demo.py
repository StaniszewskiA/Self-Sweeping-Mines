from keras.layers import Dense, Activation, InputLayer
from keras.models import Sequential, load_model
from keras.optimizers import Adam
import numpy as np


def make_model():
    model = Sequential()
    model.add(InputLayer(shape=(3,))) #Input tensor
    model.add(Dense(units = 9)) #Hidden layer 1
    model.add(Dense(units = 9)) #Hidden layer 2
    model.add(Dense(units = 11)) #Hidden layer 3
    model.add(Dense(units = 1)) #Output layer
    model.summary(100)

if __name__ == "__main__":
    make_model()
