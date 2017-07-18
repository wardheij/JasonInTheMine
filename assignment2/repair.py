import csv

file_in = 'data/test_set_VU_DM_2014.csv'
file_out = 'data/submission.csv'
file_final = 'data/outfile.csv'

with open(file_in, 'r') as in_file:
    rdr = csv.reader(in_file, delimiter=',')
    header  = next(rdr, None)
    counter = 0
    with open(file_out, 'r') as out_file:
        rdr2 = csv.reader(out_file, delimiter=',')
        header2 = next(rdr2, None)
        with open(file_final, 'wb') as final_file:
            rdr3 = csv.writer(final_file, delimiter=',')
            rdr3.writerow(header2)
            # Afhankelijk van header uitcommenten:
            thing = next(rdr2)  

            for row in rdr:
                counter += 1
                
                if int(row[0]) != int(thing[0]):
                    rdr3.writerow([int(row[0]), int(row[7])])       
                else:
                    rdr3.writerow(thing)
                    thing = next(rdr2)
