# -*- coding: utf-8 -*-
"""oil_spill_final

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tNzkWWjahm9YipKOMsvDONLZVkHfjxCZ
"""

import numpy as np
import pandas as pd

from google.colab import drive
  drive.mount('/content/drive')



import os
folder_path = '/content/drive/MyDrive/dataset'
os.chdir(folder_path)

import os
folder_contents = os.listdir(folder_path)
print(folder_contents)

from PIL import Image
import shutil
import matplotlib.pyplot as plt
import glob
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os

train_no_spill_dir = '/content/drive/MyDrive/dataset/train/Non Oil Spill'

train_no_spill_count = len([f for f in os.listdir(train_no_spill_dir) if os.path.isfile(os.path.join(train_no_spill_dir, f))])

print("Number of No Spill images in train dataset:", train_no_spill_count)

import os

train_spill_dir = '/content/drive/MyDrive/dataset/train/Oil Spill'

train_spill_count = len([f for f in os.listdir(train_spill_dir) if os.path.isfile(os.path.join(train_spill_dir, f))])

print("Number of Spill images in train dataset:", train_spill_count)

import os

test_no_spill_dir = '/content/drive/MyDrive/dataset/test/Non Oil Spill'

test_no_spill_count = len([f for f in os.listdir(test_no_spill_dir) if os.path.isfile(os.path.join(test_no_spill_dir, f))])

print("Number of No Spill images in test dataset:", test_no_spill_count)

import os

test_spill_dir = '/content/drive/MyDrive/dataset/test/Oil Spill'

test_spill_count = len([f for f in os.listdir(test_spill_dir) if os.path.isfile(os.path.join(test_spill_dir, f))])

print("Number of Spill images in test dataset:", test_spill_count)

i=0
for non_oilspill_train_file in os.listdir(f"/content/drive/MyDrive/dataset/train/Non Oil Spill"):
    img = Image.open(f"/content/drive/MyDrive/dataset/train/Non Oil Spill/{non_oilspill_train_file}")
    plt.imshow(img)
    plt.title(non_oilspill_train_file)
    plt.show()
    i+=1
    if i==5:
        break

i=0
for oilspill_train_file in os.listdir(f"/content/drive/MyDrive/dataset/train/Oil Spill"):
    img = Image.open(f"/content/drive/MyDrive/dataset/train/Oil Spill/{oilspill_train_file}")
    plt.imshow(img)
    plt.title(oilspill_train_file)
    plt.show()
    i+=1
    print(i)
    if i==5:
        break

i=0
for non_spill_test_file in os.listdir("/content/drive/MyDrive/dataset/test/Non Oil Spill"):
    img = Image.open(f"/content/drive/MyDrive/dataset/test/Non Oil Spill/{non_spill_test_file}")
    plt.imshow(img)
    plt.title(non_spill_test_file)
    plt.show()
    i+=1
    if i==5:
        break

i=0
for oilspill_test_file in os.listdir("/content/drive/MyDrive/dataset/test/Oil Spill"):
    img = Image.open(f"/content/drive/MyDrive/dataset/test/Oil Spill/{oilspill_test_file}")
    plt.imshow(img)
    plt.title(oilspill_test_file)
    plt.show()
    i+=1
    if i==5:
        break

train_datagen = ImageDataGenerator(rescale=1/255)
validation_datagen = ImageDataGenerator(rescale=1/255)

train_generator = train_datagen.flow_from_directory(
    "/content/drive/MyDrive/dataset/train",
    target_size=(150,150),
    class_mode="binary"
)

validation_generator = validation_datagen.flow_from_directory(
    "/content/drive/MyDrive/dataset/test",
    target_size=(150,150),
    class_mode="binary"
)

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch,logs={}):
    if(logs.get('accuracy')>=0.95):
      print("\nReached 95% accuracy so cancelling training1")
      self.model.stop_training=True
callbacks = myCallback()

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16,(3,3), activation = "relu", input_shape=(150,150,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(32,(3,3), activation = "relu"),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64,(3,3), activation = "relu"),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation="relu"),
    tf.keras.layers.Dense(1,activation = 'sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(
    train_generator,
    steps_per_epoch = 8,
    epochs = 50,
    verbose=1,
    validation_data=validation_generator,
    callbacks=[callbacks]
)

acc = history.history["accuracy"]
val_acc = history.history["val_accuracy"]
loss = history.history["loss"]
val_loss = history.history["val_loss"]

epochs = range(1, len(acc) + 1)

fig = plt.figure(figsize=(25,8))
ax1 = fig.add_subplot(121)
ax1.plot(epochs, acc, "b-", label="Training acc")
ax1.plot(epochs, val_acc, "g-", label="Validation acc")
ax1.set_title("Training and validation accuracy")
ax1.legend()

ax2 = fig.add_subplot(122)
ax2.plot(epochs, loss, "b-", label="Training loss")
ax2.plot(epochs, val_loss, "g-", label="Validation loss")
ax2.set_title("Training and validation loss")
ax2.legend()

import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

model = tf.keras.models.load_model('model.h5')

target_size = (150, 150)

image_path = '/content/drive/MyDrive/test2.jpg'
img = image.load_img(image_path, target_size=target_size)
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.0

img.show()

prediction = model.predict(img_array)
if prediction[0] < 0.5:
    print("Predicted class: Non Oil Spill")
else:
    print("Predicted class: Oil Spill")

