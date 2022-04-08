.. GrainPy documentation master file, created by
   sphinx-quickstart on Tue Mar 29 20:33:40 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The 'grainsize' Module
===========================

The **grainsize** module contains the *GrainSizeDist* class, which is the fundamental GrainPy object. The *GrainSizeDist* object contains a variety of attributes and methods to aid the user with data compilation and visualization. 


'path' Attribute
^^^^^^^^^^^^^^^^^^^^^
The *path* attribute is the only required parameter for creating a *GrainSizeDist* object, and consists of either a list or tuple of path(s) for the file(s) containing the grain size distribution data. This parameter can be input manually, or interactively using the *selectdata* function from the `**util** module <https://grainpy.readthedocs.io/en/latest/tutorials/util.html>`_.

::

   # selectdata function opens a user dialog window to select files interactively
   files = selectdata()
   
   # create a new instance of the GrainSizeDist class with the selected files
   var = GrainSizeDist(files)


'lith' & 'area' Attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The *lith* and *area* attributes are optional. Their intent is to provide a means to differentiate GrainSizeDist objects by lithology and/or location. Currently, this is only used for grain size distribution plot titles.

::

   # using the path attribute to indicate all samples are of alluvium lithology
   var = GrainSizeDist(files, ltih='alluvium')
   
   # alternatively, can assign attribute anytime after instantiation
   var = GrainSizeDist(files)
   var.lith = 'alluvium'

   # using the area attribute to indicate all samples are located in Lebanon Junction
   var = GrainSizeDist(files, area='Lebanon Junction')
   
   # using both *lith* and *path*
   var = GrainSizeDist(files, lith='alluvium', area='Lebanon Junction')


'samplenames' Method
^^^^^^^^^^^^^^^^^^^^^^^^^
The *samplenames* method assumes that the base file names represent the sample names and are unique. Both of these assumptions are not strictly required, but are used in other methods of the GrainSizeDist class, as well as in plot titles.

::

   # using the instance of GrainSizeDist class created above
   var.samplenames()


'bins' Method
^^^^^^^^^^^^^^^^^^
The *bins* method assumes that the orignal files have bins input in microns, and the bin intervals are the same in all file(s) selected and input for the GrainSizeDist instance. The method returns a Pandas dataframe of the bin intervals in phi units, microns, and millimaters.

::

   # using the instance of GrainSizeDist class created above
   var.bins()


'data' Method
^^^^^^^^^^^^^^^^
The *data* method returns a Pandas dataframe of the raw data for all file(s) selected and input for the GrainSizeDist instance. 

::

   # using the instance of GrainSizeDist class created above
   var.data()

*Note: if the minimum bin value is not consistent in all input file paths, then this method will raise an error.*


'datacp' Method
^^^^^^^^^^^^^^^^
The *datacp* method returns a Pandas dataframe of the cumulative proportions for all file(s) selected and input for the GrainSizeDist instance. 

::

   # using the instance of GrainSizeDist class created above
   var.datacp()


'datast' Method
^^^^^^^^^^^^^^^^
The *datast* method returns a Pandas dataframe of the statistics calculated from the data and cumulative proportions for all file(s) selected and input for the GrainSizeDist instance. 

::

   # using the instance of GrainSizeDist class created above
   var.datast()


'gsd_single' Method
^^^^^^^^^^^^^^^^^^^^
The *gsd_single* method creates two image files (.pdf and .jpg) grain size distributions of either:
1. each file(s) selected and input for the GrainSizeDist instance (default)
2. a list of user-selected sample names (basenames of files) using the parameter *files*
3. indices of user-selected 'slice' of GrainSizeDist.path list

::

   # grain size distribution plots of all samples included in GrainSizeDist instance
   var.gsd_single()
   
   # grain size distribution plots of two samples, 'file 1' and 'file 7' included in GrainSizeDist instance
   var.gsd_single(files=['file 1', 'file 7'])
   
   # grain size distribution plots of first three samples included in GrainSizeDist instance
   var.gsd_single(i=0, j=3)


'gsd_multi' Method
^^^^^^^^^^^^^^^^^^^
The *gsd_multi* method creates two image files (.pdf and .jpg) of:
1. Cumulative proportion curves of all files, with mean and 95% confidence interval (default)
2. Mean cumulative proportion curve with 95% confidence interval, and mean grain size distributions per bin
3. Grain size distributions per bin (as curve), mean grain size distribution per bin (as histogram), and 95% confidence interval

Selected statistics and confidence intervals are included in each plot by default, but can be disabled with the boolean parameters *stplt=False* and *ci=False*

::

   # option 1, default; using instance "var" of GrainSizeDist class created above
   var.gsd_multi()
   
   # option 2, with no statistics included
   var.gsd_multi(bplt=True, stplt=False)
   
   # option 3, with no statistics and no confidence interval
   var.gsd_multi(bplt=True, cplt=False, ci=False)
