import keras
import helpers

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import np_utils
from keras.layers.recurrent import LSTM

from numpy import linalg as LA

def append_dates(data_dict, days):
	"""
	Flattens the data of multiple time instances.
	"""
	out = []

	for i, elem in enumerate(data_dict):
		temp = []
	
		# Prevent out of range
		if i + days < len(data_dict):
			for j in range(days):
				# If the next date belongs to the same patient
				if data_dict[i + j].keys()[0][:7] == data_dict[i + j + 1].keys()[0][:7]:
					temp = np.append(temp, data_dict[i + j].values())
		
			# Only if all dates are present
			if len(temp) == days * len(elem.values()[0]):
				out.append(temp)

	out = np.array(out)
	return out

# Scales the output to enhance precision
scale = 10.0

# Prepare data
data_dict = helpers.read_data('additive_and_avg_compressed.csv')
data_dict, mood_index = helpers.process_data(data_dict)
data_dict = sorted(data_dict)
data_matrix = np.array([elem.values()[0] for elem in data_dict])
data_matrix = append_dates(data_dict, 1)

# Build NN
model = Sequential()
# model.add(Dense(32, activation='relu', input_dim=data_matrix.shape[1]))
# model.add(Dense(32, activation='softmax'))
# model.add(Dense(int(10 * scale), activation='softmax'))
# model.compile(optimizer='rmsprop',
#               loss='categorical_crossentropy',
#               metrics=['accuracy'])

layers = [95, 50, 100, int(10 * scale)]

model.add(LSTM(
        layers[1],
        input_dim=data_matrix.shape[1],
        return_sequences=True))

model.add(Dropout(0.2))

model.add(LSTM(
        layers[2],
        return_sequences=False))

model.add(Dropout(0.2))

model.add(Dense(
        layers[3]))

model.add(Activation("linear"))
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
# Comment

# Set labels
train_labels = np.array([round(data_matrix[i + 1 + len(data_matrix)/5][mood_index]*scale) for i, x in enumerate(data_matrix[len(data_matrix)/5:-1, mood_index])])
test_labels = np.array([round(data_matrix[i + 1][mood_index]*scale) for i, x in enumerate(data_matrix[:len(data_matrix)/5, mood_index])])
data = data_matrix

# Set data
train_data = data[len(data)/5:-1]

train_data = np.reshape(train_data, (train_data.shape[0], train_data.shape[1], 1))

test_data = data[:len(data)/5]
test_data_mood = data_matrix[:len(data_matrix)/5]

# Convert labels to categorical one-hot encoding
train_one_hot_labels = np_utils.to_categorical(train_labels.astype(int), int(10 * scale))
test_one_hot_labels = np_utils.to_categorical(test_labels.astype(int), int(10 * scale))

# Train the model, iterating on the data in batches of 32 samples
model.fit(train_data, train_one_hot_labels, epochs=50, batch_size=32, verbose=1)

# Predictions
predictions = model.predict(test_data)

# Calculate score
j = 0.0
error = 0.0

for i, entry in enumerate(test_data_mood):
	predict = np.argmax(predictions[i]) / scale

	if data_dict[i].keys()[0][:7] == data_dict[i + 1].keys()[0][:7] and round(predict) == round(entry[mood_index]):
		j += 1

	error += abs(predict - entry[mood_index])

cur_perc = j / len(test_data_mood)
cur_err = error / len(test_data_mood)

print "Percentage: ", cur_perc, "\t Average error:", cur_err
