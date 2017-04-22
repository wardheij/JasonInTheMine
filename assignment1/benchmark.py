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


def process(data, timeframe = 1):
	predictions = []

	for patient, pat_value in data.iteritems():
		dates = sorted(pat_value.keys())

		for i, date in enumerate(dates):
			if i < timeframe:
				continue

			predictions.append([patient, date, round(pat_value[dates[i-1]]['mood'])])

	return predictions

def score(data, predictions):
	points = 0.0
	tries = len(predictions)
	error = 0

	for prediction in predictions:
		patient, date, value = prediction

		if data[patient][date]['mood'] == round(value):
			points += 1

		error += abs(data[patient][date]['mood'] - round(value))

	return points / tries, error / tries

data = read_data('compressed.csv')
predictions = process(data)
print score(data, predictions)