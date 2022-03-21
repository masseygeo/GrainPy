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
import scipy.stats
from matplotlib import pyplot as plt
from util import *
from grainclass import *




class Grainsize():
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
                
        return data
    



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
    
        return cp


    

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
        data=self.data()
        cp = self.data_cp()
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
        st.loc['median'] = median_list
        st.loc['median_gs'] = [wentclass(i) for i in median_list]
        st.loc['mean'] = mean_list
        st.loc['mean_gs'] = [wentclass(i) for i in mean_list]
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
  

    

    def gsd_single(self, files=None, i=0, j=0):
        """
        Method to plot grain size distribution data as a histogram of binned sizes, 
        cumulative percentage line, and statistics. Formatted to show Wentworth scale 
        grain size divisions, x scales in phi units and millimeters, and legend with 
        statistics. User has the option of plotting all files in the Grainsize object 
        (default) or slicing specific file(s) using list of specific sample name(s) or 
        indexing (i, j). Plots are saved in jpeg and PDF formats in the same location 
        as the data files.

        Parameters
        ----------
        files : list, optional
            List of strings of specific samples to be plotted. The default 
            is None.
        i : integer, optional
            First index location for slicing specific files to be plotted. The 
            default is 0.
        j : integer, optional
            Second index location for slicing specific files to be plotted. The 
            default is 0.

        Returns
        -------
        None.

        """
        path = self.path
        bins = self.bins()
        data = self.data()
        cp = self.data_cp()
        st = self.data_st()
        
        # counter for saving files
        c = 0
        
        # Collect sample names to be plotted
        if files != None:
            samples = files
        elif i!=0 or j!=0:
            samples = self.samplenames()[i:j]
        else:
            samples = self.samplenames()
    
        # plot all samples
        for sample in samples:
            
            # create figure and axes
            fig, ax, ax2, ax3 = gsd_format()
            
            ax.set_ylim(0, max(data[sample]) + 0.25)
            ax.set_title(sample, size=18, weight='bold', style='italic')
            
            # plot bars of volume percentages within each bin
            ax.bar(bins['phi'], data[sample], width=0.105, color='0.7', align='edge', edgecolor='k', lw=0.2)
        
            # plot cumulative percentage line
            ax2.plot(bins['phi'], cp[sample].replace(0, np.nan), color='#AB2328', linewidth=2.5)
            
            # plot statistic lines
            med_ln = ax.axvline(st[sample].loc['median'], color='blue', ls=(0, (1, 1)), lw=1.5) 
            mean_ln = ax.axvline(st[sample].loc['mean'], color='blue', lw=1.5)
            modes = st[sample].iloc[19::2]
            mode_label = []
            x = 1
            for mode in modes:
                modes_ln = ax.axvline(mode, color='black', ls=(0, (5, 1)), lw=1.5, zorder=4)
                if mode != np.nan:
                    label = 'mode%d: '%x + str(round(modes[x-1],1)) + '\u03C6' + ', {}'.format(wentclass(modes[x-1]))
                    mode_label.append(label)
                x+=1
                                
            # key and annotation text
            sed = st[sample].loc['sediment_class']
            sort = st[sample].loc['sorting_class']
            sand = str(round(st[sample].loc['sand'], 1))
            silt = str(round(st[sample].loc['silt'], 1))
            clay = str(round(st[sample].loc['clay'], 1))
            ax.annotate('{0}, {1}  -  sand: {2}%,  silt: {3}%,  clay: {4}%'.format(
                sed, sort, sand, silt, clay), xy=(0.5, -0.105), xycoords='axes fraction', 
                horizontalalignment='center')
            
            mean_lab = 'mean: {0:.1f}\u03C6, {1}'.format(st[sample].loc['mean'], 
                                                         st[sample].loc['mean_gs'])
            med_lab = 'median: {0:.1f}\u03C6, {1}'.format(st[sample].loc['median'], 
                                                          st[sample].loc['median_gs'])
            ax.legend(handles=[mean_ln, med_ln], labels=[mean_lab, med_lab], 
                      bbox_to_anchor=(0.5, -0.133), ncol=2, fancybox=False, 
                      frameon=False, loc='center')
            
            modelab = '  /  '.join(mode_label)
            ax2.legend(handles=[modes_ln], labels=[modelab], bbox_to_anchor=(0.5, -0.166), 
                       fancybox=False, frameon=False, loc='center')
            
            skew = str(round(st[sample].loc['skewness'], 2)) + ', {}'.format(
                st[sample].loc['skewness_class'])
            kurt = str(round(st[sample].loc['kurtosis'], 2)) + ', {}'.format(
                st[sample].loc['kurtosis_class'])
            ax.annotate('skewness: {0}     kurtosis: {1}'.format(skew, kurt), xy=(0.5, -0.204), 
                        xycoords='axes fraction', horizontalalignment='center')
            
            # save figure in directory with sample files
            save_pdf = os.path.splitext(path[c])[0] + '.pdf'
            plt.savefig(fname=save_pdf, dpi=300, bbox_inches='tight')
            
            save_jpg = os.path.splitext(path[c])[0] + '.jpg'
            plt.savefig(fname=save_jpg, dpi=300, bbox_inches='tight')      
            
            # increase counter
            c += 1




    def gsd_multi(self, bins_plt=False, st_plt=False):
        
        path = self.path[0]
        bins = self.bins()['phi']
        data = self.data()
        cp = self.data_cp()
        st = self.data_st()
             
        # create figure and axes
        fig, ax, ax2, ax3 = gsd_format()
        ax.set_ylim(0, max(data.mean(axis=1)) + 0.25)  
        
        # set savefile name and plot title
        if type(self.area) != str and type(self.lith) != str:
            title = 'Mean Grain Size Distribution'
            file = 'MeanGSD'
        elif type(self.area) != str and type(self.lith) == str:
            title = 'Mean Grain Size Distribution' + ' - ' + self.lith
            file = 'MeanGSD_' + self.lith
        elif type(self.area) == str and type(self.lith) != str:
            title = 'Mean Grain Size Distribution' + ' - ' + self.area
            file = 'MeanGSD_' + self.area
        else:
            both = '{0} ({1})'.format(self.lith, self.area)
            title = 'Mean Grain Size Distribution' + ' - ' + both
            file = 'MeanGSD_' + self.lith + '_' + self.area
        
        ax.set_title(title, size=18, weight='bold', style='italic')
        
        # optional plot of mean volume percentages within each bin
        if bins_plt == True:
            # plot bin volumes bars of average
            ax.bar(bins, data.mean(axis=1), width=0.1, color='0.7', align='edge', 
                   edgecolor='k', lw=0.2, zorder=1)
        
        # plot cumulative line of all samples
        for column, contents in cp.replace(0, np.nan).iteritems():
            ax2.plot(bins, contents, color='k', linewidth=0.5, zorder=2)
        
        # plot mean cumulative line
        ax2.plot(bins, cp.mean(axis=1).replace(0,np.nan), color='#AB2328', linewidth=2.5, 
                 zorder=2.2)
        
        # plot 95% confidence intervals
        n = len(cp.columns)
        sem = cp.sem(axis=1)
        
        # use z (>=30) or t (<30) distribution
        if n >= 30:
            ci = scipy.stats.norm.interval(alpha=0.95, loc=cp.mean(axis=1), scale=sem)
        else:
            ci = scipy.stats.t.interval(alpha=0.95, df=n-1, loc=cp.mean(axis=1), scale=sem) 
        
        ax2.fill_between(bins, ci[1], ci[0], color='#AB2328', alpha=0.3, zorder=2.1)
    
        
        
        # key and annotation text
        # means of selected statistics
        sand = str(round(st.loc['sand'].mean(), 1))
        silt = str(round(st.loc['silt'].mean(), 1))
        clay = str(round(st.loc['clay'].mean(), 1))
        sed = folkclass(st.loc['sand'].mean(), st.loc['silt'].mean(), st.loc['clay'].mean())
        sort = sortclass(st.loc['sorting'].mean())
        
        # key and annotation        
        ax.annotate('{0}, {1}  -  sand: {2}%,  silt: {3}%,  clay: {4}%'.format(
            sed, sort, sand, silt, clay), xy=(0.5, -0.105), xycoords='axes fraction', 
            horizontalalignment='center')
        
        # # optional stats plots and annotations
        # if st_plt == True:
        #     mean = st.loc['mean'].mean()
        #     mean_ln = ax.axvline(mean, color='blue', lw=1.5)
        #     mean_lab = wentclass(mean)
            
        #     median = st.loc['median'].mean()

            
            
        #     median = 
            
        #     med_ln = ax.axvline(st[sample].loc['median'], color='blue', ls=(0, (1, 1)), lw=1.5) 
        #     modes = st[sample].iloc[19::2]
            
            
        #     ax.legend(handles=[mean_ln, med_ln], labels=[mean_lab, med_lab], 
        #               bbox_to_anchor=(0.5, -0.133), ncol=2, fancybox=False, 
        #               frameon=False, loc='center')
            
    
        
        
        # save figure in directory with sample files
        filesave = path.replace(os.path.basename(path), file)
        
        save_pdf =  filesave + '.pdf'
        plt.savefig(fname=save_pdf, dpi=300, bbox_inches='tight')
        
        save_jpg = filesave + '.jpg'
        plt.savefig(fname=save_jpg, dpi=300, bbox_inches='tight')



# TESTING
path = selectdata()
test = Grainsize(path)
