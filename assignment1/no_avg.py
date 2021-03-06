# WJ Vrielink, WJ Heij, HJ Haanstra
#
# compress_data.py
#
# Compress input data to reduce file size.
#
# 23-4-2017


import csv

def read_data(filename):
    """
    Reads data from 'filename' into nested dictionary with [patients][date][variables].
    """

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
    """
    Writes data back in a compressed format.
    """
    with open(filename, 'wb') as data_file:
        out = csv.writer(data_file, delimiter=',')

        for patient, pat_value in data.iteritems():
            for date, dat_value in pat_value.iteritems():
                for variable, arr in dat_value.iteritems():
                    value, amount = arr

                    if variable in ["mood", "circumplex.arousal", "circumplex.valence", "activity"]:
                        out.writerow([patient, date, variable, value / amount, amount])
                    else:
                        out.writerow([patient, date, variable, value, amount])

if __name__ == '__main__':
    data = read_data('dataset_mood_smartphone.csv')
    write_data(data, 'additive_and_avg_compressed.csv')
