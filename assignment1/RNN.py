from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import np_utils
import keras
import helpers
import numpy as np
from numpy import linalg as LA

def append_dates(data_dict, days):
	out = []
	for i, elem in enumerate(data_dict):
		temp = []
		if i + days < len(data_dict):
			for j in range(days):
				if data_dict[i + j].keys()[0][:7] == data_dict[i + j + 1].keys()[0][:7]:
					temp = np.append(temp, data_dict[i + j].values())
			if len(temp) == days * len(elem.values()[0]):
				out.append(temp)

	out = np.array(out)
	print out.shape
	return out


data_dict = helpers.read_data('compressed.csv')
data_dict, mood_index = helpers.process_data(data_dict)
data_dict = sorted(data_dict)
data_matrix = np.array([elem.values()[0] for elem in data_dict])
data_matrix = append_dates(data_dict, 7)

batch_s = 1
scale = 10.0

best_err = 1
best_perc = 0 

while batch_s <= 32:
	model = Sequential()
	model.add(Dense(batch_s, activation='relu', input_dim=data_matrix.shape[1]))
	model.add(Dense(int(10 * scale), activation='softmax'))
	model.compile(optimizer='rmsprop',
	              loss='categorical_crossentropy',
	              metrics=['accuracy'])

	train_labels = np.array([round(data_matrix[i + 1 + len(data_matrix)/5][mood_index]*scale) for i, x in enumerate(data_matrix[len(data_matrix)/5:-1, mood_index])])
	test_labels = np.array([round(data_matrix[i + 1][mood_index]*scale) for i, x in enumerate(data_matrix[:len(data_matrix)/5, mood_index])])
	data = data_matrix
	# data = np.delete(data_matrix, mood_index, axis=1)

	train_data = data[len(data)/5:-1]
	test_data = data[:len(data)/5]
	test_data_mood = data_matrix[:len(data_matrix)/5]

	# Convert labels to categorical one-hot encoding
	train_one_hot_labels = np_utils.to_categorical(train_labels.astype(int), int(10 * scale))
	test_one_hot_labels = np_utils.to_categorical(test_labels.astype(int), int(10 * scale))

	# Train the model, iterating on the data in batches of 32 samples
	model.fit(train_data, train_one_hot_labels, epochs=50, batch_size=32, verbose=0)

	# evaluate the model
	# scores = model.evaluate(test_data, test_one_hot_labels, verbose=0)
	# print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

	# predictions
	predictions = model.predict(test_data)

	j = 0.0
	error = 0.0
	for i, entry in enumerate(test_data_mood):
		# Futiele poging de error minder te maken
		predict = np.argmax(predictions[i])
		predict = np.random.choice(np.arange(predict-2, predict+3), p=predictions[i][predict-2:predict+3]**2 / sum(predictions[i][predict-2:predict+3]**2)) / scale
		# predict = np.argmax(predictions[i])/scale

		if data_dict[i].keys()[0][:7] == data_dict[i + 1].keys()[0][:7] and round(predict) == round(entry[mood_index]):
			j += 1

		error += abs(predict - entry[mood_index])

	cur_perc = j / len(test_data_mood)
	cur_err = error / len(test_data_mood)

	print batch_s, "Percentage: ", cur_perc, "\t Average error:", cur_err

	if cur_perc > best_perc:
		best_err = cur_err
		best_perc = cur_perc
		best = batch_s

	batch_s += 1

print "Best is: ", best, "\t Percentage: ", best_perc, "\t Average error:", best_err
