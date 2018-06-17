#!/usr/bin/env python
"""Graphs the progress of various technologies."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
__author__ = "Geert Barentsen"

import os
import numpy as np
import pylab as plt
import matplotlib.ticker as ticker

from astropy.table import Table
from astropy import log


###########
# Constants
###########

DATADIR = "data"
RED = "#e74c3c"
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
                fontsize=16,
                backgroundcolor="#f6f6f6")

        if trendfit:
            self.ax.plot(self.xdata, 10**np.polyval(self.trendfit(), self.xdata),
                         color=BLUE, lw=2, alpha=0.5, zorder=-10)
            if title:
                """
                self.ax.text(0.05, 0.95,
                             '{0}\n{1}'.format(self.title,
                                               self.get_doubling_text()),
                             va='top',
                             transform=self.ax.transAxes,
                             fontsize=18)
                """
                
                if 'ranial' in self.ylabel:
                    self.ax.text(0.05, 0.95,
                                 "+{:.5f}% per year".format(self.get_annual_increase()),
                                 va='top',
                                 ha='left',
                                 transform=self.ax.transAxes,
                                 fontsize=18)
                else:
                    self.ax.text(0.05, 0.95,
                                 "+{:.0f}% per year".format(self.get_annual_increase()),
                                 va='top',
                                 ha='left',
                                 transform=self.ax.transAxes,
                                 fontsize=18)

        self.ax.set_xlabel(self.xlabel, fontsize=18)
        self.ax.set_ylabel(self.ylabel, fontsize=18)
        
        if self.xlim:
            self.ax.set_xlim(self.xlim)
        if self.ylim:
            self.ax.set_ylim(self.ylim)

        self.ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))
        
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
        return doubling_time
        
    def get_doubling_text(self):
        return "double every {:.0f} months".format(self.get_doubling_time())

    def get_annual_increase(self):
        """Returns the percentage increase per year."""
        annual_fractional_increase = 100 * (10**self.trendfit()[0]) - 100
        log.info("{0} increases by {1:.2f} percent each year".format(self.prefix, annual_fractional_increase))
        return annual_fractional_increase

    def get_prediction(self):
        """Returns the increase after 22 years."""
        myfit = self.trendfit()
        predict = 10**np.polyval(self.trendfit(), [2000, 2022])
        increase = predict[1] / predict[0]
        return "{0}: increased {1:.0f}x between 2000 and 2022".format(self.prefix, increase)


class TransistorCountData(DataSet):
    title = "CPU transistor counts"
    prefix = "transistor-counts"
    xcolumn = "year"
    xlabel = "Year"
    ycolumn = "transistors"
    ylabel = "Transistors"
    xlim = [1965, 2020]

    def plot(self, **kwargs):
        super(TransistorCountData, self).plot(**kwargs)
        # Annotate the era of multi-core processors
        self.ax.plot([2006, 2018], [5e6, 5e6], lw=2.5, color='black')
        self.ax.text(2012, 1.7e6, "Multi-core era", fontsize=15, ha="center")
        return self.fig


class DiskDrivePriceData(DataSet):
    title = "Storage per dollar ratios"
    prefix = "disk-drive-price"
    xcolumn = "year"
    xlabel = "Year"
    ycolumn = "size_mb"
    ylabel = "MB per dollar"
    xlim = [1999, 2019]

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
    xlim = [1991, 2018]


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
    title = "Pixel rates of large optical surveys"
    prefix = "telescope-pixel-counts"
    xcolumn = "year"
    xlabel = "Start of science"
    ycolumn = "pixels"
    ylabel = "Pixels/s"
    labelcolumn = "name"
    xlim = [1998, 2026]

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


class SpacePhotometryData(DataSet):
    title = "Pixel rates of NASA's photometry missions"
    prefix = "space-photometry-missions"
    xcolumn = "year"
    xlabel = "Launch"
    ycolumn = "pixels_per_second"
    ylabel = "Telemetered pixels"
    labelcolumn = "name"
    xlim = [2006, 2029]


class IAUMembers(DataSet):
    title = "Number of IAU members"
    prefix = "iau-members"
    xcolumn = "year"
    xlabel = "Year"
    ycolumn = "iau_members"
    ylabel = "Members"


class CranialCapacityData(DataSet):
    title = "The cranial capacity of humans"
    prefix = "cranial-capacity"
    xcolumn = "year"
    xlabel = "Million years BC"
    ycolumn = "brain_cc"
    ylabel = "Cranial capacity [cm³]"
    xlim = [-3.5, 0.1]

    def __init__(self):
        super(CranialCapacityData, self).__init__()
        self.xdata = self.table['year'] / 1e6

    def get_doubling_time(self):
        """Returns number of months it takes for the y-axis data to double."""
        doubling_time = np.log10(2) / self.trendfit()[0]
        return doubling_time
        
    def get_doubling_text(self):
        return "doubles every {:.1f} million years".format(self.get_doubling_time())

    def get_annual_increase(self):
        """Returns the percentage increase per year."""
        annual_fractional_increase = 100 * (10**self.trendfit()[0]) - 100
        annual_fractional_increase = annual_fractional_increase / 1e6
        log.info("{0} increases by {1:.2f} percent each year".format(self.prefix, annual_fractional_increase))
        return annual_fractional_increase

if __name__ == '__main__':
    """Create graphs for all datasets in the repository."""
    DESTINATION_DIR = 'graphs'
    datasets = [DiskDrivePriceData(),
                SupercomputerSpeedData(),
                ResearchInternetSpeedData(),
                StorageBusSpeedData(),
                TelescopePixelCountsData(),
                TelescopePixelCountsInfraredData(),
                SpacePhotometryData(),
                IAUMembers(),
                TransistorCountData(),
                CranialCapacityData()]
    datasets = [CranialCapacityData()]
    for ds in datasets:
        for extension in ['png', 'pdf']:
            output_filename = os.path.join(DESTINATION_DIR,
                                           ds.prefix+'.'+extension)
            log.info("Writing {}".format(output_filename))
            ds.plot(title=True).savefig(output_filename, dpi=200)
        #print(ds.get_prediction())