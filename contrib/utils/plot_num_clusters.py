#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Produce plots (using matplotlib) from data written by the SEEDS
PrintPopulationTypeClusters action.  This can either be used as a command-line
tool or by importing and calling the plot_num_clusters function.

Dependencies:
    - Python 2.7 or greater
    - Matplotlib
    - Numpy
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0"
__credits__ = "Brian Connelly"

import argparse
import csv
import numpy
import re
import string
import sys

import matplotlib.pyplot as plt

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0"


def plot_num_clusters(file, outfile='num_clusters.pdf', title=None, grid=False, epochs=[],
                      labels=[]):
    reader = csv.reader(file)
    rownum = 0
    data_read = False

    for row in reader:
        # Skip commented lines
        if re.match('^\s*#', row[0]) != None:
            continue

        rownum += 1

        if rownum == 1:
            colnames = row[1:]

            for i in range(len(colnames)):
                colnames[i] = re.sub('_', ' ', colnames[i])

            continue
        else:
            row = list(map(float, row))

            if (len(epochs) == 0 or row[0] in epochs):
                if data_read:
                    data = numpy.vstack((data,row))
                else:
                    data = numpy.array(row)
                    data_read = True

    if data_read:
        fig = plt.figure()

        if len(labels) > 0 and len(labels) == len(colnames):
            colnames = labels

        plot_cols = list(range(1, data.shape[1], 3))

        # Plot the number of clusters
        for t in plot_cols:
            plt.errorbar(data[:,0], data[:,t], yerr=None, xerr=None, label=string.capitalize(colnames[t-1]))

        if grid:
            plt.grid()

        plt.xlabel("Time (epoch)")
        plt.ylabel("Clusters")

        if title:
            plt.title(title)

        plt.legend(loc=0)
        plt.savefig(outfile)
    else:
        print("Could not generate plot: No data match given parameters")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot population densities created from the PrintCellTypeCount SEEDS Action')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-e', '--epochs', action='store', default=[], nargs='+',
                        help='epochs for which to show data (default: all)')
    parser.add_argument('-g', '--grid', action='store_true', help='show a grid (default: False)')
    parser.add_argument('-o', '--outfile', action='store', default="num_clusters.pdf",
                        help='name of generated plot (default: num_clusters.pdf)')
    parser.add_argument('-l', '--labels', action='store', nargs='+', default=[],
                        help='list of labels for each cell type (default: use data file)')
    parser.add_argument('-t', '--title', action='store', default=None,
                        help='title of the plot (default: no title)')
    parser.add_argument('-v', '--version', action='version', version=__version__,
                        help='display version information and exit')
    args = parser.parse_args()

    epochs = []
    if len(args.epochs) > 0:
        for r in args.epochs:
            m = re.match(r"^\s*(?P<start>\d+)\-(?P<end>\d+)\s*$", r)
            if m != None:
                epochs += list(range(int(m.group("start")), int(m.group("end"))+1))

            m = re.match(r"^\s*(?P<value>\d+)\s*$", r)
            if m != None:
                epochs.append(int(m.group("value")))

    # Sort the list and remove duplicates
    epochs.sort()
    s = set(epochs)
    epochs = []
    [epochs.append(i) for i in s]

    plot_num_clusters(file=args.infile, outfile=args.outfile, title=args.title,
                      grid=args.grid, epochs=epochs, labels=args.labels)

