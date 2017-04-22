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

			if values[8] != 0:
				data.append({patient + date: values})

	return data

def init_k_means(in_data, no_clusters = 10):
	'''
    //
	'''
	in_data = sorted(in_data)
	init_data = np.array([elem.values()[0] for elem in in_data])

	kmeans = KMeans(n_clusters = no_clusters, n_init = 10)

	# Leave out mood?
	# kmeans.fit(init_data)
	kmeans.fit(init_data[:, np.arange(init_data.shape[1]) != 8])

	helper_mean = [[0, 0] for y in range(no_clusters)]

	for i, val in enumerate(kmeans.labels_):
		if i < len(kmeans.labels_) - 1 and in_data[i].keys()[0][:7] == in_data[i + 1].keys()[0][:7]:
			helper_mean[val][0] += in_data[i + 1].values()[0][8]
			helper_mean[val][1] += 1

   	cluster_mean = []

	for means in helper_mean:
		if means[1] != 0:
			cluster_mean.append(means[0] / means[1])
		else:
			cluster_mean.append(0)

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
			# Leave out mood?
			# predictions.append([patient, date, predict_kmeans(kmeans, cluster_mean, [pat_value[date].values()])])
			predictions.append([patient, date, predict_kmeans(kmeans, cluster_mean, [pat_value[date].values()[:8]+pat_value[date].values()[9:]])])

	return predictions

def score(data, predictions):
	points = 0.0
	tries = len(predictions)
	error = 0

	for prediction in predictions:
		patient, date, value = prediction

		if data[patient][date]['mood'] == round(value):
			points += 1

		error += abs(data[patient][date]['mood'] - value)

	return points / tries, error / tries

if __name__ == '__main__':
	data_dict = read_data('compressed.csv')

	train_data = dict(data_dict.items()[len(data_dict)/5:])
	test_data = dict(data_dict.items()[:len(data_dict)/5])

	data_matrix = process_data(train_data)

	best = 0
	best_percentage = 0
	best_error = 0
	for i in range(1, 30):
		kmeans, cluster_mean = init_k_means(data_matrix, i)
		predictions = process_kmeans(kmeans, cluster_mean, test_data)
		percentage, avg_error = score(data_dict, predictions)

		print i, "Percentage: ", percentage, "\t Average error:", avg_error

		if percentage > best_percentage or avg_error < best_error:
			best = i
			best_percentage = percentage
			best_error = avg_error

	print "Best is: ", best, "\t Percentage: ", best_percentage, "\t Average error:", best_error

