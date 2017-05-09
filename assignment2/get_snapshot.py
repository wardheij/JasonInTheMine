import random
import csv

def get_snapshot(filename, outfile):
	random.seed(42)

	with open(filename, 'r') as data_file:
		rdr = csv.reader(data_file, delimiter=',')

		with open(outfile, 'wb') as out_file:
			out = csv.writer(out_file, delimiter=',')

			out.writerow(next(rdr, None))

			last = 0
			skip = True

			for row in rdr:
				if row[0] != last:
					last = row[0]

					if random.random() < .999:
						skip = True
					else:
						skip = False

				if not skip:
					out.writerow(row)

get_snapshot('data/test_set_VU_DM_2014.csv', 'data/test_set_snapshot.csv')




