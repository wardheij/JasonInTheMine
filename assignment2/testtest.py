import csv

file_in = 'data/test_set_VU_DM_2014.csv'
file_out = 'data/repaired.csv'

with open(file_in, 'r') as in_file:
	rdr = csv.reader(in_file, delimiter=',')

	header  = next(rdr, None)

	counter = 0

	with open(file_out, 'r') as out_file:
		rdr2 = csv.reader(out_file, delimiter=',')

		# Afhankelijk van header uitcommenten:
		header2 = next(rdr2, None)
		print header2

		for row in rdr:
			counter +=1
			thing = rdr2.next()

			if int(row[0]) != int(thing[0]):
				print "Gaat fout op regel:", counter
				print "in: ", int(row[0]), "    out: ", int(thing[0])
				break