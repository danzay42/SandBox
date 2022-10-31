import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
from keras import layers, utils
from keras.datasets import mnist

# задача распознования чисел
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train / 255
x_test = x_test / 255

# plt.figure(figsize=(10,5))
# for i in range(25):
#     plt.subplot(5, 5, i+1)
#     plt.xticks([])
#     plt.yticks([])
#     plt.imshow(x_train[i], cmap=plt.cm.binary)
# plt.show()

y_train_cat = utils.to_categorical(y_train, 10)
y_test_cat = utils.to_categorical(y_test, 10)

# входной слой  28*28 нейронов -
# скрытый слой  128?  нейронов Relu
# выходной слой 10    нейронов softmax (задача классификации)

model = keras.Sequential([
        layers.Flatten(input_shape=(28,28,1)),
        layers.Dense(128, activation="relu"),
        layers.Dense(10, activation="softmax")
        ])
print(model.summary())
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=['accuracy'])
model.fit(x_train, y_train_cat, batch_size=32, epochs=5, validation_split=0.2)
model.evaluate(x_test, y_test_cat)

# неверные результаты
pred = model.predict(x_test)
pred = np.argmax(pred, axis=1)
mask = pred == y_test

x_false = x_test[~mask]
p_false = pred[~mask]
for i in range(5):
    print(f"{p_false[i]=}")
    plt.imshow(x_false[i], cmap=plt.cm.binary)
    plt.show()

