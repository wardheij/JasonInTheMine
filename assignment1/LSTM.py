import helpers

import numpy as np
import tensorflow as tf

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
data_dict = helpers.read_data('compressed.csv')
data_dict, mood_index = helpers.process_data(data_dict)

# print(data_dict)

# data_dict = sorted(data_dict)  # TODO: fix sorting
data_matrix = np.array([list(elem.values())[0] for elem in list(data_dict)])
# data_matrix = append_dates(data_dict, 5) # TODO: dit gaat nog fout snik

# Build NN
# model = Sequential()
# model.add(Dense(32, activation='relu', input_dim=data_matrix.shape[1]))
# model.add(Dense(32, activation='softmax'))
# model.add(Dense(int(10 * scale), activation='softmax'))
# model.compile(optimizer='rmsprop',
#               loss='categorical_crossentropy',
#               metrics=['accuracy'])

# http://monik.in/a-noobs-guide-to-implementing-rnn-lstm-using-tensorflow/

num_vars = 30 # TODO: hoeveel variabelen zijn er per dag gelogd?
num_hidden = 24 # TODO: geen idee hoeveel dit moet zijn

input_placeholder = tf.placeholder(tf.float32, [None, num_vars, 1])
output_placeholder = tf.placeholder(tf.float32, [None, 10, 1])
cell = tf.nn.rnn_cell.LSTMCell(num_hidden, state_is_tuple=True)

val, state = tf.nn.dynamic_rnn(cell, input_placeholder, dtype=tf.float32)

val = tf.transpose(val, [1, 0, 2])
last = tf.gather(val, int(val.get_shape()[0]) - 1)

weight = tf.Variable(tf.truncated_normal([num_hidden, int(output_placeholder.get_shape()[1])]))
bias = tf.Variable(tf.constant(0.1, shape=[output_placeholder.get_shape()[1]]))

prediction = tf.nn.softmax(tf.matmul(last, weight) + bias)

cross_entropy = -tf.reduce_sum(output_placeholder * tf.log(tf.clip_by_value(prediction,1e-10,1.0)))

optimizer = tf.train.AdamOptimizer()
minimize = optimizer.minimize(cross_entropy)

init_op = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init_op)

# batch_size = 1000
# no_of_batches = int(len(train_input)/batch_size)
# epoch = 5000
# for i in range(epoch):
#     ptr = 0
#     for j in range(no_of_batches):
#         inp, out = train_input[ptr:ptr+batch_size], train_output[ptr:ptr+batch_size]
#         ptr+=batch_size
#         sess.run(minimize,{data: inp, target: out})
#     print "Epoch - ",str(i)
# incorrect = sess.run(error,{data: test_input, target: test_output})
# print('Epoch {:2d} error {:3.1f}%'.format(i + 1, 100 * incorrect))
# sess.close()

# # Set labels
# train_labels = np.array([round(data_matrix[i + 1 + len(data_matrix)/5][mood_index]*scale) for i, x in enumerate(data_matrix[len(data_matrix)/5:-1, mood_index])])
# test_labels = np.array([round(data_matrix[i + 1][mood_index]*scale) for i, x in enumerate(data_matrix[:len(data_matrix)/5, mood_index])])
# data = data_matrix

# # Set data
# train_data = data[len(data)/5:-1]
# test_data = data[:len(data)/5]
# test_data_mood = data_matrix[:len(data_matrix)/5]

# # Convert labels to categorical one-hot encoding
# train_one_hot_labels = np_utils.to_categorical(train_labels.astype(int), int(10 * scale))
# test_one_hot_labels = np_utils.to_categorical(test_labels.astype(int), int(10 * scale))

# print(test_one_hot_labels)


# # Train the model, iterating on the data in batches of 32 samples
# model.fit(train_data, train_one_hot_labels, epochs=50, batch_size=32, verbose=0)
#
# # Predictions
# predictions = model.predict(test_data)
#
# # Calculate score
# j = 0.0
# error = 0.0
#
# for i, entry in enumerate(test_data_mood):
# 	predict = np.argmax(predictions[i]) / scale
#
# 	if data_dict[i].keys()[0][:7] == data_dict[i + 1].keys()[0][:7] and round(predict) == round(entry[mood_index]):
# 		j += 1
#
# 	error += abs(predict - entry[mood_index])
#
# cur_perc = j / len(test_data_mood)
# cur_err = error / len(test_data_mood)
#
# print("Percentage: ", cur_perc, "\t Average error:", cur_err)
