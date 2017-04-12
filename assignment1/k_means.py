import csv
from sklearn.cluster import KMeans

def read_data(filename):
	pass

def init_k_means(init_data, new_data):
    '''
    Predict label for one new data point @new_data based on cluster
    centers of the initial data @init_data.
    '''

    kmeans = KMeans(n_clusters=10).fit(init_data)
    
    helper_mean = array van lengte n_clusters shape: [0, 0]

    for i, val in enumerate(kmeans.labels_):
    	cluster_mean[val][0] += init_data[i]['mood'] 
    	cluster_mean[val][1] += 1

   	cluster_mean = []

    for means in cluster_mean:
    	cluster_mean.append(means[0] / means[1])

    return kmeans, cluster_mean

def predict_kmeans(data, cluster_mean):
    return cluster_mean[kmeans.predict(new_data)]

