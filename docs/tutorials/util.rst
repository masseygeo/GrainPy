.. GrainPy documentation master file, created by
   sphinx-quickstart on Tue Mar 29 20:33:40 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The 'util' Module
=================

The **util** module provides functionalities called within the *GrainSizeDist* class, but may also be called individually to the user.

The 'datacheck' Function
-------------------------
The most common problem with input data is bin sizes are not consistent in all files. For example, one bin may be 0.375198, but some files may have been rounded inadvertently to 0.37520). The *datacheck* function checks the smallest expected bin value input as a function parameter by the user, displays the results of the datacheck, and offers the option to automatically fix the problematic files by changing them, or let's the user manually examing the file(s) themselves. We warn the user that the auto-fix solution is permanent and changes the original files!

::

   # call function using "files" variable created above
   # min_bin and bin_rows have default values, but may be changed accordingly by user
   datacheck(files)
   

The 'df_ex' & 'gems_ex' Functions
-----------------------------------
The *df_ex* and *gems_ex* functions afford the user the option to export *GrainSizeDist* object data as tables (.csv or .xlsx). 

The *df_ex* function requires a **dataframe** parameter, then saves that dataframe according to the chosen location/name from the interactive user-dialog window. Dataframes include returns of the *bins*\, *data*\ , *datacp*\, or *datast* methods, or any other type of non-GrainPy dataframe.

The *gems_ex* function requires a **GrainSizeDist** object parameter, then saves the data and selected statistics in a transposed format to a location/name from the interactive user-dialog window.

::

   # df_ex function
   # first export cumulative proportion dataframe
   df_ex(gsd.datacp())
   
   # then statistics dataframe from a GrainSizeDist object named 'gsd'
   df_ex(gsd.datast())
   
   # gems_ex function with a GrainSizeDist object named 'gsd'
   gems_ex(gsd)
   

The 'selectdata' Function
--------------------------
The *selectdata* function provides an interactive user dialog window to manually select file(s). This provides a user-friendly option to select single or multiple Excel files (.xlsx or .xls), save a list of paths to the selected files, then can be used as a parameter for creating a GrainSizeDist object.

::

   # selectdata function, call function then select file(s) using dialog window
   files = selectdata()
   files
   

