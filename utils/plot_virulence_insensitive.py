#!/usr/bin/env python

import csv
import os
import numpy
import gzip
import re

import matplotlib.pyplot as plt

# -------------------------------------------------------------------
runname = "ld100-%02d-novtrans_%d"
datadir = "data"
file = "virulence.dat.gz"
reps = range(400,403)
ld100s = [1,5,10,15,20,25,30,35,40,45,50]
ld100s = [1,10,20,30,40,50]
colors = ['w', 'b', 'g', 'y', 'r']
# -------------------------------------------------------------------

fig = plt.figure()

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
                if len(row) != 5:
                    continue
                elif re.match('^\s*#', row[0]) != None:
                    continue


                numrows += 1

                row = map(float, row)

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

    label = "ld100=%3.1f" % (ldval)
    #plt.errorbar(means[:,0], means[:,3], yerr=stems[:,3], label=label)
    plt.plot(means[:,0], means[:,3], label=label)


plt.grid()
plt.title("Virulence of Insensitive Parasites")
plt.xlabel("Time (epoch)")
plt.ylabel("Virulence")
plt.legend()
plt.savefig("plots/virulence-insensitive.pdf")
