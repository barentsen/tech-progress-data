#!/usr/bin/env python
"""Graphs the progress of various technologies."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
__author__ = "Geert Barentsen"

import os
import numpy as np
import pylab as plt
import logging
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
    labelcolumn = None
    xlim, ylim = None, None

    def __init__(self, filename=None):
        # Read the data
        if filename == None:
            filename = os.path.join(DATADIR, self.prefix, self.prefix+'.csv')
        self.table = Table.read(filename, format='ascii')
        self.xdata = self.table[self.xcolumn]
        self.ydata = self.table[self.ycolumn]
        
    def trendfit(self):
        # Fit the exponential trend
        return np.polyfit(self.xdata, np.log10(self.ydata), 1)

    def plot(self, trendfit=True, title=True):
        self.fig = plt.figure(figsize=(8, 5))
        self.ax = plt.subplot(111)
        self.ax.set_yscale("log")
        self.ax.scatter(self.xdata,
                        self.ydata, 
                        facecolor=RED,
                        s=70,
                        linewidth=1,
                        edgecolor='black')

        # Show labels next to the data points
        if self.labelcolumn:
            labels = self.table[self.labelcolumn]
            for i in range(len(labels)):
                plt.text(self.xdata[i] + 0.6, self.ydata[i], labels[i],
                ha="left",
                va="center",
                fontsize=14,
                backgroundcolor="#f6f6f6")

        if trendfit:
            self.ax.plot(self.xdata, 10**np.polyval(self.trendfit(), self.xdata),
                         c=BLUE, lw=2, alpha=0.5, zorder=-10)
            if title:
                self.ax.text(0.05, 0.95,
                             '{0}\ndouble every {1:.0f} months'.format(
                                                    self.title,
                                                    self.get_doubling_time()),
                             va='top',
                             transform=self.ax.transAxes,
                             fontsize=18)

        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        
        if self.xlim:
            self.ax.set_xlim(self.xlim)
        if self.ylim:
            self.ax.set_ylim(self.ylim)
        
        # Aesthetics
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["top"].set_visible(False)
        self.ax.get_xaxis().tick_bottom()
        self.ax.get_yaxis().tick_left()
        self.fig.tight_layout()
        return self.fig

    def get_doubling_time(self):
        """Returns number of months it takes for the y-axis data to double."""
        doubling_time = 12 * np.log10(2) / self.trendfit()[0]
        logging.info("{0} doubles every {1:.2f} months".format(self.prefix, doubling_time))
        return doubling_time

    def get_annual_increase(self):
        """Returns the percentage increase per year."""
        annual_fractional_increase = 100 * (10**self.trendfit()[0]) - 100
        logging.info("{0} increases by {1:.2f} percent each year".format(self.prefix, annual_fractional_increase))
        return annual_fractional_increase


class TransistorCountData(DataSet):
    title = "CPU transistor counts"
    prefix = "transistor-counts"
    xcolumn = "year"
    xlabel = "Year"
    ycolumn = "transistors"
    ylabel = "Transistors"
    xlim = [1965, 2020]

    def plot(self):
        super(TransistorCountData, self).plot()
        # Annotate the era of multi-core processors
        self.ax.plot([2006, 2014], [5e6, 5e6], lw=2.5, c='black')
        self.ax.text(2010, 1.7e6, "Multi-core", fontsize=15, ha="center")
        return self.fig


class DiskDrivePriceData(DataSet):
    title = "Storage per dollar ratios"
    prefix = "disk-drive-price"
    xcolumn = "year"
    xlabel = "Year"
    ycolumn = "size_mb"
    ylabel = "MB per dollar"

    def __init__(self):
        super(DiskDrivePriceData, self).__init__()
        self.ydata = self.table['size_mb'] / self.table['cost_usd']


class SupercomputerSpeedData(DataSet):
    title = "Supercomputer speeds"
    prefix = "fastest-supercomputer"
    xcolumn = "year"
    xlabel = "Year"
    ycolumn = "flops"
    ylabel = "FLOPS"


class ResearchInternetSpeedData(DataSet):
    title = "Internet speeds"
    prefix = "research-internet-speed"
    xcolumn = "year"
    xlabel = "Year"
    ycolumn = "bps"
    ylabel = "Bits/s"


class StorageBusSpeedData(DataSet):
    title = "Storage bus speeds"
    prefix = "storage-bus-speed"
    xcolumn = "year"
    xlabel = "Year"
    ycolumn = "bps"
    ylabel = "Bits/s"
    labelcolumn = "name"
    xlim = [1980, 2020]


class TelescopePixelCountsData(DataSet):
    title = "Pixel rates of optical surveys"
    prefix = "telescope-pixel-counts"
    xcolumn = "year"
    xlabel = "Start of science"
    ycolumn = "pixels"
    ylabel = "Pixels/s"
    labelcolumn = "name"
    xlim = [1998, 2025]

    def __init__(self):
        super(TelescopePixelCountsData, self).__init__()
        self.ydata = self.table['pixels'] / self.table['cycle_time']


class TelescopePixelCountsInfraredData(DataSet):
    title = "Pixel rates of near-infrared surveys"
    prefix = "telescope-pixel-counts-near-infrared"
    xcolumn = "year"
    xlabel = "Start of science"
    ycolumn = "pixels"
    ylabel = "Pixels/s"
    labelcolumn = "name"
    #xlim = [1998, 2025]

    def __init__(self):
        super(TelescopePixelCountsInfraredData, self).__init__()
        self.ydata = self.table['pixels'] / self.table['cycle_time']


if __name__ == '__main__':
    """Create graphs for all datasets in the repository."""
    DESTINATION_DIR = 'graphs'
    datasets = [DiskDrivePriceData(),
                SupercomputerSpeedData(),
                ResearchInternetSpeedData(),
                StorageBusSpeedData(),
                TelescopePixelCountsData(),
                TelescopePixelCountsInfraredData(),
                TransistorCountData()]
    for ds in datasets:
        for extension in ['png', 'pdf']:
            output_filename = os.path.join(DESTINATION_DIR,
                                           ds.prefix+'.'+extension)
            ds.plot().savefig(output_filename, dpi=200)