import csv
from sklearn.cluster import KMeans

def read_data(filename):
	data = {}
	with open(filename, 'r') as data_file:
		rdr = csv.reader(data_file, delimiter=',')
		next(rdr, None)

		next_date = ''
		date_entries = []
		day = {}

		for i, row in rdr:
			patient, date, variable, value, times = row

			next_date = rdr[(i + 1) % len(rdr)][2]

			if variable == 'mood':
				continue

			day['date'] = date
			day[variable] = float(value)

			if date != next_date:
				date_entries.append(day)
				day = {}

	return date_entries


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
