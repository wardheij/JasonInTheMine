import csv

def make_batches(filename, batchname, batchsize=10000):

	with open(filename, 'r') as data_file:
		rdr = csv.reader(data_file, delimiter=',')

		header = next(rdr, None)

		count = 0
		cur_size = 0
		last = 0
		
		out = csv.writer(open(batchname + '_' + str(count) + '.csv', 'wb'), delimiter=',')
		out.writerow(header)

		for row in rdr:
			if row[0] != last:
				if cur_size >= batchsize:
					cur_size = 0
					count += 1

					out = csv.writer(open(batchname + '_' + str(count) + '.csv', 'wb'), delimiter=',')
					out.writerow(header)

				last = row[0]

				cur_size += 1
			
			out.writerow(row)


make_batches('data/test_set_snapshot.csv', 'data/test_batches', batchsize=100)
