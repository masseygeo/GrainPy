.. GrainPy documentation master file, created by
   sphinx-quickstart on Tue Mar 29 20:33:40 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The 'grainsize' Module
===========================

The **grainsize** module contains the *GrainSizeDist* class, which is the fundamental GrainPy object. The *GrainSizeDist* object contains a variety of attributes and methods to aid the user with data compilation and visualization. 


'path' Attribute
^^^^^^^^^^^^^^^^^^^^^
The *path* attribute is the only reqquirement for creating a *GrainSizeDist* object, and consists of either a list or tuple of path(s) for the file(s) containing the grain size distribution data. This parameter can be input manually, or interactively using the *selectdata* function from the `util module <https://grainpy.readthedocs.io/en/latest/tutorials/util.html>`_.

::

   # selectdata function opens a user dialog window to select files interactively
   files = selectdata()
   
   # create a new instance of the GrainSizeDist class with the selected files
   var = GrainSizeDist(files)


'lith' & 'area' Attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The *lith* and *area* attributes are optional. Their intent is to provide a means to differentiate GrainSizeDist objects by lithology and/or location. Currently, this is only used for grain size distribution plot titles.

::

   # using GrainSizeDist instance from above, assign attributes after instantiation
   var.lith = 'alluvium'
   var.area = 'Lebanon Junction'
   
   # alternatively, assign attributes at time of instantiation
   var = GrainSizeDist(files, lith='alluvium', area='Lebanon Junction')


'samplenames' Method
^^^^^^^^^^^^^^^^^^^^^^^^^
The *samplenames* method assumes that the input file names represent the sample names and are unique. Both of these assumptions are not strictly required, but are used in other methods of the GrainSizeDist class, as well as in plot titles. Calling the *samplenames* method returns a list of the assumed sample names.

::

   # using the GrainSizeDist instance from above
   var.samplenames()


'bins' Method
^^^^^^^^^^^^^^^^^^
The *bins* method returns a dataframe of the bin intervals in phi units, microns, and millimaters.

::

   # using the GrainSizeDist instance from above
   var.bins()


'data' Method
^^^^^^^^^^^^^^^^
The *data* method returns a dataframe of the grain size distribution data compiled for all file(s) selected and input for a *GrainSizeDist* object. 

::

   # using the GrainSizeDist instance from above
   var.data()


'datacp' Method
^^^^^^^^^^^^^^^^
The *datacp* method returns a dataframe of the cumulative proportions compiled for all file(s) selected and input for a *GrainSizeDist* object. 

::

   # using the GrainSizeDist instance from above
   var.datacp()


'datast' Method
^^^^^^^^^^^^^^^^
The *datast* method returns a dataframe of statistics calculated from the data and cumulative proportions for all file(s) selected and input for a *GrainSizeDist* object. 

::

   # using the GrainSizeDist instance from above
   var.datast()


'gsd_single' Method
^^^^^^^^^^^^^^^^^^^^
The *gsd_single* method saves two image files of grain size distribution plots (.pdf and .jpg) in the directory where the sample files are located. The default for this method is to plot all samples, however, the user has the option to manually select sample(s) by either:

1. manually inputting a list of sample names using the *files* parameter
2. defining indices of a 'slice' from the *path* attribute using the *i* and *j* parameters

::

   # grain size distribution plots of all samples
   var.gsd_single()
   
   # grain size distribution plots of two samples, 'file 1' and 'file 7'
   var.gsd_single(files=['file 1', 'file 7'])
   
   # grain size distribution plots of first three samples included in a *GrainSizeDist* object
   var.gsd_single(i=0, j=3)


'gsd_multi' Method
^^^^^^^^^^^^^^^^^^^
The *gsd_multi* method saves two image files of grain size distribution plots (.pdf and .jpg) of multiple samples in the directory where the sample files are located. There are three plot options (1-3) and two additional options (4-5) to customize each plot according to user specifications:

1. Cumulative proportion curves of all files, with mean and 95% confidence interval. This is the default with parameters *bplt* = False, *cplt* = True, *stplt* = True, and *ci* = True.
2. Mean cumulative proportion curve with 95% confidence interval, and histogram of mean grain size distributions using the *bplt* parameter.
3. Histogram of mean grain size distribution per bin with 95% confidence interval, and grain size distributions per bin for each sample (as curves) using the *bplt* and *cplt* parameters.
4. Plotting mean, median, and modes, and selected statistics of mean in plot legend using the *stplt* parameter.
5. Plotting the 95% confidence interval using the *ci* parameter.

::

   # option 1, default
   var.gsd_multi()
   
   # options 2 and 4
   var.gsd_multi(bplt=True, stplt=False)
   
   # options 3 and 5
   var.gsd_multi(bplt=True, cplt=False, ci=False)
