import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
from keras import layers, activations

# celsius to fahrenheit y = x*1.8+32
c = np.array([-40, -10, 0, 8, 15, 22, 38])
f = np.array([-40, 14, 32, 46, 59, 72, 100])

model = keras.Sequential()
model.add(layers.Dense(units=1, input_shape=(1,), activation="linear"))
model.compile(loss="mean_squared_error", optimizer=tf.optimizers.Adam(0.1))

history = model.fit(c, f, epochs=500, verbose=0)

plt.plot(history.history['loss'])
plt.grid(True)
plt.show()

print(model.get_weights())
