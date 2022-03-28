# -*- coding: utf-8 -*-
"""
This module contains functions used to classify grain sizes and distributions in terms of commonly accepted descriptive classifications, including those from Folk and Ward (1957), Folk (1954, 1966, 1972), and Wentworth (1922).


--------------------------------------
Copyright 2021-2022 Matthew A. Massey

This file is part of GrainPy.

GrainPy is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. GrainPy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with GrainPy. If not, see <https://www.gnu.org/licenses/>. 
"""


__all__ = [
    "wentworth_gs",
    "folk_sed",
    "folk_sort",
    "folk_skew",
    "folk_kurt",
]


import numpy as np


def wentworth_gs(phi):
    """
    Convert grain size in phi units to qualitative Wentworth classification name.

    Parameters
    ----------
    phi : integer or float
        grain size in phi units

    Returns
    -------
    gs : string
        text description of grain size

    """

    if -1 <= phi < 0:
        gs = 'very coarse sand'
    elif 0 <= phi < 1:
        gs = 'coarse sand'
    elif 1 <= phi < 2:
        gs = 'medium sand'
    elif 2 <= phi < 3:
        gs = 'fine sand'
    elif 3 <= phi < 4:
        gs = 'very fine sand'
    elif 4 <= phi < 5:
        gs = 'coarse silt'
    elif 5 <= phi < 6:
        gs = 'medium silt'
    elif 6 <= phi < 7:
        gs = 'fine silt'
    elif 7 <= phi < 8:
        gs = 'very fine silt'
    elif 8 <= phi:
        gs = 'clay'
    else:
        gs = np.nan

    return gs


def folk_sed(sand, silt, clay):
    """
    Convert relative sand-silt-clay percentages to qualitative Folk (1954, 1972) sediment classiciation name.

    Parameters
    ----------
    sand : integer or float
        percentage of total sand
    silt : integer or float
        percentage of total silt
    clay : integer or float
        percentage of total clay

    Returns
    -------
    sed : string
        text description of sediment

    """
    if sand >= 90:
        sed = 'sand'
    elif 50 <= sand < 90:
        if silt/clay >= 2:
            sed = 'silty sand'
        elif clay/silt >= 2:
            sed = 'clayey sand'
        else:
            sed = 'muddy sand'
    elif 10 <= sand < 50:
        if silt/clay >= 2:
            sed = 'sandy silt'
        elif clay/silt >= 2:
            sed = 'sandy clay'
        else:
            sed = 'sandy mud'
    elif sand < 10:
        if silt/clay >= 2:
            sed = 'silt'
        elif clay/silt >= 2:
            sed = 'clay'
        else:
            sed = 'mud'
    else:
        sed = np.nan

    return sed


def folk_sort(sorting):
    """
    Convert inclusive graphic standard deviation of grain size distribution to qualitative Folk and Ward (1957) classiciation name for sorting.

    Parameters
    ----------
    sorting : integer or float
        inclusive graphic standard deviation in phi units 

    Returns
    -------
    sort : string
        text description of sorting

    """
    if sorting <= 0.35:
        sort = 'very well sorted'
    elif 0.35 < sorting <= 0.5:
        sort = 'well sorted'
    elif 0.5 < sorting <= 0.71:
        sort = 'moderately well sorted'
    elif 0.71 < sorting <= 1.0:
        sort = 'moderately sorted'
    elif 1.0 < sorting <= 2.0:
        sort = 'poorly sorted'
    elif 2.0 < sorting <= 4.0:
        sort = 'very poorly sorted'
    elif 4.0 < sorting:
        sort = 'extremely poorly sorted'
    else:
        sort = np.nan

    return sort


def folk_skew(skewness):
    """
    Convert inclusive graphic skewness of grain size distribution curve to qualitative Folk and Ward (1957) classification name for skewness.

    Parameters
    ----------
    skewness : integer or float
        inclusive graphic skewness value

    Returns
    -------
    skew : string
        text description of skewness

    """
    if 0.3 < skewness <= 1:
        skew = 'strongly coarse skewed'
    elif 0.1 < skewness <= 0.3:
        skew = 'coarse skewed'
    elif -0.1 <= skewness <= 0.1:
        skew = 'near symmetrical'
    elif -0.3 <= skewness < -0.1:
        skew = 'fine skewed'
    elif -1.0 <= skewness < -0.1:
        skew = 'strongly fine skewed'
    else:
        skew = np.nan

    return skew


def folk_kurt(kurtosis):
    """
    Convert inclusive graphic kurtosis of grain size distribution curve to qualitative Folk and Ward (1957) classification name for kurtosis.

    Parameters
    ----------
    kurtosis : integer or float
        inclusive graphic kurtosis value

    Returns
    -------
    kurt : string
        text description of kurtosis

    """
    if 0.41 <= kurtosis <= 0.67:
        kurt = 'very platykurtic'
    elif 0.67 < kurtosis <= 0.9:
        kurt = 'platykurtic'
    elif 0.9 < kurtosis <= 1.10:
        kurt = 'mesokurtic'
    elif 1.10 < kurtosis <= 1.5:
        kurt = 'leptokurtic'
    elif 1.5 < kurtosis <= 3.0:
        kurt = 'very leptokurtic'
    elif 3.0 < kurtosis:
        kurt = 'extremely leptokurtic'
    else:
        kurt = np.nan

    return kurt
