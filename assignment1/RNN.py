from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import np_utils
import keras
import helpers
import numpy as np

print(keras.__version__)
data_dict = helpers.read_data('compressed.csv')
data_matrix, mood_index = helpers.process_data(data_dict)

model = Sequential()
model.add(Dense(32, activation='relu', input_dim=18))
model.add(Dense(10, activation='softmax'))
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

labels = data_matrix[:, mood_index]
data = np.delete(data_matrix, mood_index, axis=1)

# hier zijn je changes!!!!!!!

# Convert labels to categorical one-hot encoding
one_hot_labels = np_utils.to_categorical(labels.astype(int), 10)

# Train the model, iterating on the data in batches of 32 samples
model.fit(data, one_hot_labels, batch_size=5)

# evaluate the model
scores = model.evaluate(data, one_hot_labels)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# predictions
predictions = model.predict(data)
