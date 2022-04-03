.. GrainPy documentation master file, created by
   sphinx-quickstart on Tue Mar 29 20:33:40 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The 'util' Module
=================

The 'util' module provides functionality that is both called within the GrainSizeDist class, and may be of interest to the user. Functions, parameters, and examples are presented below...

selectdata function
--------------------
The *selectdata* function provides a user dialog window to select files to include in a GrainSizeDist object. This provides a user-friendly option to select single or multiple Excel files (.xlsx or .xls), save a list of paths to the selected files, then can be used as a parameter for creating a GrainSizeDist object.

For example...

::

   # call the function with no parameters, select the file(s) using your mouse and the user dialog window that opens, and click 'ok'
   files = selectdata()
   # the variable 'files' is a list of paths that can then be input as a parameter in a GrainSizeDist object
   files
   

datacheck function
--------------------
The most common problem with input data is bin sizes are not consistent in all files. For example, one bin may be 0.375198, but some files may have been rounded inadvertently to 0.37520). The *datacheck* function checks the smallest expected bin value input as a function parameter by the user, displays the results of the datacheck, and offers the option to automatically fix the problematic files by changing them, or let's the user manually examing the file(s) themselves. We warn the user that the auto-fix solution is permanent and changes the original files!

::

   # call the function using the "files" variable created above. 
   # min_bin and bin_rows have default values of 0.375198 and 93 by default, but may be changed accordingly by the user
   datacheck(files)
   

df_ex and gems_ex functions
----------------------------
The df_ex and gems_ex functions afford the user the option to export GrainSizeDist object information as tables (.csv or .xlsx). The df_ex function exports the data as it is displayed in GrainPy. The gems_ex function exports the data in a transposed data format, along with a few basic statistics and blank fields.

::

   # exporting cumulative proportions and statistics from GrainSizeDist object named gsd
   # exporting cumulative proportion data followed by statistics
   df_ex(gsd.datacp())
   df_ex(gsd.datast())
   
   # using the gems_ex function...
   gems_ex(gsd)
   
   # df_ex requires a dataframe parameter, but gems_ex requires a GrainSizeDist object!


