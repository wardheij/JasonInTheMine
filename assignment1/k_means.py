import copy
import csv
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans

def read_data(filename):
	variables = ['mood','circumplex.arousal','circumplex.valence','activity','screen','call', \
				'sms', 'appCat.builtin','appCat.communication','appCat.entertainment', \
				'appCat.finance','appCat.game','appCat.office','appCat.other',\
				'appCat.social','appCat.travel','appCat.unknown','appCat.utilities', \
				'appCat.weather']

	entry = {var: 0 for var in variables}

	with open(filename, 'r') as data_file:
		rdr = csv.reader(data_file, delimiter=',')
		next(rdr, None)

		entries = {}

		for row in rdr:

			patient, date, variable, value, times = row

			if patient not in entries:
				entries[patient] = {}
			if date not in entries[patient]:
				entries[patient][date] = copy.copy(entry)

			entries[patient][date][variable] = float(value)

		return entries

def process_data(data_dict):
	'''
	Transforms dictionary with data to a matrix containing arrays with values for
	all variables.
	'''
	data = []
	times = 1
	for patient, dates in data_dict.iteritems():
		for date, entries in dates.iteritems():
			values = entries.values()

			# # leave out mood?
			# data.append(values[:7] + values[9:])
			data.append(values)

	return np.array(data)

def init_k_means(init_data):
	'''
    //
	'''
	no_clusters = 10
	kmeans = KMeans(n_clusters=no_clusters)
	print init_data.shape
	init_data = np.array(init_data)
	kmeans.fit(init_data)

	helper_mean = [[0, 0] for y in range(no_clusters)]

	for i, val in enumerate(kmeans.labels_):
		if init_data[i][8] != 0:
			helper_mean[val][0] += init_data[i][8]
			helper_mean[val][1] += 1

   	cluster_mean = []

	for means in helper_mean:
		if means[1] != 0:
			cluster_mean.append(means[0] / means[1])
		else:
			cluster_mean.append(0)

	print cluster_mean

	return kmeans, cluster_mean

def predict_kmeans(kmeans, cluster_mean, new_data):
    return cluster_mean[kmeans.predict(new_data)[0]]

def process_kmeans(kmeans, cluster_mean, data, timeframe = 1):
	predictions = []

	for patient, pat_value in data.iteritems():
		dates = sorted(pat_value.keys())

		for i, date in enumerate(dates):
			if i < timeframe or pat_value[date].values()[8] == 0:
				continue

			predictions.append([patient, date, round(predict_kmeans(kmeans, cluster_mean, [pat_value[date].values()]))])

	return predictions

def score(data, predictions):
	points = 0.0
	tries = len(predictions)

	for prediction in predictions:
		patient, date, value = prediction

		if data[patient][date]['mood'] == round(value):
			points += 1

	return points / tries

if __name__ == '__main__':
	data_dict = read_data('compressed.csv')

	train_data = dict(data_dict.items()[(len(data_dict) * 4)/5:])
	test_data = dict(data_dict.items()[:len(data_dict)/5])

	data_matrix = process_data(train_data)
	kmeans, cluster_mean = init_k_means(data_matrix)
	predictions = process_kmeans(kmeans, cluster_mean, test_data)
	print score(data_dict, predictions)

	# for data in data_matrix:
	# 	print(data[8], predict_kmeans(kmeans, cluster_mean, [data]))
