.. GrainPy documentation master file, created by
   sphinx-quickstart on Tue Mar 29 20:33:40 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The 'classify' Module
=====================

The 'classify' module contains functions to convert numerical statistics of grain size analyses into various qualitative classifcations. These functions are called within the GrainSizeDist class, but can also be used by the user for quick references.

The 'wentworth_gs' Function
----------------------------
The *wentworth_gs* function converts grain sizes, in phi units, into the qualitative grain size classification scheme of Wentworth (1922).

::

   wentworth_gs(-1)
   wentworth_gs(3.6)

*  Wentworth, C.K., 1922, A Scale of Grade and Class Terms for Clastic Sediments: Journal of Geology, Volume 30, Number 5, DOI: https://doi.org/10.1086/622910.

The 'folk_sed' Function
------------------------
The *folk_sed* function classifies sand, silt, and clay proportions into the qualitative sediment classification scheme of Folk (1954).

::

   folk_sed(20, 20, 60)
   folk_sed(2.5, 90.2, 7.3)

*  Folk, R.L., 1954, The Distinction between Grain Size and Mineral Composition in Sedimentary-Rock Nomenclature: Journal of Geology, Volume 62, Number 4, DOI: https://doi.org/10.1086/626171.

The 'folk_sort', 'folk_skew', & 'folk_kurt' Functions
-------------------------------------------------------
The *folk_sort*, *folk_skew*, and *folk_kurt* functions classify sediment sorting, and skewness and kurtosis of grain size distributions according to the classification of Folk and Ward (1957).

::

   folk_sort(1.35)
   folk_skew(0.12)
   folk_kurt(0.96)
   
*  Folk, R.L., and Ward, W.C., 1957, Brazos River bar: a study in the significance of grain size parameters: Journal of Sedimentary Petrology, Volume 27, Number 1, DOI: https://doi.org/10.1306/74D70646-2B21-11D7-8648000102C1865D.


