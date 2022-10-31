import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
from keras import layers, utils
from keras.datasets import mnist

# задача распознования чисел c алогритмом BatchNormalization
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train / 255
x_test = x_test / 255

y_train_cat = utils.to_categorical(y_train, 10)
y_test_cat = utils.to_categorical(y_test, 10)

limit = 5000
x_train_data = x_train[:limit]
y_train_data = y_train_cat[:limit]
x_valid = x_train[limit:limit*2]
y_valid = y_train_cat[limit:limit*2]

model = keras.Sequential([
        layers.Flatten(input_shape=(28,28,1)),
        layers.Dense(300, activation="relu"),
        layers.BatchNormalization(),
        layers.Dense(10, activation="softmax")
        ])
print(model.summary())
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=['accuracy'])
his = model.fit(x_train_data, y_train_data, batch_size=32, epochs=50,
                validation_data=(x_valid, y_valid))
# model.evaluate(x_test, y_test_cat)

plt.plot(his.history['loss'])
plt.plot(his.history['val_loss'])
plt.show()

