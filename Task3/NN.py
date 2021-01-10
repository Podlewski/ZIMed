import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pydicom
import pandas as pd
import os
import sklearn.metrics as metrics
import tensorflow as tf

from tensorflow.keras import layers, models
from tensorflow.python.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


def get_pixels_hu(scan):
    image = scan.pixel_array.astype(np.int16)
    image[image == -2000] = 0

    intercept = ds.RescaleIntercept
    slope = ds.RescaleSlope

    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)

    image += np.int16(intercept)
    return np.array(image, dtype=np.int16)


MIN_BOUND = -1000.0
MAX_BOUND = 400.0


def normalize(image):
    image = (image - MIN_BOUND) / (MAX_BOUND - MIN_BOUND)
    image[image > 1] = 1.
    image[image < 0] = 0.
    return image


PIXEL_MEAN = 0.3


def zero_center(image):
    image = image - PIXEL_MEAN
    return image


def change_label_to_int(label):
    if label == 'Intraventricular':
        return 0
    elif label == 'Intraparenchymal':
        return 1
    elif label == 'Subarachnoid':
        return 2
    elif label == 'Chronic':
        return 3
    elif label == 'Subdural':
        return 4
    elif label == 'Epidural':
        return 5


models_directory = './dcm_files/models'
if not os.path.isdir(models_directory):
    os.mkdir(models_directory)

classes = ['Intraventricular', 'Intraparenchymal', 'Subarachnoid', 'Chronic', 'Subdural', 'Epidural']

# descriptions = pd.read_excel('./dcm_files/my_descriptions.xlsx', usecols=['category', 'path'])[0:50]
descriptions = pd.read_csv('./dcm_files/my_description_balanced.csv', usecols=['category', 'path'])
descriptions['category'] = descriptions['category'].apply(lambda x: change_label_to_int(x))
print(descriptions.groupby(by='category').count())

categories = descriptions['category'].to_numpy()
images = descriptions['path'].to_numpy()

x = []
y = []
for idx, img in enumerate(images):
    ds = pydicom.filereader.dcmread(img)
    image = get_pixels_hu(ds)
    image = normalize(image)
    image = zero_center(image)
    x.append(image)
    y.append(categories[idx])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)

y_train = np.array(y_train)
y_test = np.array(y_test)

x_train = np.array(x_train)
x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], x_train.shape[2], 1))
x_test = np.array(x_test)
x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], x_test.shape[2], 1))

print('y_train shape: ', y_train.shape, 'x_train_shape: ', x_train.shape)
print('y_train shape: ', y_test.shape, 'x_train_shape: ', x_test.shape)

img_width = 512
img_height = 512

cnn = models.Sequential([
    layers.Conv2D(filters=32, kernel_size=(5, 5), activation='relu', input_shape=(img_width, img_height, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(filters=64, kernel_size=(5, 5), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(32, activation='relu'),
    layers.Dense(len(classes), activation='softmax')
])

checkpoint_filepath = './dcm_files/models/'
metric = 'accuracy'
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=True,
    monitor=metric,
    mode='max',
    save_best_only=True)
early = EarlyStopping(monitor='accuracy', mode='min', patience=3)
learning_rate_reduction = ReduceLROnPlateau(monitor='accuracy', patience=3, verbose=1, factor=0.3, min_lr=0.000001)
callbacks_list = [early, learning_rate_reduction, model_checkpoint_callback]

cnn.summary()
cnn.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
cnn.fit(x_train, y_train, epochs=150, batch_size=32, callbacks=callbacks_list, shuffle=True)
cnn.save('./dcm_files/models/my_model.h5')

pd.DataFrame(cnn.history.history).plot()
plt.show()

cnn_eval = cnn.evaluate(x_test, y_test)
print(cnn_eval)

y_pred = cnn.predict(x_test)
y_pred_classes = [np.argmax(element) for element in y_pred]

confusion_matrix = metrics.confusion_matrix(y_true=y_test, y_pred=y_pred_classes)
sns.heatmap(confusion_matrix, cmap='coolwarm', square=True, annot=True, annot_kws={'size': 16}, cbar=False,
            xticklabels=classes, yticklabels=classes)
plt.xlabel('Predicted values')
plt.ylabel('True values')
plt.show()

print("Classification Report: \n", classification_report(y_test, y_pred_classes))
