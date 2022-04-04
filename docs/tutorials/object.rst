.. GrainPy documentation master file, created by
   sphinx-quickstart on Tue Mar 29 20:33:40 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The GrainSizeDist Class
========================

The *GrainSizeDist* class is the fundamental data structure to hold grain size distribution data. Attibutes of the class include, (1) a list or tuple of the path(s) to the file(s) to be included in the instance of the *GrainSizeDist* class; (2) the lithology of the file(s) included in the *GrainSizeDist* class; (3) the area (generalized location) of the file(s) included in the *GrainSizeDist* class. Attribute 1 is required to create a new instance of the *GrainSizeDist* class, while attributes 2 and 3 are optional and, currently, only used for grain size distribution plot titles. Planned functionalities for GrainPy will make more use of attributes 2 and 3.


Attribute: path
^^^^^^^^^^^^^^^^
The *path* attribute is a required parameter to create an instance of the GrainSizeDist class, and consists of either a list or tuple of path(s) to the file(s) of interest. This can be input manually, or interactively using the *selectdata* function from the 'util' module.

::

   # selecting files using the file diaglog windown from the util module
   files = selectdata()
   
   # creating a new instance of the GrainSizeDist class
   var = GrainSizeDist(files)


Attribute: lith
^^^^^^^^^^^^^^^^
The *lith* attribute is optional, but is meant to represent the lithology of the file(s) selected for the GrainSizeDist object. For example, below we are inputting a list of files of samples collected from alluvium:

::

   # creating a new instance of the GrainSizeDist class; all files of alluvium lithology
   var = GrainSizeDist(files, ltih='alluvium')
   
   # alternatively, can assign lith attribute post creation
   var = GrainSizeDist(files)
   var.lith = 'alluvium'


Attribute: area
^^^^^^^^^^^^^^^^
The *area* attribute is also optional, but was originally designed to represent the area (or quadrangle) of a particular set of files selected for a particular GrainSizeDist object. For example, below we are inputting a list of files of samples of collected from the Lebanon Junction 7.5-minute quadrangle:

::

   # creating a new instance of the GrainSizeDist class; all files from the Lebanon Junction quadrangle
   var = GrainSizeDist(files, area='Lebanon Junction')
   
   # alternatively, can assign lith attribute post creation
   var = GrainSizeDist(files)
   var.area = 'Lebanon Junction'


Method: samplenames
^^^^^^^^^^^^^^^^^^^^
The *samplenames* method assumes that the base file names represent the sample names and are unique. Both of these assumptions are not strictly required, but are used in other methods of the GrainSizeDist class, as well as in plot titles.

::

   # using the instance of GrainSizeDist class created above
   var.samplenames()


Method: bins
^^^^^^^^^^^^^^^^
The *bins* method assumes that the orignal files have bins input in microns, and the bin intervals are the same in all file(s) selected and input for the GrainSizeDist instance. The method returns a Pandas dataframe of the bin intervals in phi units, microns, and millimaters.

::

   # using the instance of GrainSizeDist class created above
   var.bins()


Method: data
^^^^^^^^^^^^^^^^
The *data* method returns a Pandas dataframe of the raw data for all file(s) selected and input for the GrainSizeDist instance. 

::

   # using the instance of GrainSizeDist class created above
   var.data()

*Note: if the minimum bin value is not consistent in all input file paths, then this method will raise an error.*


Method: datacp
^^^^^^^^^^^^^^^^
The *datacp* method returns a Pandas dataframe of the cumulative proportions for all file(s) selected and input for the GrainSizeDist instance. 

::

   # using the instance of GrainSizeDist class created above
   var.datacp()


Method: datast
^^^^^^^^^^^^^^^^
The *datast* method returns a Pandas dataframe of the statistics calculated from the data and cumulative proportions for all file(s) selected and input for the GrainSizeDist instance. 

::

   # using the instance of GrainSizeDist class created above
   var.datast()


Method: gsd_single
^^^^^^^^^^^^^^^^^^^
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


Method: gsd_multi
^^^^^^^^^^^^^^^^^^
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
