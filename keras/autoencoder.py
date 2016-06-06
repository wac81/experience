# -*- coding:utf-8 -*-

from keras.models import Sequential

from keras.layers import containers, AutoEncoder, Dense
from keras import models
import numpy as np

data_dim = 32

if __name__ == "__main__":

    #X_train = np.random.random((1000,  data_dim))
    #X_test = np.random.random((1000, data_dim))
    # X_train = np.array([[1,0,0,0], [0,1,0,0],[0,0,1,0], [0,0,0,1]])
    # X_test = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]])

    X_train = np.array([[1,0,0,0,0,0], [0,1,0,0,0,0],[0,0,1,0,0,0], [0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]])
    X_test = np.array([[1,0,0,0,0,0], [0,1,0,0,0,0],[0,0,1,0,0,0], [0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]])
    # X_train = X_train.astype("float32")
    # X_test = X_test.astype("float32")
    # input shape: (nb_samples, 32)
    encoder = containers.Sequential([Dense(4, input_dim=6),Dense(2, input_dim=4, activation='sigmoid')])

    decoder = containers.Sequential([Dense(4, input_dim=2),Dense(6, input_dim=4, activation='sigmoid')])

    #output_reconstruction参数为True,则dim(input) = dim(output)
    autoencoder = AutoEncoder(encoder=encoder, decoder=decoder, output_reconstruction=True)
    # print autoencoder.get_output()1
    model = models.Sequential()
    model.add(autoencoder)

    # 训练autoencoder
    model.compile(optimizer='sgd', loss='mse')

    model.fit(X_train, X_train, nb_epoch=25000, show_accuracy=True, batch_size=1)
    # model.fit(X_train, X_train, nb_epoch=10)

    representations = model.predict(X_train)
    print representations


    # predicting compressed representations of inputs:
    autoencoder.output_reconstruction = False  # the model has to be recompiled after modifying this property
    model.compile(optimizer='sgd', loss='mse')
    representations = model.predict(X_test)
    print representations
    #
    # # 预测输入数据的压缩表示
    # autoencoder.output_reconstruction = False  # 修改属性后，模型需要重新编译
    # model.compile(optimizer='sgd', loss='mse')
    # representations = model.predict(X_test)
    # print representations
    #
    # # the model is still trainable, although it now expects compressed representations as targets
    # model.fit(X_test, representations, nb_epoch=20)
    #
    # # to keep training against the original inputs, just switch back output_reconstruction to True
    # #再次训练原始输入数据
    # autoencoder.output_reconstruction = True
    # model.compile(optimizer='sgd', loss='mse')
    # representations = model.predict(X_test)
    # print representations
    # model.fit(X_train, X_train, nb_epoch=10)
