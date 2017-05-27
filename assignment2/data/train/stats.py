import numpy as np
import os

no_variables = 55

def get_stats(data_matrix):
    stats = np.empty([5, no_variables])
    length = len(data_matrix)
    for i in range(no_variables):
        stats[0,i] = len(np.unique(data_matrix[~np.isnan(data_matrix[:,i])]))
        stats[1,i] = data_matrix[:,i].size - np.count_nonzero(~np.isnan(data_matrix[:,i]))
        stats[2,i] = length - np.count_nonzero(data_matrix[~np.isnan(data_matrix[:,i])])
        data_matrix[data_matrix[:,i] == 0] = np.nan

        stats[3,i] = np.nanmean(data_matrix[:, i])
        stats[4,i] = np.nanstd(data_matrix[:,i])

    return stats, length

def load_csv(filename):
    skip = 0
    if '0' in filename:
        skip = 1
    return np.genfromtxt(open(filename, "rb"), skip_header=skip, delimiter=",")


if __name__ == "__main__":
    files = os.listdir(os.getcwd())

    stats = np.zeros([5, no_variables])
    total_length = 0
    for f in files:
        if f.endswith(".csv"):
            print('Load {}..'.format(f))
            data = load_csv(f)
            print('File loaded.')
            print('Getting stats..')
            f_stats, length = get_stats(data)
            stats = np.add(stats, f_stats)
            total_length += length
            print('Total number of entries: {}'.format(total_length))
            print('Statistics calculated.')
        else:
            continue

    stats[3:,:] = np.divide(stats[3:,:], 10)

    # np.savetxt('unique.txt', stats[0,:])
    # np.savetxt('missing.txt', stats[1,:])
    # np.savetxt('zeros.txt', stats[2,:])
    # np.savetxt('mean.txt', stats[3,:])
    # np.savetxt('std.txt', stats[4,:])
    np.savetxt('percentages_new.txt', np.divide(stats, total_length))
    print('Total number of entries: {}'.format(total_length))
