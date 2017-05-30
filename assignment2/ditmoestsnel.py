import csv

def make_batches(filename, batchname, batchsize=10000):

	with open(filename, 'r') as data_file:
		rdr = csv.reader(data_file, delimiter=',')

		header = next(rdr, None)

		count = 0
		cur_size = 0
		last = 0
		
		out = csv.writer(open(batchname + '_' + str(count) + '.csv', 'wb'), delimiter=',')
		# out.writerow(header)

		print header[7]

		for row in rdr:
			if int(row[0]) > 332172:
				out.writerow([row[0], row[7]])


make_batches('data/test_set_VU_DM_2014.csv', 'data/outdingetje', batchsize=100)

