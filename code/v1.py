import os
import numpy
import pickle
import keras
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from ecisreader import *


def prepare_data(dataset: list[tuple[numpy.ndarray, numpy.ndarray]]) -> tuple:
    xs = []
    ys = []
    scaler_x = StandardScaler()
    scaler_y = StandardScaler()

    for i in range(len(dataset)):
        xs.append(dataset[i][0][2:])
        ys.append(dataset[i][1])

    xs_scaled = scaler_x.fit_transform(xs)
    ys_scaled = scaler_y.fit_transform(ys)

    with open('.\\models\\v1\\xscale.pkl', 'wb') as file:
        pickle.dump(scaler_x, file)

    with open('.\\models\\v1\\yscale.pkl', 'wb') as file:
        pickle.dump(scaler_y, file)

    return train_test_split(xs_scaled, ys_scaled, test_size=0.2, train_size=0.8)


def build_model() -> keras.Sequential:
    model = keras.Sequential([
        keras.layers.Input(shape=(3,)),
        keras.layers.Dense(100, activation='relu'),
        keras.layers.Dense(100, activation='relu'),
        keras.layers.Dense(100, activation='relu'),
        keras.layers.Dense(100, activation='relu'),
        keras.layers.Dense(10)
    ])

    model.compile(optimizer=keras.optimizers.Adam(), loss='mse', metrics=['mae'])

    return model


def train_model() -> None:
    dataset = v1_dataset()
    reaction_params_train, reaction_params_test, gops_train, gops_test = prepare_data(dataset)

    model = build_model()
    EPOCHS = 100
    checkpoint_filepath = '.\\models\\v1\\v1.keras'

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

        Z, A = reader.read_target(buffer)
        Z_targ.append(Z)
        A_targ.append(A)
        ener.append(reader.read_energy(buffer))

    pred_xs_raw = numpy.array([[Z_targ[i], A_targ[i], ener[i]] for i in range(len(files))])
    
    return pred_xs_raw


def tabulate() -> None:
    model = keras.models.load_model('.\\models\\v1\\v1.keras', compile=True)
    
    with open('.\\models\\v1\\xscale.pkl', 'rb') as file:
        xscale = pickle.load(file)

    with open('.\\models\\v1\\yscale.pkl', 'rb') as file:
        yscale = pickle.load(file)

    pred_xs_raw = get_prediction_data()
    pred_xs_scaled = xscale.transform(pred_xs_raw)

    pred_ys_scaled = model.predict(pred_xs_scaled)
    pred_ys_raw = yscale.inverse_transform(pred_ys_scaled)

    # ZAID sorting for convenience
    pred_xs_raw = sorted(pred_xs_raw, key=lambda x: 1000 * x[0] + x[1])

    with open('.\\models\\v1\\output.txt', 'w') as file:
        table = 'Zt'.center(6) + 'At'.center(6) + 'Elab'.center(10)
        params = ['V real', 'r real', 'a real',
                  'W volu', 'ir volu', 'ia volu',
                  'W surf', 'ir surf', 'ia surf',
                  'r coul'
        ]

        for param in params:
            table += param.center(10)
        table += '\n'

        for i in range(len(pred_xs_raw)):
            Z, A, En = int(pred_xs_raw[i][0]), int(pred_xs_raw[i][1]), pred_xs_raw[i][2]
            table += str(Z).center(6) + str(A).center(6) + str(round(En, 1)).center(10)

            for output in pred_ys_raw[i]:
                table += str(round(output, 3)).center(10)

            table += '\n'

        file.write(table)


if __name__ == '__main__':
    tabulate()