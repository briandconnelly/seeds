#!/usr/bin/env python

import csv
import os
import numpy
import gzip

import matplotlib.pyplot as plt

# -------------------------------------------------------------------
runname = "ld100-%02d-novtrans_%d"
datadir = "data"
file = "cell_type_count.dat.gz"
reps = range(400,403)
ld100s = [1,5,10,15,20,25,30,35,40,45,50]
labels = ['Empty', 'Uninfected-Susceptible', 'Uninfected-Resistant',
          'Infected-Sensitive', 'Infected-Insensitive']
colors = ['w', 'b', 'g', 'y', 'r']

# -------------------------------------------------------------------

for ldval in ld100s:
    for r in range(len(reps)):
        rep = reps[r]
        dir = runname % (ldval, rep)
        target = os.path.join(dir, datadir, file)

        if os.path.exists(target):
            f = gzip.open(target, 'rb')
            reader = csv.reader(f)
            numrows = 0

            for row in reader:
                if len(row) != 6 or row[0] == "#":
                    continue

                numrows += 1
                row = map(int, row)

                if numrows == 1:
                    data = numpy.array(row)
                else:
                    data = numpy.vstack((data,row))
                    
            f.close()

            if r == 0:
                alldata = data
            else:
                alldata = numpy.dstack([alldata, data])
        else:
            print "File %s does not exist.  Skipping" % (target)

    # alldata will be of form [row,col,repicate], so all records in the 1st row, 3rd col would be alldata[0,2,:]
    (nrows, ncols, nreps) = numpy.shape(alldata)

    means = numpy.zeros((nrows, ncols))
    stems = numpy.zeros((nrows, ncols))

    for r in range(nrows):
        for c in range(ncols):
            means[r,c] = numpy.mean(alldata[r,c,:])
            stems[r,c] = numpy.mean(alldata[r,c,:])/ (len(alldata[r,c,:])**(0.5))


    fig = plt.figure()
    title = "LD100=%d" % (ldval)
    plt.title(title)
    plt.xlabel("Time (epoch)")
    plt.ylabel("Density")

    for i in range(2,6):
        plt.plot(means[:,0], means[:,i], label=labels[i-1], color=colors[i-1])

    plt.ylim([0, 100000])
    plt.grid()
    plt.legend()
    figfile = "plots/density-ld100-%02d.pdf" % (ldval)
    plt.savefig(figfile)
