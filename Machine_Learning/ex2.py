import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf

# # Простейший пример
# x = tf.Variable(-2.)
# with tf.GradientTape() as tape:
#     y = x ** 2
# df = tape.gradient(y, x)
# print(df)


# Пример посложнее
w = tf.Variable(tf.random.normal((3,2)))
b = tf.Variable(tf.zeros(2, dtype=tf.float32))
x = tf.Variable([[-2., 1., 3.]])
with tf.GradientTape() as tape:
    y = x @ w + b
    loss = tf.reduce_mean(y ** 2)
df = tape.gradient(loss, [w, b])
print(f"w={df[0]}\nb={df[1]}")

