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
				entries[patient][date] = entry

			entries[patient][date][variable] = float(value)

		return entries

data = read_data('compressed.csv')

def process_data(data):
	for patient, dates in data.iteritems():
		print(patient)
		for date, entries in dates.iteritems():
			print(dates)

process_data(data)
	# fix for missing data
	# http://stackoverflow.com/questions/35611465/python-scikit-learn-clustering-with-missing-data

def init_k_means(init_data, new_data):
	'''
    Predict label for one new data point @new_data based on cluster
    centers of the initial data @init_data.
	'''
	no_clusters = 10
	kmeans = KMeans(n_clusters=no_clusters).fit(init_data)

	helper_mean = [[0,0] for y in range(no_clusters)]

	for i, val in enumerate(kmeans.labels_):
		cluster_mean[val][0] += init_data[i]['mood']
		cluster_mean[val][1] += 1

   	cluster_mean = []

	for means in cluster_mean:
		cluster_mean.append(means[0] / means[1])

	return kmeans, cluster_mean

def predict_kmeans(data, cluster_mean):
    return cluster_mean[kmeans.predict(new_data)]
