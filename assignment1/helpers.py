# WJ Vrielink, WJ Heij, HJ Haanstra
#
# helpers.py
#
# Helper functions for data representation.
#
# 23-4-2017


import copy
import csv
import random

import numpy as np

from sklearn.cluster import KMeans

def read_data(filename):
	"""
    Reads data from 'filename' into nested dictionary with [patients][date][variables].
    """
	variables = ['mood','circumplex.arousal','circumplex.valence','activity','screen','call', \
				'sms', 'appCat.builtin','appCat.communication','appCat.entertainment', \
				'appCat.finance','appCat.game','appCat.office','appCat.other',\
				'appCat.social','appCat.travel','appCat.unknown','appCat.utilities', \
				'appCat.weather']

	entry = {var: 0 for var in variables}

	with open(filename, 'r') as data_file:
		rdr = csv.reader(data_file, delimiter=',')
		next(rdr, None)

		entries = {}

		for row in rdr:

			patient, date, variable, value, times = row

			if patient not in entries:
				entries[patient] = {}
			if date not in entries[patient]:
				entries[patient][date] = copy.copy(entry)

			entries[patient][date][variable] = float(value)

		return entries

def process_data(data_dict):
	'''
	Transforms dictionary with data to a list of dictionaries containing arrays with values for
	all variables. Dict should be [patients][date][variables].
	'''
	data = []
	times = 1
	for patient, dates in data_dict.items():
		for date, entries in dates.items():
			values = entries.values()
			values = list(values)
			if values[8] != 0:
				data.append({patient + date: list(values)})

	return data, 8
