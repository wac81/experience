# -*- coding:utf-8 -*-
'''This script goes along the blog post
"Building powerful image classification models using very little data"
from blog.keras.io.
It uses data that can be downloaded at:
https://www.kaggle.com/c/dogs-vs-cats/data
In our setup, we:
- created a data/ folder
- created train/ and validation/ subfolders inside data/
- created cats/ and dogs/ subfolders inside train/ and validation/
- put the cat pictures index 0-999 in data/train/cats
- put the cat pictures index 1000-1400 in data/validation/cats
- put the dogs pictures index 12500-13499 in data/train/dogs
- put the dog pictures index 13500-13900 in data/validation/dogs
So that we have 1000 training examples for each class, and 400 validation examples for each class.
In summary, this is our directory structure:
```
data/
    train/
        dogs/
            dog001.jpg
            dog002.jpg
            ...
        cats/
            cat001.jpg
            cat002.jpg
            ...
    validation/
        dogs/
            dog001.jpg
            dog002.jpg
            ...
        cats/
            cat001.jpg
            cat002.jpg
            ...
```
'''

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential,Model
from keras.layers import Convolution2D, MaxPooling2D,AveragePooling2D,ZeroPadding2D
from keras.layers import Activation, Dropout, Flatten, Dense, advanced_activations
from keras import optimizers
from keras import backend as K
K.set_image_dim_ordering('th')

# dimensions of our images.
img_width, img_height = 200, 200

train_data_dir = 'data/train'
validation_data_dir = 'data/validation'
nb_train_samples = 2000
nb_validation_samples = 424
nb_epoch = 50


model = Sequential()
model.add(Convolution2D(64, 3, 3, init='glorot_uniform', subsample=(1, 1), input_shape=(1, img_width, img_height)))
model.add(advanced_activations.LeakyReLU(alpha=0.3))
model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))

model.add(Convolution2D(128, 3, 3, subsample=(1, 1), dim_ordering='th'))
model.add(advanced_activations.LeakyReLU(alpha=0.3))
model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))

model.add(Convolution2D(128, 3, 3, subsample=(1, 1), dim_ordering='th'))
model.add(advanced_activations.LeakyReLU(alpha=0.3))
model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))

# model.add(Convolution2D(128, 3, 3, subsample=(1, 1), dim_ordering='th'))
# model.add(advanced_activations.LeakyReLU(alpha=0.3))
# model.add(AveragePooling2D(pool_size=(2, 2), dim_ordering="th"))

model.add(Convolution2D(256, 2, 2, subsample=(1, 1), dim_ordering='th'))
model.add(advanced_activations.LeakyReLU(alpha=0.3))
model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))

model.add(Convolution2D(256, 2, 2, subsample=(1, 1), dim_ordering='th'))
model.add(advanced_activations.LeakyReLU(alpha=0.3))
model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))

# model.add(Convolution2D(128, 3, 1, subsample=(1, 1), dim_ordering='th'))
# model.add(advanced_activations.LeakyReLU(alpha=0.3))
# model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))
#
# model.add(Convolution2D(128, 1, 3, subsample=(1, 1), dim_ordering='th'))
# model.add(advanced_activations.LeakyReLU(alpha=0.3))
# model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))




