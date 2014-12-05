tech-progress-data
==================

Description
-----------
This repository aims to collate data on the technological process of microprocessors, networks, telescopes, etc.

Usage
-----
Create a plot illustrating the evolution of transistor counts in microprocessors (i.e. Moore's law):

    ```Python
    import plot_progress
    mydata = plot_progress.TransistorCountData()
    mydata.get_plot().show()
    ```

License
-------
Made available under the MIT License. For details see the LICENSE file.
