import keras
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def prepare_data(dataset) -> tuple:
    xs = []
    ys = []
    scaler_x = StandardScaler()
    scaler_y = StandardScaler()

    for i in dataset:
        xs.append(dataset[i][0])
        ys.append(dataset[i][1])

    xs_scaled = scaler_x.fit_transform(xs)
    ys_scaled = scaler_y.fit_transform(ys)

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

if __name__ == '__main__':
    dataset = []
    reaction_params_train, reaction_params_test, gops_train, gops_test = prepare_data(dataset)
    model = build_model()
    EPOCHS = 100
    checkpoint_filepath = ''

    callbacks = [keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True, start_from_epoch=10), 
                 keras.callbacks.ModelCheckpoint(filepath=checkpoint_filepath, monitor='loss', save_best_only=True)]
    
    model.fit(x=reaction_params_train, y=gops_train, epochs=EPOCHS, callbacks=callbacks)
    model.save('v1.h5')

    loss, error = model.evaluate(reaction_params_test, gops_test, verbose=2)
    print("Loss = ", loss)
    print("Error = ", error)
