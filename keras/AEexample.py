import numpy as np
np.random.seed(1337) # for reproducibility

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, AutoEncoder, Layer
from keras.optimizers import SGD, Adam, RMSprop, Adagrad, Adadelta
from keras.utils import np_utils
from keras.utils.dot_utils import Grapher
from keras.callbacks import ModelCheckpoint
from keras.layers import containers

batch_size = 10000
nb_classes = 10
nb_epoch = 1

adg = Adagrad()
sgd = SGD()
rms = RMSprop()

#the data, shuffled and split between train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
X_test = X_test.reshape(10000, 784)
X_train = X_train.astype("float64")
X_test = X_test.astype("float64")
X_train /= 255
X_test /= 255
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

#convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

#creating the autoencoder

#first autoencoder
AE1_output_reconstruction = True
ae1 = Sequential()
encoder1 = containers.Sequential([Dense(4, 2, activation='tanh')])
decoder1 = containers.Sequential([Dense(2, 4, activation='tanh')])
ae1.add(AutoEncoder(encoder=encoder1, decoder=decoder1,
output_reconstruction=AE1_output_reconstruction, tie_weights=True))

#training the first autoencoder
ae1.compile(loss='mean_squared_error', optimizer=RMSprop())
ae1.fit(X_train, X_train, batch_size=batch_size, nb_epoch=nb_epoch,
show_accuracy=False, verbose=1, validation_data=[X_test, X_test])