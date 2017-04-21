import copy
import csv
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
	for patient, dates in data_dict.iteritems():
		for date, entries in dates.iteritems():
			values = entries.values()

			# # leave out mood?
			# data.append(values[:7] + values[9:])
			data.append(values)

	return data

	# fix for missing data
	# http://stackoverflow.com/questions/35611465/python-scikit-learn-clustering-with-missing-data

def init_k_means(init_data):
	'''
    //
	'''
	no_clusters = 10
	kmeans = KMeans(n_clusters=no_clusters)
	kmeans.fit(init_data)

	helper_mean = [[0,0] for y in range(no_clusters)]

	for i, val in enumerate(kmeans.labels_):
		helper_mean[val][0] += init_data[i][8]
		helper_mean[val][1] += 1

   	cluster_mean = []

	for means in helper_mean:
		cluster_mean.append(means[0] / means[1])

	return kmeans, cluster_mean

def predict_kmeans(cluster_mean, new_data):
    return cluster_mean[kmeans.predict(new_data)]

if __name__ == '__main__':
	data_dict = read_data('compressed.csv')
	data_matrix = process_data(data_dict)
	kmeans, cluster_mean = init_k_means(data_matrix)
