import argparse

import numpy as np
import pandas as pd
from keras.layers.core import Dense
from keras.models import Sequential
from keras.layers.recurrent import SimpleRNN
from keras.callbacks import ModelCheckpoint, EarlyStopping
import matplotlib.pyplot as plt

def mlp(input_shape, loss='mse', optimizer='adam'):
    model = Sequential()

    model.add(Dense(32, input_dim=input_shape, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss=loss, optimizer=optimizer)
    return model

def rnn(input_shape, loss='mse'):
    model = Sequential()

    model.add(SimpleRNN(32, input_shape=input_shape))

def from_dataframe_to_xy(df):
    return (np.array(df[['NO2_61FD', 'NO2_61F0', 'NO2_61EF', 'temp', 'rh', 't_grad', 'pressure', 'pluvio']]),
            np.array(df['ref']))


def split_dataframe(dataframe, percent):
    nb_rows = int(np.floor(percent * len(dataframe)))
    return dataframe[:nb_rows], dataframe[nb_rows:]


def get_generic_model(model, input_shape):
    if model == "mlp":
        return mlp(input_shape[1])
    if model == "rnn":
        return rnn(input_shape[1:])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="choose a model to train (mlp, rnn, lstm, gru)", type=str)
    parser.add_argument("input_data", help="pickle to use for training", type=str)
    parser.add_argument("-o", "--output",
                        help="if specified will monitor the training to store the weights of the network",
                        default="model.h5", type=str)
    parser.add_argument("-v", "--verbose",
                        help="increase the verbose")
    parser.add_argument("-p", "--plot",
                        help="plot the predictions versus the test", action="store_true")

    args = parser.parse_args()

    df = pd.read_pickle(args.input_data)

    df_train, df_test = split_dataframe(df, 0.5)
    df_valid, df_test = split_dataframe(df_test, 0.5)

    X_train, y_train = from_dataframe_to_xy(df_train)
    X_valid, y_valid = from_dataframe_to_xy(df_valid)
    X_test, y_test = from_dataframe_to_xy(df_test)

    model = get_generic_model(args.model, X_train.shape)
    model.summary()

    callbacks_list = []
    early_stopping = EarlyStopping('val_loss', patience=10)
    callbacks_list.append(early_stopping)
    if args.output:
        model_checkpoint = ModelCheckpoint(args.output)
        callbacks_list.append(model_checkpoint)

    model.fit(X_train, y_train, epochs=1000, validation_data=(X_valid, y_valid),
              callbacks=callbacks_list, verbose=args.verbose)

    score = model.evaluate(X_test, y_test)
    print("\n\n\t - RMSE = {}".format(np.sqrt(score)))

    if args.plot:
        y_pred = model.predict(X_test)

        plt.plot(y_pred, y_test, '+')
        plt.show()


if __name__ == '__main__':
    main()
