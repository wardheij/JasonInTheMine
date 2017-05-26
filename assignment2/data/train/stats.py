import numpy as np
import os

no_variables = 51

def get_stats(data_matrix):
    stats = np.empty([5, no_variables])
    for i in range(no_variables):
        stats[0,i] = len(np.unique(data_matrix[:,i]))
        stats[1,i] = data_matrix[:,i].size - np.count_nonzero(~np.isnan(data_matrix[:,i]))
        stats[2,i] = np.count_nonzero(data_matrix[:,i])
        data_matrix[data_matrix == 0] = np.nan

        stats[3,i] = np.nanmean(data_matrix[:, i])
        stats[4,i] = np.nanstd(data_matrix[:,i])
    return stats

def load_csv(filename):
    skip = 0
    if '0' in filename:
        skip = 1
    return np.genfromtxt(open(filename, "rb"), skip_header=skip, delimiter=",")


if __name__ == "__main__":
    files = os.listdir(os.getcwd())

    stats = np.zeros([5, no_variables])

    for f in files:
        if f.endswith(".csv"):
            print('Load {}..'.format(f))
            data = load_csv(f)
            print('File loaded.')
            print('Getting stats..')
            stats = np.add(stats, get_stats(data))
            print('Statistics calculated.')
        else:
            continue
    stats = np.divide(stats, len(files))
    np.savetxt('unique.txt', stats[0,:])
    np.savetxt('missing.txt', stats[1,:])
    np.savetxt('zeros.txt', stats[2,:])
    np.savetxt('mean.txt', stats[3,:])
    np.savetxt('std.txt', stats[4,:])
