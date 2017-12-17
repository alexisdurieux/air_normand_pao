from keras.models import Sequential

from keras.layers.core import Dense
from keras.layers.recurrent import SimpleRNN, LSTM, GRU

from keras.optimizers import Adam

def mlp(nb_units, input_dim, loss='mse'):
    model = Sequential()

    model.add(Dense(nb_units, input_shape=input_dim, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal', activation='relu'))

    optimizer = Adam(lr=3e-4)
    model.compile(loss=loss, optimizer=optimizer)

    return model

def simple_rnn(nb_units, input_dim, loss='mse'):
    model = Sequential()

    model.add(SimpleRNN())
    pass

def lstm(nb_units, input_dim, loss='mse'):
    pass

def gru(nb_units, input_dim, loss='mse'):
    pass
