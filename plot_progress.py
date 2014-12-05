#!/usr/bin/env python
"""Module to aid plotting the datasets on technological progress."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
__author__ = "Geert Barentsen"

import os
import pylab as plt
from astropy.table import Table


###########
# Constants
###########

DATADIR = "data"
RED = "#c0392b"
BLUE = "#2c3e50"


#########
# Classes
#########

class DataSet(object):

    xlabel = ""
    ylabel = ""

    def __init__(self, xdata, ydata):
        self.xdata = xdata
        self.ydata = ydata

    def get_plot(self):
        pp = ProgressPlot()
        pp.add_dataset(self)
        return pp


class ProgressPlot(object):

    def __init__(self):
        self.fig = plt.figure()
        self.ax = plt.subplot(111)
        self.ax.set_yscale("log")

    def add_dataset(self, dataset):
        self.ax.scatter(dataset.xdata, dataset.ydata, 
                    lw=1, edgecolor='black',
                    facecolor=BLUE, s=70)

    def show(self):
        plt.show()

    def save(self, filename):
        plt.fig.savefig(filename)


class TransistorCountData(DataSet):

    xlabel = "Transistor count"
    ylabel = "Year of introduction"

    def __init__(self):
        filename = os.path.join(DATADIR, 'transistor-counts', 'transistor-counts.csv')
        self.table = Table.read(filename, format='ascii.csv')
        super(TransistorCountData, self).__init__(self.table['year'], self.table['transistors'])

    def get_plot(self):
        myplot = super(TransistorCountData, self).get_plot()
        # Annotate the era of multi-core processors
        plt.plot([2006, 2014], [5e6, 5e6], lw=2.5, c='black')
        myplot.ax.text(2010, 1.8e6, "Multi-core", fontsize=18, ha="center")
        return myplot


class StorageBusSpeedData(DataSet):

    xlabel = "Bits per second"
    ylabel = "Year"

    def __init__(self):
        filename = os.path.join(DATADIR, 'storage-bus-speed', 'storage-bus-speed.txt')
        self.table = Table.read(filename, format='ascii')
        super(StorageBusSpeedData, self).__init__(self.table['year'], self.table['bits_per_sec'])


class HardDriveCapacityData(DataSet):

    xlabel = "Bytes"
    ylabel = "Year"

    def __init__(self):
        filename = os.path.join(DATADIR, 'hard-drive-capacity', 'hard-drive-capacity.txt')
        self.table = Table.read(filename, format='ascii')
        super(HardDriveCapacityData, self).__init__(self.table['year'], self.table['bytes'])


class TelescopePixelCountsData(DataSet):

    xlabel = "Pixels per second (typical)"
    ylabel = "Start of science"

    def __init__(self):
        filename = os.path.join(DATADIR, 'telescope-pixel-counts', 'telescope-pixel-counts.txt')
        self.table = Table.read(filename, format='ascii')
        pixels_per_sec = self.table['pixels'] / self.table['cycle_time']
        super(TelescopePixelCountsData, self).__init__(self.table['year'], pixels_per_sec)


"""Example: how to create a plot."""
if __name__ == '__main__':
    #tc = TransistorCountData()
    #tc = StorageBusSpeedData()
    tc = TelescopePixelCountsData()
    p = tc.get_plot()
    plt.show()