# build the VGG16 network
# model = Sequential()
# model.add(ZeroPadding2D((1, 1), input_shape=(1, img_width, img_height)))
#
# model.add(Convolution2D(64, 3, 3, activation='relu', name='conv1_1'))
# model.add(ZeroPadding2D((1, 1)))
# model.add(Convolution2D(64, 3, 3, activation='relu', name='conv1_2'))
# model.add(MaxPooling2D((2, 2), strides=(2, 2)))
#
# model.add(ZeroPadding2D((1, 1)))
# model.add(Convolution2D(128, 3, 3, activation='relu', name='conv2_1'))
# model.add(ZeroPadding2D((1, 1)))
# model.add(Convolution2D(128, 3, 3, activation='relu', name='conv2_2'))
# model.add(MaxPooling2D((2, 2), strides=(2, 2)))
#
# model.add(ZeroPadding2D((1, 1)))
# model.add(Convolution2D(256, 3, 3, activation='relu', name='conv3_1'))
# model.add(ZeroPadding2D((1, 1)))
# model.add(Convolution2D(256, 3, 3, activation='relu', name='conv3_2'))
# model.add(ZeroPadding2D((1, 1)))
# model.add(Convolution2D(256, 3, 3, activation='relu', name='conv3_3'))
# model.add(MaxPooling2D((2, 2), strides=(2, 2)))
#
# model.add(ZeroPadding2D((1, 1)))
# model.add(Convolution2D(512, 3, 3, activation='relu', name='conv4_1'))
# model.add(ZeroPadding2D((1, 1)))
# model.add(Convolution2D(512, 3, 3, activation='relu', name='conv4_2'))
# model.add(ZeroPadding2D((1, 1)))
# model.add(Convolution2D(512, 3, 3, activation='relu', name='conv4_3'))
# model.add(MaxPooling2D((2, 2), strides=(2, 2)))
#
# model.add(ZeroPadding2D((1, 1)))
# model.add(Convolution2D(512, 3, 3, activation='relu', name='conv5_1'))
# model.add(ZeroPadding2D((1, 1)))
# model.add(Convolution2D(512, 3, 3, activation='relu', name='conv5_2'))
# model.add(ZeroPadding2D((1, 1)))
# model.add(Convolution2D(512, 3, 3, activation='relu', name='conv5_3'))
# model.add(MaxPooling2D((2, 2), strides=(2, 2)))

model.add(Flatten())
# model.add(Dense(128))
# model.add(advanced_activations.LeakyReLU(alpha=0.3))
# model.add(Dense(256))
# model.add(advanced_activations.LeakyReLU(alpha=0.3))
model.add(Dropout(0.5))
# model.add(Dense(8))
# model.add(advanced_activations.LeakyReLU(alpha=0.3))

model.add(Dense(1))
model.add(Activation('sigmoid'))

# model.add(Flatten())
# model.add(Dense(256, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer=optimizers.SGD(lr=1e-5, momentum=0.9),
              # optimizer='rmsprop',
              metrics=['accuracy'])

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
        # rescale=1./255,
        # shear_range=0,
        # zoom_range=0,
        # horizontal_flip=False
)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator()


train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=32,
        class_mode='binary',
        color_mode='grayscale')

validation_generator = test_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=32,
        class_mode='binary',
        color_mode='grayscale')



model.fit_generator(
        train_generator,
        samples_per_epoch=nb_train_samples,
        nb_epoch=nb_epoch,
        validation_data=validation_generator,
        nb_val_samples=nb_validation_samples)



# model.load_weights('first_try.h5')



# class_mode: "categorical", "binary", "sparse"或None之一. 默认为"categorical. 该参数决定了返回的标签数组的形式,
# "categorical"会返回2D的one-hot编码标签,"binary"返回1D的二值标签."sparse"返回1D的整数标签,如果为None则不返回任何标签,
# 生成器将仅仅生成batch数据, 这种情况在使用model.predict_generator()和model.evaluate_generator()等函数时会用到.

validation_generator = test_datagen.flow_from_directory(
                       './data2',
        target_size=(img_width, img_height),
        batch_size=5,
        class_mode=None,
        shuffle=False,
        color_mode='grayscale')
#
out = model.predict_generator(validation_generator,545)
print out
import os
filePath = './data_raw'
# for parent ,dirnames , filenames in os.walk(filePath):
#         for filename in filenames:
#                 test_img = image.load_img(os.path.join(filePath, filename), grayscale = True, target_size = [img_height, img_width])
#                 X = image.img_to_array(test_img)
#                 X = np.expand_dims(X, axis=0)
#                 out = model.predict(X)
#
#                 print out
#                 print(np.argmax(out, axis=1))
#
# from keras import backend as K
#
# get_layer_output = K.function([model.layers[0].input],[model.layers[0].output])
#                               # [model.layers[3].output])
# import numpy as np
# # layer_output = get_layer_output([np.insert(X, X.shape[1], values=np.zeros(X.shape[0]), axis=1)])[0]
# layer_output = get_layer_output([np.array([X, np.zeros(X.shape)])])[0]
# print model.get_output_at(1)

model_file = "first_try.model"
model_weight = "first_try.h5"
json_str = model.to_json()
with open(model_file, 'w') as fp:
    fp.write(json_str)
model.save_weights(model_weight)
# model.predict(x)
#
#
# model.load_weights('first_try.h5')