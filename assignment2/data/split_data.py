import pandas as pd
import csv

def split_data(filename, set):

	for i,chunk in enumerate(pd.read_csv(filename, chunksize=1000)):
		chunk.to_csv('{}_batch_{}.csv'.format(set, i))

split_data('test_chunk_1.csv', 'test')
