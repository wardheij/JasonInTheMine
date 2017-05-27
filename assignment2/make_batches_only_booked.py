import csv

def make_batches(filename, batchname, batchsize=10000):

	with open(filename, 'r') as data_file:
		rdr = csv.reader(data_file, delimiter=',')

		header = next(rdr, None)

		count = 0
		cur_size = 0
		last = 0
		
		out = csv.writer(open(batchname + '_' + str(count) + '.csv', 'wb'), delimiter=',')
		print header[-1], header[-3]
		out.writerow(header)

		cache = []
		clicked = 0
		booked = 0

		lucky = 0

		for row in rdr:
			if row[0] != last:
				for cached in cache:
					out.writerow(cached)

				print "booked: ", booked, "    clicked: ", clicked

				cache = []
				clicked = 0
				booked = 0

				if cur_size >= batchsize:
					cur_size = 0
					count += 1

					out = csv.writer(open(batchname + '_' + str(count) + '.csv', 'wb'), delimiter=',')
					out.writerow(header)

				last = row[0]

				cur_size += 1
			
			# out.writerow(row)
			cache.append(row)
			if int(row[-1]):
				booked += 1
			if int(row[-3]):
				clicked += 1
				lucky+=1


		for cached in cache:
			out.writerow(cached)

		print "Total clicks: ", lucky

make_batches('data/training_set_snapshot.csv', 'data/training_special_batches', batchsize=100)
