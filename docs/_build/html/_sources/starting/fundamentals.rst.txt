.. GrainPy documentation master file, created by
   sphinx-quickstart on Tue Mar 29 20:33:40 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GrainPy Fundamentals
=====================

Data Input
-----------

Grain size distribution data can be obtained from a variety of equipment, including sieves, hydrometers, and laser diffraction particle size analyzers. GrainPy collects and organizes this data, then calculates cumulative percentages and a variety of statistics, however, there are a few basic requirements for the input data structure:

   1. Currently, GrainPy only accepts Excel files (.xlsx or .xls).

   2. Each file contains data for one sample only.

   3. Bins used in the analytical method are located in a column immediately preceding the collected data. 

   4. Bin sizes are in microns.

   5. Bins are arranged from smallest to largest.

   6. Bin sizes represent the lower limit of each interval interval, with a final bin size representing the maximum upper limit included in the study.

   7. Currently, GrainPy can only accept multiple files that use the same bins. 

   8. Optional: files are named according to the sample name. This is completely up to the user, but filenames are used in the titles of plots.



Compiling the Data
-------------------
Given the correct input format, GrainPy can easily collect and organize single or multiple files, and calculate cumulative percentages and a variety of sample statistics.

::

   # list or tuple of complete paths to files
   files = ['path to file 1', ..., 'path to file n']
   
   # compile data from file(s), cumulative proportions, and statistics
   var = GrainSizeDist(files)
   var.data()
   var.datacp()
   var.datast()


.. figure:: https://i.imgur.com/XtCbxh2.png
    :align: center
    :height: 400px
    :figclass: align-center




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

