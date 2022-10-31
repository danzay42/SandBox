import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import re
import numpy as np
# import matplotlib.pyplot as plt

from keras.layers import Dense, LSTM, Embedding
from keras.models import Sequential
from keras.optimizers import Adam
from keras.utils import pad_sequences, to_categorical
from keras.preprocessing.text import Tokenizer

# Сеть с долгосрочной краткосрочной памятью (LSTM), не работает
texts_true = open('./train_data_true.txt', 'r', encoding='utf-8').readlines()
texts_false = open('./train_data_false.txt', 'r', encoding='utf-8').readlines()

texts = texts_true + texts_false
count_true = len(texts_true)
count_false = len(texts_false)
count_total = count_true + count_false

max_words_count = 1000
tokenizer = Tokenizer(num_words=max_words_count, filters='!–"—#$%&amp;()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r«»', lower=True, split=' ', char_level=False)
tokenizer.fit_on_texts(texts)

max_text_len = 10
data = tokenizer.texts_to_sequences(texts)
data_pad = pad_sequences(data, maxlen=max_text_len)

X = data_pad
Y = np.array([[1,0]]*count_true+[[0,1]]*count_false)

indeces = np.random.choice(X.shape[0], size=X.shape[0], replace=False)
X = X[indeces]
Y = Y[indeces]

model = Sequential([
    Embedding(max_words_count, 128, input_length=max_text_len),
    LSTM(128, return_sequences=True),
    LSTM(64),
    Dense(2, activation='softmax')
    ])

model.compile(loss="categorical_crossentropy", optimizer=Adam(0.0001), metrics=['accuracy'])
history = model.fit(X,Y,batch_size=32, epochs=50)

reverse_word_map = dict(map(reversed, tokenizer.word_index.items()))
def sequence_to_text(list_of_indices):
    return [reverse_word_map.get(letter) for letter in list_of_indices]

data = tokenizer.texts_to_sequences(["Думайте позитивно"])
data_pad = pad_sequences(data, maxlen=max_text_len)
words = sequence_to_text(data[0])
print(words)

res = model.predict(data_pad)
print(f"{res=}", np.argmax(res), sep='\n')
