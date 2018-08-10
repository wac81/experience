# -*- coding:utf-8 -*-

'''
https://kexue.fm/archives/4765
'''

from __future__ import print_function
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM

from keras.optimizers import RMSprop
import sys
sys.path.append('..')
# import mod1
from attention.attention_keras import *
import numpy as np
import random
import sys
import codecs
# path = get_file('nietzsche.txt', origin="https://s3.amazonaws.com/text-datasets/nietzsche.txt")
# text = open(path).read().lower()
from keras.models import Model
from keras.layers import *


text = codecs.open(u"唐诗三百首.txt", encoding='utf8').read()
print('corpus length:', len(text))

chars = set(text)
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 8
step = 1
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

print('Vectorization...')
X = np.zeros((len(sentences), maxlen), dtype=np.int16)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t] = char_indices[char]
    y[i, char_indices[next_chars[i]]] = 1


# build the model: 2 stacked LSTM
print('Build model...')
# model = Sequential()
S_inputs = Input(shape=(None, ), dtype='int16')
embeddings = Embedding(len(chars), maxlen)(S_inputs)
# model.add(LSTM(1024, return_sequences=True, input_shape=(maxlen, len(chars))))
lstm = LSTM(1024, return_sequences=True)(embeddings)
O_seq = Attention(8, 16)([lstm, embeddings, embeddings])
O_seq = Dropout(0.2)(lstm)
O_seq = LSTM(1024, return_sequences=False)(O_seq)
O_seq = Dense(len(chars))(O_seq)
outputs = Activation('softmax')(O_seq)
# model.add(Dropout(0.2))
# model.add(LSTM(1024, return_sequences=False))
# model.add(Dropout(0.2))
# model.add(Dense(len(chars)))
# model.add(Activation('softmax'))
model = Model(inputs=S_inputs, outputs=outputs)
optimizer = RMSprop(lr=0.01)

model.compile(loss='categorical_crossentropy', optimizer=optimizer)


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# train the model, output generated text after each iteration
for iteration in range(1, 100):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(X, y, batch_size=32, nb_epoch=1)

    start_index = random.randint(0, len(text) - maxlen - 1)

    for diversity in [0.2, 0.5, 0.8, 1.0, 1.2]:
        print()
        print('----- diversity:', diversity)

        generated = ''
        sentence = text[start_index: start_index + maxlen]
        generated += sentence
        print('----- Generating with seed: "' + sentence + '"')
        sys.stdout.write(generated)

        for i in range(100):
            x = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x[0, t, char_indices[char]] = 1.

            preds = model.predict(x[0], verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char

            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()
