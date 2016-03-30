# -*- coding:utf-8 -*-

from keras.models import Sequential

from keras.layers import containers, AutoEncoder, Dense
from keras import models
import numpy as np

data_dim = 32

if __name__ == "__main__":

    #X_train = np.random.random((1000,  data_dim))
    #X_test = np.random.random((1000, data_dim))
    X_train = np.array([[0,0,0,1], [0,0,1,0], [0,1,0,0], [1,0,0,0]])
    X_test = np.array([[0,0,0,6], [0,0,6,0], [0,6,0,0], [6,0,0,0]])
    # input shape: (nb_samples, 32)
    encoder = containers.Sequential([Dense(2, input_dim=4,activation='tanh')])
    decoder = containers.Sequential([Dense(4, input_dim=2)])

    #output_reconstruction参数为True,则dim(input) = dim(output)
    autoencoder = AutoEncoder(encoder=encoder, decoder=decoder, output_reconstruction=True)
    model = models.Sequential()
    model.add(autoencoder)

    # 训练autoencoder
    model.compile(optimizer='sgd', loss='mse')
    model.fit(X_train, X_train, nb_epoch=10,batch_size=64,show_accuracy=True)

    # 预测输入数据的压缩表示
    autoencoder.output_reconstruction = False  # 修改属性后，模型需要重新编译
    model.compile(optimizer='sgd', loss='mse')
    representations = model.predict(X_test)
    print representations

    # the model is still trainable, although it now expects compressed representations as targets
    model.fit(X_test, representations, nb_epoch=1)

    # to keep training against the original inputs, just switch back output_reconstruction to True
    #再次训练原始输入数据
    autoencoder.output_reconstruction = True
    model.compile(optimizer='sgd', loss='mse')
    model.fit(X_train, X_train, nb_epoch=10)
