import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
from keras.layers import Flatten, Dense, Reshape, Input, Lambda, BatchNormalization, Dropout
from keras.models import Model
from keras.datasets import mnist
import keras.backend as K


# Вариационный автоэнкодер (VAE)


(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train / 255
x_test = x_test / 255
x_train = tf.reshape(tf.cast(x_train, tf.float32), [-1, 28*28])
x_test = tf.reshape(tf.cast(x_test, tf.float32), [-1, 28*28])

hidden_dim = 2
batch_size = 60 # должно быть кратно 60 000 (размер входных данных)

def noiser(args):
  l_mean, l_log_var = args
  N = K.random_normal(shape=(batch_size, hidden_dim), mean=0., stddev=1.0)
  return K.exp(l_log_var / 2) * N + l_mean

# VAE
## encoder
le_in = Input((28, 28, 1))
le = Flatten()(le_in)
le = Dense(256, activation='relu')(le)
le = BatchNormalization()(le)
le = Dropout(0.3)(le)
le = Dense(128, activation='relu')(le)
le = BatchNormalization()(le)
le_out = Dropout(0.3)(le)
##
lh_in = Input(128)
lh_mean = Dense(hidden_dim)(lh_in)
lh_log_var = Dense(hidden_dim)(lh_in)
lh_out = Lambda(noiser, output_shape=(hidden_dim,))([
  lh_mean,
  lh_log_var
])
## decoder
ld_in = Input(hidden_dim)
ld = Dense(128, activation='relu')(ld_in)
ld = BatchNormalization()(ld)
ld = Dropout(0.3)(ld)
ld = Dense(256, activation='relu')(ld)
ld = BatchNormalization()(ld)
ld = Dropout(0.3)(ld)
ld = Dense(28*28, activation='sigmoid')(ld)
ld_out = Reshape((28, 28, 1))(ld)

encoder = Model(le_in, le_out, name='encoder')
hidden  = Model(lh_in, lh_out, name='hidden')
decoder = Model(ld_in, ld_out, name='decoder')
vae = Model(le_in, decoder(hidden(encoder(le_in))), name="vae")
print(encoder.summary())
print(hidden.summary())
print(decoder.summary())
print(vae.summary())


def vae_loss(x, y):
  x = K.reshape(x, shape=(batch_size, 28*28))
  y = K.reshape(y, shape=(batch_size, 28*28))
  loss = K.sum(K.square(x-y), axis=-1)
  kl_loss = -0.5 * K.sum(1 + lh_log_var - K.square(lh_mean) - K.exp(lh_log_var), axis=-1)
  return loss + kl_loss

vae.compile(optimizer='adam', loss=vae_loss)

vae.fit(x_train, x_train, epochs=5, batch_size=batch_size, shuffle=True)


lh_out = encoder.predict(x_test[:6000], batch_size=batch_size)
plt.scatter(lh_out[:, 0], lh_out[:, 1])
n = 5
total = 2*n+1
plt.figure(figsize=(total, total))
num = 1
for i in range(-n, n+1):
  for j in range(-n, n+1):
    ax = plt.subplot(total, total, num)
    num += 1
    img = decoder.predict(np.expand_dims([3*i/n, 3*j/n], axis=0))
    plt.imshow(img.squeeze(), cmap='gray')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
