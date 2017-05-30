import csv

original = 'data/test_set_VU_DM_2014.csv'
filename = 'data/outfile.csv'
filename2 = 'data/repaired.csv'

with open(original, 'r') as data_file:
	rdr = csv.reader(data_file, delimiter=',')

	header = next(rdr, None)

	with open(filename, 'r') as data_file2:
		rdr2 = csv.reader(data_file2, delimiter=',')

		header2 = next(rdr2, None)

		count = 0
		cur_size = 0
		last = 0
		
		out = csv.writer(open(filename2, 'wb'), delimiter=',')

		out.writerow(header2)

		cache = []
		cache2 = []
		okay = False

		for row in rdr:
			if row[0] != last:
				for ding in cache2:
					if ding not in cache:
						if len(cache) > 1:
							print len(cache), cur_size
							
							for s in cache:
								out.writerow(s)
							break
						out.writerow(cache[0])
					else:
						cache.remove(ding)
						out.writerow(ding)


				cache = []
				cache2 = []

				last = row[0]

			cache.append([int(row[0]), int(row[7])])
			row2 = next(rdr2, None)
			cache2.append([int(row2[0]), int(row2[1])])
			cur_size += 1


		for ding in cache2:
			while ding not in cache:
				count += 1
				ding = [ding[0], ding[1] + '0']
				if not count % 10000:
					print 'count'
			out.writerow(ding)

