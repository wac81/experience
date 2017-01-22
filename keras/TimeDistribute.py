# -*- coding:utf-8 -*-
from __future__ import print_function
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.wrappers import *
import numpy as np
import random


# as the first layer in a model
model = Sequential()
model.add(TimeDistributed(Dense(8), input_shape=(10, 3)))
# now model.output_shape == (None, 10, 8)

# subsequent layers: no need for input_shape
model.add(TimeDistributed(Dense(2)))
model.add(Activation("linear"))
# compile

model.compile(loss="mean_squared_error", optimizer="rmsprop")

#prepare dataset
X_train = np.random.random((100, 10, 3))
print ('random array:', X_train)
# y_train = \
mu,sigma = 0,1 #均值与标准差
y_train = []
y_train_temp = []
for i in range(10):
    single = np.random.choice([0,1])
    y_train_temp.append([single, 1-single])
for i in range(100):
    # single = np.random.choice([0,1])
    y_train.append(y_train_temp)

# y_train = np.random.normal(mu,sigma,10)
print ('random array:', y_train)

model.fit(X_train, y_train, nb_epoch=25000, show_accuracy=True, batch_size=1)
# now model.output_shape == (None, 10, 32)