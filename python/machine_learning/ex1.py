import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# import numpy as np
# import matplotlib.pyplot as plt
import tensorflow as tf

# # Нахождение минимума функции (или когда производная функции равна 0)
# x = tf.Variable(-1.)
# # y = lambda: x**2 - x
# # N = 100
# # opt = tf.optimizers.SGD(learning_rate=0.1)
# # for n in range(N):
# #     opt.minimize(y, [x])
# print(x)

# # Функции автозаполнения
# tf_vars = [tf.eye(3), tf.zeros((3,3)), tf.ones((3,3)), tf.fill((4,2), 42)]
# # zeros_like, ones_like, identity - возвращает копию
# for v in tf_vars:
#     print(v)
# print(tf.range(1, 11, 0.2))

# # Функции случайных величин
# normal = tf.random.normal((5,), 0, 0.1)
# uniform = tf.random.uniform((5,), -1, 1)
# truncate_normal = tf.random.truncated_normal()
# # shuffle = tf.random.shuffle()
# # seed = tf.random.set_seed()
# print(normal, uniform,  sep='\n')

# # Операторы
# a = tf.constant([1,2,3])
# b = tf.constant([7,8,9])
# print(f"{a+b=}\n{tf.add(a, b)=}\n{a-b=}\n{a/b=}\n{a*b=}")
# vm = tf.tensordot(a, b, axes=0)
# mm = tf.tensordot(a, b, axes=1)
# print(f"{vm=}\n{mm=}")
# a2 = tf.constant(tf.range(1,10), shape=(3,3))
# b2 = tf.constant(tf.range(5,14), shape=(3,3))
# m1 = tf.matmul(a2, b2)
# m2 = a2 @ b2
# # tf.reduce_[max|min|mean|sum|prod|all|any|logsumexp]
# print(f"{m1=}\n{m2=}")

# Функции ML
# tf.keras.activations - функции активации 
# tf.keras.losses - критерии качества

