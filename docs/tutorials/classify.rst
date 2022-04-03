.. GrainPy documentation master file, created by
   sphinx-quickstart on Tue Mar 29 20:33:40 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The 'classify' Module
=====================

The 'classify' module contains functions to convert numerical statistics of grain size analyses into various qualitative classifcations. These functions are called within the GrainSizeDist class, but can also be used by the user for quick references.

wentworth_gs function
----------------------
The *wentworth_gs* function converts grain sizes, in phi units, into the qualitative grain size classification scheme of Wentworth (1922).

::

   wentworth_gs(-1)
   wentworth_gs(3.6)
   wentworth_gs(11.21)

*  Wentworth, C.K., 1922, A Scale of Grade and Class Terms for Clastic Sediments: Journal of Geology, Volume 30, Number 5, DOI: https://doi.org/10.1086/622910

folk_sed function
------------------
The *folk_sed* function classifies sand, silt, and clay proportions into the qualitative sediment classification scheme of Folk (19XX)

folk_sort, folk_skew, & folk_kurt functions
--------------------------------------------



