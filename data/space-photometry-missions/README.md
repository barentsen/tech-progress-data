## How many data points per second do space photometers downlink?

The CSV file in this directory attempts to summarize this question.
It is very difficult to measure the exact science data rate of any given 
mission, so we use very simple assumptions to obtain a ballpark figure.

The assumptions are as follows:

* MOST: assume that MOST, on average, sent back lightcurves for 1 star at a time at ~30 sec cadence. This leads to 0.03 data points per second.
* CoRoT: assume on-board lightcurves for 12,000 targets at 512s cadence plus 10 asteroseismic targets at 2s cadence. This leads to 28.4 data points per second.
* Kepler: assume 3 megapixels at 30 minute cadence plus 20,000 pixels at 1 minute cadence. This leads to 2,000 pixels per second.
* TESS: assume full-frame images (4 x 4096^2 pixels) at 30 minute cadence plus 16,000 targets (11^2 pixels) at 2 minute cadence. This leads to 53,961 pixels per second.
* PLATO: TBC. I don't want to make incorrect assumptions while the mission is being designed.
* WFIRST: Assume 300 megapixels at 15 min cadence.  This leads to 333,333 pixels per second.

Please open an issue if you feel these assumptions mis-represent the amount of science data telemetered from a given mission.

Note that all these missions are fantastic achievements. The telemetered data rates alone do not represent their scientific value; e.g. the scientific content of on-board lightcurves is higher than those of telemetered pixels.
