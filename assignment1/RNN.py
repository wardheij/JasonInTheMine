from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import np_utils
import keras
import helpers
import numpy as np

data_dict = helpers.read_data('compressed.csv')
data_matrix = helpers.process_data(data_dict)

model = Sequential()
model.add(Dense(32, activation='relu', input_dim=100))
model.add(Dense(10, activation='softmax'))
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

labels = data_matrix[:,8]
data = np.delete(data_matrix,8, axis=1)

# Convert labels to categorical one-hot encoding
one_hot_labels = np_utils.to_categorical(labels, 10)

# Train the model, iterating on the data in batches of 32 samples
model.fit(data, one_hot_labels, batch_size=32)
