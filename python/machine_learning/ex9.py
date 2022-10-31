import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
# import matplotlib.pyplot as plt

from keras.layers import Dense, SimpleRNN, Input, Embedding
from keras.models import Sequential
from keras.utils import to_categorical
from keras.preprocessing.text import Tokenizer

# Рекурентная нейроная сеть
text = open('text.txt', 'r', encoding="utf-8-sig").read()

max_words_count = 1000
tokenizer = Tokenizer(num_words=max_words_count, 
                      filters='!–"—#$%&amp;()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r«»',
                      lower=True, split=' ', char_level=False)
tokenizer.fit_on_texts([text])

data = tokenizer.texts_to_sequences([text])[0]
res = np.array(data)

inp_words=3
n = res.shape[0] - inp_words
X = np.array([res[i:i + inp_words] for i in range(n)])
Y = to_categorical(res[inp_words:], num_classes=max_words_count)

model = Sequential([
    Embedding(max_words_count, 256, input_length=inp_words),
    Input((inp_words, max_words_count)),
    SimpleRNN(128, activation='tanh'),
    Dense(max_words_count, activation='softmax')
    ])

print(model.summary())

model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
history = model.fit(X,Y,batch_size=32, epochs=1)

def build_phrase(texts, str_len=20):
    res = texts
    data = tokenizer.texts_to_sequences([texts])[0]
    for i in range(str_len):
        x = data[i:inp_words+i]
        inp = np.expand_dims(x, axis=0)

        pred = model.predict(inp)
        indx = pred.argmax(axis=1)[0]
        data.append(indx)
        res += " " + tokenizer.index_word[indx]
    return res

print(build_phrase("что такое жизнь"))

