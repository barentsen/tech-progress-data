Data & graphs on the progress of technology
===========================================
***Showing the data behind Moore's law™***

This repository collates and visualizes data sets which demonstrate the increasing trends of computing power, storage capacity, astronomical surveys, etc.  The aim of these graphs is to encourage discussions related to *Moore's law* to be based on data, rather than assumptions or hear-say.  The various sources behind the data points are documented inside the `data` directory of this repository.

## The Graphs

### Computing power

![Supercomputer speeds double every 13 months](https://github.com/barentsen/tech-progress-data/blob/master/graphs/fastest-supercomputer.png)

![CPU transistor counts double every 23 months](https://raw.githubusercontent.com/barentsen/tech-progress-data/master/graphs/transistor-counts.png)

### Storage & I/O

![Internet speeds double every 16 months](https://github.com/barentsen/tech-progress-data/blob/master/graphs/research-internet-speed.png)

![Storage-per-dollar ratios double every 23 months](https://github.com/barentsen/tech-progress-data/blob/master/graphs/disk-drive-price.png)

![Storage bus speeds double every 35 months](https://github.com/barentsen/tech-progress-data/blob/master/graphs/storage-bus-speed.png)

### Astronomical surveys

![Pixel rates of near-infrared astronomy surveys double every 41 months](https://github.com/barentsen/tech-progress-data/blob/master/graphs/telescope-pixel-counts-near-infrared.png)

![Pixel rates of optical astronomical surveys double every 41 months](https://github.com/barentsen/tech-progress-data/blob/master/graphs/telescope-pixel-counts.png)

### Biology

![The cranial capacity of humans doubles every 1.5 million years](https://raw.githubusercontent.com/barentsen/tech-progress-data/master/graphs/cranial-capacity.png)


## Slides
A short presentation using these data is shown here:

https://speakerdeck.com/barentsen/a-3-minute-rant-on-the-deluge-of-data-in-astronomy

## Usage
To create the graphs and fit the exponential trends to all the data sets in this repository, run:

```
python plot_progress.py
```

## Dependencies
* matplotlib
* numpy
* astropy

## Contributing
Additional data sets, or corrections to the existing ones, are welcome. Please open a pull request!

## Authors
 * Geert Barentsen (@barentsen)
 * Josh Peek (@jegpeek)
 * See the `README` files in the sub-directories under `data` for data source credits.

## License
Made available under the MIT License, 
unless otherwise specified in the README files inside the `data` sub-directories.
