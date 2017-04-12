import csv

def read_data(filename):
	data = {}
	with open(filename, 'r') as data_file:
		rdr = csv.reader(data_file, delimiter=',')
		next(rdr, None)

		for row in rdr:
			patient, date, variable, value, times = row

			if variable != 'mood':
				continue

			value = float(value)

			if patient in data:
				if date in data[patient]:
					data[patient][date][variable] = value
				else:
					data[patient][date] = {}
					data[patient][date][variable] = value
			else:
				data[patient] = {}
				data[patient][date] = {}
				data[patient][date][variable] = value

	return data


def process(data, timeframe):
	predictions = []

	for patient, pat_value in data.iteritems():
		dates = sorted(pat_value.keys())

		for i, date in enumerate(dates):
			if i < timeframe:
				continue

			predictions.append([patient, date, int(pat_value[dates[i-1]]['mood'])])

	return predictions

def score(data, predictions):
	points = 0.0
	tries = len(predictions)

	for prediction in predictions:
		patient, date, value = prediction

		if data[patient][date]['mood'] == value:
			points += 1

	return points / tries

data = read_data('compressed.csv')
predictions = process(data, 1)
print score(data, predictions)