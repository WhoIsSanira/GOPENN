import os
import numpy
import pickle
import keras
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from dataset import Dataset
from ecisreader import EcisReader


class GOPENN:
    def __init__(self, dataset: list[Dataset], path: str, model_name: str) -> None:
        self.dataset = dataset
        self.model_path = path
        self.model_name = model_name

    @property
    def model_folder(self) -> str:
        return self.model_path + '\\' + self.model_name 

    def prepare_data(self) -> tuple:
        xs = []
        ys = []
        scaler_x = StandardScaler()
        scaler_y = StandardScaler()

        for i in range(len(self.datasets)):
            xs.append(self.datasets[i].xs)
            ys.append(self.datasets[i].ys)

        xs_scaled = scaler_x.fit_transform(xs)
        ys_scaled = scaler_y.fit_transform(ys)

        xscale_file = self.model_folder + '\\' + 'xscale.pkl'
        yscale_file = self.model_folder + '\\' + 'yscale.pkl'

        with open(xscale_file, 'wb') as file:
            pickle.dump(scaler_x, file)

        with open(yscale_file, 'wb') as file:
            pickle.dump(scaler_y, file)

        return train_test_split(xs_scaled, ys_scaled, test_size=0.2, train_size=0.8)

    def build_model(self) -> keras.Sequential:
        model = keras.Sequential([
            keras.layers.Input(shape=self.dataset[0].xs.shape),
            keras.layers.Dense(100, activation='relu'),
            keras.layers.Dense(100, activation='relu'),
            keras.layers.Dense(100, activation='relu'),
            keras.layers.Dense(100, activation='relu'),
            keras.layers.Dense(self.dataset[0].ys.shape)
        ])

        model.compile(optimizer=keras.optimizers.Adam(), loss='mse', metrics=['mae'])

        return model

    def train_model(self) -> None:
        EPOCHS = 100
        reaction_params_train, reaction_params_test, gops_train, gops_test = self.prepare_data()

        model = self.build_model()
        checkpoint_filepath = self.model_folder + '\\' + self.model_name + '.keras'

        callbacks = [keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True, start_from_epoch=10), 
                    keras.callbacks.ModelCheckpoint(filepath=checkpoint_filepath, monitor='loss', save_best_only=True)]
        
        model.fit(x=reaction_params_train, y=gops_train, epochs=EPOCHS, callbacks=callbacks)

        loss, error = model.evaluate(reaction_params_test, gops_test, verbose=2)
        print("Loss = ", loss)
        print("Error = ", error)
    
    def tabulate(self) -> None:
        model_path = self.model_folder + '\\' + self.model_name + '.keras'
        model = keras.models.load_model(model_path, compile=True)
        
        with open(self.model_folder + '\\' + 'xscale.pkl', 'rb') as file:
            xscale = pickle.load(file)
    
        with open(self.model_folder + '\\' + 'yscale.pkl', 'rb') as file:
            yscale = pickle.load(file)
    
        pred_xs_raw = numpy.array([self.dataset[i].xs for i in range(len(self.dataset))])
        pred_xs_scaled = xscale.transform(pred_xs_raw)
    
        pred_ys_scaled = model.predict(pred_xs_scaled)
        pred_ys_raw = yscale.inverse_transform(pred_ys_scaled)
    
        # ZAID sorting for convenience
        pred_xs_raw = sorted(pred_xs_raw, key=lambda x: 1000 * x[0] + x[1])
    
        with open(self.model_folder + '\\output.txt', 'w') as file:
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
    pass
