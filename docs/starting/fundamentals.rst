.. GrainPy documentation master file, created by
   sphinx-quickstart on Tue Mar 29 20:33:40 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GrainPy Fundamentals
=====================

Data Input
-----------

Grain size distribution data can be obtained from a variety of equipment, including sieves, hydrometers, and laser diffraction particle size analyzers, however, there are a few basic requirements for the input data structure in order to utilize GrainPy:

   1. Grain size distribution data must be an Excel file (.xlsx or .xls).

   2. Each file contains data for one sample only.

   3. Bins used in the user's methodology are located in a column immediately preceding the data collected. 

   4. Bin sizes are in microns.

   5. Bins are arranged from smallest to largest.

   6. Bins represent the lower limit of each grain size interval, and the last row contains the maximum *UPPER* limit (therefore there is one more row of bins than data.


Compiling the Data
-------------------
Given the correct input format, GrainPy can easily collect and organize single or multiple files, and calculate cumulative percentages and a variety of sample statistics.

::

   # list or tuple of complete paths to files
   files = ['path to file 1', ..., 'path to file n']
   
   # compile data, cumulative proportions, and statistics from file(s)
   var = GrainSizeDist(files)
   var.data()
   var.datacp()
   var.datast()


.. figure:: https://i.imgur.com/XtCbxh2.png
    :align: center
    :height: 400px
    :figclass: align-center

The figures above show an example of three Excel files on the left, with bins in one column and data in the following column. After these files have been input into GrainPy, the user can see the compiled data, cumulative percentages, and data statistics as shown on the right.




Visualizing the Data
---------------------

Data can then be visualized and interpreted with publication-quality grain size distribution plots.

::

   # plots of individual files
   var.gsd_single()
   
   # plot of all files
   var.gsd_multi()


.. figure:: https://i.imgur.com/ZFmjpiz.png
    :align: center
    :height: 400px
    :figclass: align-center

The two figures above show a GrainPy plot for a single sample (left) and multiple samples (right). The single sample plot shows a histogram of relative proportions within each bin, a cumulative proportion curve, mean, median, and mode(s) of the sample (vertical lines), and selected statistics below the plot. The multiple sample plot shows cumulative proportion curves for all samples (black lines), the mean cumulative proportion curve (dark red lines), and a 95% confidence interval of the mean (translucent red polygon). GrainPy has multiple options for plots, which are discussed in detail in the `Plotting <https://grainpy.readthedocs.io/en/latest/tutorials/plots.html>`_ section.
