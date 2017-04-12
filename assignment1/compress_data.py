import csv

def read_data(filename):
	data = {}
	with open(filename, 'r') as data_file:
		rdr = csv.reader(data_file, delimiter=',')
		next(rdr, None)

		for row in rdr:
			_, patient, time, variable, value = row

			if value == 'NA':
				continue

			date = time[:10]
			value = float(value)

			if patient in data:
				if date in data[patient]:
					if variable in data[patient][date]:
						data[patient][date][variable][0] += value
						data[patient][date][variable][1] += 1
					else:
						data[patient][date][variable] = [value, 1]
				else:
					data[patient][date] = {}
					data[patient][date][variable] = [value, 1]
			else:
				data[patient] = {}
				data[patient][date] = {}
				data[patient][date][variable] = [value, 1]

	return data

def write_data(data, filename):
	with open(filename, 'wb') as data_file:
		out = csv.writer(data_file, delimiter=',')

		for patient, pat_value in data.iteritems():
			for date, dat_value in pat_value.iteritems():
				for variable, arr in dat_value.iteritems():
					value, amount = arr

					out.writerow([patient, date, variable, value / amount, amount])

data = read_data('dataset_mood_smartphone.csv')
print len(data)
write_data(data, 'compressed.csv')
