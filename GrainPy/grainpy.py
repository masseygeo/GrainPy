# -*- coding: utf-8 -*-
"""
Copyright 2021-2022 Matthew A. Massey

This file is part of GrainPy.

GrainPy is free software: you can redistribute it and/or modify it under the terms 
of the GNU General Public License as published by the Free Software Foundation, 
either version 3 of the License, or (at your option) any later version. GrainPy is 
distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without 
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with GrainPy. 
If not, see <https://www.gnu.org/licenses/>. 
"""




import os
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from util import *
from grainclass import *




class Grainsize():
    
    
    # insert samplenames() function for instead of calling separately?
    def __init__(self, path, area=None, lith=None):
        self.path = path
        self.area = area
        self.lith = lith
    

    def samplenames(self):
        '''
        Collects basenames of class path(s).

        Returns
        -------
        samplenames : list
            sample names inferred from file basename(s)

        '''
        samplenames = []
        for path in self.path:                           
            data_basename = os.path.basename(path)           
            file, ext = os.path.splitext(data_basename)
            samplenames.append(file)
        
        return samplenames
    



    # collect all bins...solves rounding...or different gs analysis methods
    def bins(self, bin_min=0.375198, bin_rows=93, bin_col=0):
        '''
        Diameter bins used for grain size analysis.

        Parameters
        ----------
        bin_min : integer or float, optional
            value of smallest grain size bin in microns used in analysis; default
            is 0.375198 for Kentucky Geological Survey.
        bin_rows : integer, optional
            number of rows containing bin sizes; default is 93.
        bin_col : integer, optional
            vertical column number in data path file(s) containing bin sizes; 
            default is 0 (first column).

        Returns
        -------
        bins : Dataframe
            Dataframe of bins used in grain size analysis in microns, millimeters,
            and phi units.

        '''
        bins = pd.DataFrame(columns=['phi', 'mm', 'microns'])
        x = 0
        
        # extract grain size bins from first file only
        for path in self.path:
            while x == 0:
                file = pd.read_excel(path, header=None)
                i, c = np.where(file == bin_min)            
            
                bins['microns'] = file.iloc[i[0]:i[0]+bin_rows, bin_col].astype(float)      
                bins['mm'] = bins['microns'] / 1000                            
                bins['phi'] = -1 * np.log2(bins['mm'])  
                
                x += 1
        
        bins = bins.iloc[::-1].reset_index(drop=True)
        
        return bins                    
    



    # delete mean and std deviation...update gems_ex...plotting...etc     
    def data(self, bin_min=0.375198, data_rows=93, data_col=1):   
        '''
        Collects data from grain size analysis in class path file(s)

        Parameters
        ----------
        bin_min : integer or float, optional
            value of smallest grain size bin in microns used in analysis. The 
            default is 0.375198 for Kentucky Geological Survey.
        data_rows : integer, optional
            number of rows in data path(s) containing data and bin sizes. The 
            default is 93 for Kentucky Geological Survey.
        data_col : integer, optional
            vertical column number in data path file(s) containing data.
            The default is 1 (second column) for Kentucky Geological Survey.

        Returns
        -------
        data : Dataframe
            Dataframe of grain size analysis data from class path file(s)

        '''
        names = self.samplenames()
        data = pd.DataFrame()
        
        # read files
        x = 0
        for path in self.path:           
            file = pd.read_excel(path, header=None)  
            i, c = np.where(file == bin_min)                                    
            data[names[x]] = file.iloc[i[0]:i[0]+data_rows, data_col].astype(float)
            x += 1
            
        # reorganize for standard grain size distribution plots
        data = data.iloc[::-1].reset_index(drop=True).replace(np.nan, 0)
        
        # average and standard deviation if multiple samples
        if len(names) >= 1:
            data['mean'] = data.mean(axis=1)
            data['std'] = data.std(axis=1)
                
        return data
    



    # delete mean and std deviation...update gems_ex...plotting...etc     
    def data_cp(self):
        '''
        Calculates cumulative percentage of grain size data collected from 
        Grainsize.data class method

        Returns
        -------
        cp : Dataframe
            Dataframe of cumulative percentages of grain size data.

        '''
        names = self.samplenames()
        data = self.data()
        cp = pd.DataFrame()  

        for sample in names:
            cp[sample] = (data[sample].cumsum() / data[sample].sum()) * 100
        
        cp['mean'] = cp.mean(axis=1)
        cp['std'] = cp.std(axis=1)
    
        return cp



    
    # add row for lithology on first row
    def data_st(self, prom=0.1):
        '''
        Calculates statistics for grain size data from class path file(s)

        Parameters
        ----------
        prom : integer or float, optional
            Peak prominence used for collecting significant modes in multimodal
            samples. The default is 0.1.

        Returns
        -------
        st : Dataframe
            Dataframe of statistics of grain size data.

        '''
        data = self.data().iloc[:,:-1]
        cp = self.data_cp().iloc[:,:-1]
        phi = self.bins()['phi']
        st = pd.DataFrame(columns=data.columns)
        
        # stats derived from grain size data
        max_list = []
        min_list = []
        mode_list = []
        for column, contents in data.iteritems():
            idx = contents[contents > 0].index
            
            max_ = phi[idx[0]]
            max_list.append(max_)
            
            min_ = phi[idx[-1]]
            min_list.append(min_)
                        
            peak_idx = find_peaks(contents, prominence=prom)
            mode_val = contents[peak_idx[0]]
            mode_phi = phi[peak_idx[0]]
            mode_sort = [y for x,y in sorted(zip(mode_val, mode_phi))]
            mode_sort = mode_sort[::-1]
            mode_list.append(mode_sort)
            
        # stats derived from cumulative percentage data
        mean_list = []
        median_list = []
        sort_list = []
        skew_list = []
        kurt_list = []
        s_list = []
        m_list = []
        c_list = []
        for column, contents in cp.iteritems():
            phi5 = np.interp(5, contents, phi)
            phi16 = np.interp(16, contents, phi)
            phi25 = np.interp(25, contents, phi)
            phi50 = np.interp(50, contents, phi)
            phi75 = np.interp(75, contents, phi)
            phi84 = np.interp(84, contents, phi)
            phi95 = np.interp(95, contents, phi)
            
            median = phi50
            median_list.append(median)
            
            mean = (phi16 + phi50 + phi84) / 3
            mean_list.append(mean)
    
            sort = ((phi84 - phi16) / 4) + ((phi95 - phi5) / 6.6)
            sort_list.append(sort)
    
            skew = ((phi16 + phi84 - (2*phi50)) / (2 * (phi84 - phi16))
                    ) + ((phi5 + phi95 - (2*phi50)) / (2 * (phi95 - phi5)))
            skew_list.append(skew)

            kurt = (phi95 - phi5) / (2.44 * (phi75 - phi25))
            kurt_list.append(kurt)
    
            s = np.interp(4, phi, contents)
            s_list.append(s)
    
            m = np.interp(8, phi, contents) - s
            m_list.append(m)
    
            c = 100 - (m + s)
            c_list.append(c)
        
        # add rows in st dataframe for all stats and qualitative descriptions
        st.loc['sand'] = s_list
        st.loc['silt'] = m_list
        st.loc['clay'] = c_list
        st.loc['silt_clay'] = [str(round(x)) + '+' + str(round(y)) for x,y in zip(m_list, c_list)]
        st.loc['sediment_class'] = [folkclass(x,y,z) for x,y,z in zip(s_list, m_list, c_list)]
        st.loc['max'] = max_list
        st.loc['max_gs'] = [wentclass(i) for i in max_list]
        st.loc['min'] = min_list
        st.loc['min_gs'] = [wentclass(i) for i in min_list]
        st.loc['mean'] = mean_list
        st.loc['mean_gs'] = [wentclass(i) for i in mean_list]
        st.loc['median'] = median_list
        st.loc['median_gs'] = [wentclass(i) for i in median_list]
        st.loc['sorting'] = sort_list
        st.loc['sorting_class'] = [sortclass(i) for i in sort_list]
        st.loc['skewness'] = skew_list
        st.loc['skewness_class'] = [skewclass(i) for i in skew_list]
        st.loc['kurtosis'] = kurt_list
        st.loc['kurtosis_class'] = [kurtclass(i) for i in kurt_list]
        
        # make all mode lists same length then add mode rows in st dataframe
        mode_num = len(max(mode_list, key=len))
        for modes in mode_list:                      
            while len(modes) < mode_num:
                modes.append(np.nan)
        
        x = 1                                       
        while x <= mode_num:
            mode_label = 'mode' + str(x)
            st.loc[mode_label] = [modes[x-1] for modes in mode_list]
            st.loc[mode_label + '_gs'] = [wentclass(modes[x-1]) for modes in mode_list]
            x += 1
        
        return st
  
    
  
# plot method for individual analyses

# plot method for multiple analyses
    

# TESTING
path = selectdata()
test = Grainsize(path)
