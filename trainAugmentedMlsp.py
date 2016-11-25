from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import SGD
from time import localtime, strftime

import numpy as np

from bird import loader as loader
from bird.models.cuberun import CubeRun

# Settings
nb_epoch_per_mini_batch = 5
batch_size = 16
nb_classes = 19
batch_size = 8
input_shape = (257, 509)
(image_height, image_width) = input_shape
train_path = "./datasets/mlsp2013/train_preprocessed";
labels_path = "./datasets/mlsp2013/train_preprocessed/file2labels.csv";
weight_file_path = "./weights/" + strftime("%Y_%m_%d_%H:%M:%S_", localtime()) + "cuberun.h5"
samplerate = 16000

# Settings Mini Batch Generator
nb_augmentation_samples = 4000
nb_mini_baches = 5
nb_segments_per_mini_batch = 500

model = CubeRun(nb_classes=nb_classes, input_shape=input_shape)

# Setup compile
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='binary_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])

print (strftime("%a, %d %b %Y %H:%M:%S +0000", localtime()))
# load the data
mini_batch_generator = loader.mini_batch_generator(nb_augmentation_samples,
                                              nb_mini_baches,
                                              nb_segments_per_mini_batch,
                                              train_path, labels_path,
                                                   nb_classes, samplerate)

for X_train, Y_train in mini_batch_generator:
    print("X train shape:", X_train.shape)
    print("Y train shape:", Y_train.shape)
    model.fit(X_train, Y_train, batch_size, nb_epoch_per_mini_batch)


# fit the model to training data

# save the weights
model.save_weights(weight_file_path)
print (strftime("%a, %d %b %Y %H:%M:%S +0000", localtime()))
print ("The weights have been saved in: " + weight_file_path)
