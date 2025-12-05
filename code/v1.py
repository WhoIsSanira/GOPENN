import numpy as np
import tensorflow as tf
import keras


dataset = []
reaction_params = []
gops = []

for i in dataset:
    reaction_params.append(dataset[i][0])
    gops.append(dataset[i][1])
    
model = keras.Sequential([
    keras.layers.InputLayer(5),
    keras.layers.Dense(100, activation='tanh'),
    keras.layers.Dense(100, activation='tanh'),
    keras.layers.Dense(100, activation='tanh'),
    keras.layers.Dense(100, activation='tanh'),
    keras.layers.Dense(10)
])

model.compile(optimizer=keras.optimizers.Adam(), loss=keras.losses.mean_squared_error())