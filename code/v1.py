import os
import numpy
import pickle
import keras
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from ecisreader import *


def prepare_data(dataset) -> tuple:
    xs = []
    ys = []
    scaler_x = StandardScaler()
    scaler_y = StandardScaler()

    for i in range(len(dataset)):
        xs.append(dataset[i][0])
        ys.append(dataset[i][1])

    xs_scaled = scaler_x.fit_transform(xs)
    ys_scaled = scaler_y.fit_transform(ys)

    with open('.\\models\\xscale.pkl', 'wb') as file:
        pickle.dump(scaler_x, file)

    with open('.\\models\\yscale.pkl', 'wb') as file:
        pickle.dump(scaler_y, file)

    xs_train, xs_test, ys_train, ys_test = train_test_split(xs_scaled, ys_scaled, test_size=0.2, train_size=0.8)
    prepared_data = xs_train, xs_test, ys_train, ys_test

    return prepared_data


def build_model():
    model = keras.Sequential([
        keras.layers.Input(shape=(5,)),
        keras.layers.Dense(100, activation='relu'),
        keras.layers.Dense(100, activation='relu'),
        keras.layers.Dense(100, activation='relu'),
        keras.layers.Dense(100, activation='relu'),
        keras.layers.Dense(10)
    ])

    model.compile(optimizer=keras.optimizers.Adam(), loss='mse', metrics=['mae'])

    return model


def train_model():
    dataset = lithium7_dataset()
    reaction_params_train, reaction_params_test, gops_train, gops_test = prepare_data(dataset)

    model = build_model()
    EPOCHS = 100
    checkpoint_filepath = '.\\models\\v1.keras'

    callbacks = [keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True, start_from_epoch=10), 
                 keras.callbacks.ModelCheckpoint(filepath=checkpoint_filepath, monitor='loss', save_best_only=True)]
    
    model.fit(x=reaction_params_train, y=gops_train, epochs=EPOCHS, callbacks=callbacks)

    loss, error = model.evaluate(reaction_params_test, gops_test, verbose=2)
    print("Loss = ", loss)
    print("Error = ", error)


def get_prediction_data():
    directory = '.\\ecis\\v1\\in\\'
    files = os.listdir(directory)
    files = [directory + files[i] for i in range(len(files))]

    Z_targ = []
    A_targ = []
    ener = []
    reader = EcisReader()
    

    for i in range(len(files)):
        with open(files[i], 'r') as txt:
            buffer = txt.read().split('\n')
    
        Z_targ.append(reader.read_target(buffer)[0])
        A_targ.append(reader.read_target(buffer)[1])
        ener.append(reader.read_energy(buffer))

    pred_xs_raw = numpy.array([[Z_targ[i], A_targ[i], 3.0, 7.0, ener[i]] for i in range(len(files))])
    
    
    return pred_xs_raw
    

if __name__ == '__main__':
    model = keras.models.load_model('.\\models\\v1.keras', compile=True)
    
    with open('.\\models\\xscale.pkl', 'rb') as file:
        xscale = pickle.load(file)

    with open('.\\models\\yscale.pkl', 'rb') as file:
        yscale = pickle.load(file)

    pred_xs_raw = get_prediction_data()
    pred_xs_scaled = xscale.transform(pred_xs_raw)

    pred_ys_scaled = model.predict(pred_xs_scaled)
    pred_ys_raw = yscale.inverse_transform(pred_ys_scaled)

    print(pred_ys_raw)