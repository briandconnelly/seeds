#!/usr/bin/env python

import csv
import matplotlib.pyplot as plt
import numpy
import re
import sys

# TODO: make the command line version more powerful.
# - specify population number
# - specifg other parameters
# - handle zipped, bzipped files automatically
# - csv.reader accepts either filename and filehandle as first arg.  do this.

def plot_density(file, outfile='density.pdf', title=None, grid=True):
    has_header = csv.Sniffer().has_header(open(file, 'rb').read(256))

    f = open(file, 'rb')
    reader = csv.reader(f)
    rownum = 0

    for row in reader:
        rownum += 1

        if has_header and rownum == 1:
            colnames = row
            continue
        elif re.match('^\s*#', row[0]) != None:
            continue
        else:
            row = map(int, row)

            if rownum == 1 or (has_header and rownum == 2):
                data = numpy.array(row)
            else:
                data = numpy.vstack((data,row))

    fig = plt.figure()

    for t in range(2, data.shape[1]):
        if has_header:
            plt.plot(data[:,0], data[:,t], label=colnames[t])
        else:
            plt.plot(data[:,0], data[:,t])

    if grid:
        plt.grid()
    plt.xlabel("Time (epoch)")
    plt.ylabel("Density")

    if title:
        plt.title(title)
    if has_header:
        plt.legend()
    plt.savefig(outfile)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s <filename>" % (sys.argv[0])
        sys.exit(2)

    plot_density(file=sys.argv[1])

