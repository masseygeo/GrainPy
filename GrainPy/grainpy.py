#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 21:12:57 2021

@author: Matthew Massey
"""


import os
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from matplotlib import pyplot as plt
#from math import isclose
#from datetime import date
#import scipy.stats as st

from util import *
from grainclass import *



class Grainsize():
    
    def __init__(self, path, area=None, lith=None):
        self.path = path
        self.area = area
        self.lith = lith
    

    # change to basenames or filenames 
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
    def bins(self, smallbin=0.375198, binrows=93, bincol=0):
        '''
        Diameter bins used for grain size analysis.

        Parameters
        ----------
        smallbin : integer or float, optional
            value of smallest grain size bin in microns used in analysis; default
            is 0.375198 for Kentucky Geological Survey.
        binrows : integer, optional
            number of rows containing bin sizes; default is 93.
        bincol : integer, optional
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
                i, c = np.where(file == smallbin)            
            
                bins['microns'] = file.iloc[i[0]:i[0]+binrows, bincol].astype(float)      
                bins['mm'] = bins['microns'] / 1000                            
                bins['phi'] = -1 * np.log2(bins['mm'])  
                
                x += 1
        
        bins = bins.iloc[::-1].reset_index(drop=True)
        
        return bins                    
    


    # add column for standard error and 95% Margin of error     
    def data(self, smallbin=0.375198, datarows=93, datacol=1):   
        '''
        Collects data from grain size analysis in class path file(s)

        Parameters
        ----------
        smallbin : integer or float, optional
            value of smallest grain size bin in microns used in analysis. The 
            default is 0.375198 for Kentucky Geological Survey.
        datarows : integer, optional
            number of rows in data path(s) containing data and bin sizes. The 
            default is 93 for Kentucky Geological Survey.
        datacol : integer, optional
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
            i, c = np.where(file == smallbin)                                    
            data[names[x]] = file.iloc[i[0]:i[0]+datarows, datacol].astype(float)
            x += 1
            
        # reorganize for standard grain size distribution plots
        data = data.iloc[::-1].reset_index(drop=True).replace(np.nan, 0)
        
        # average and standard deviation if multiple samples
        if len(names) >= 1:
            data['mean'] = data.mean(axis=1)
            data['std'] = data.std(axis=1)
                
        return data
    


    # add column for 95% margin of error
    # different name to something else...cp?
    def cump(self):
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

    

    # update function names from grainclass module...import grainclass    
    def stats(self, prom=0.1):
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
        cp = self.cump().iloc[:,:-1]
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
            
        # stats derived from cumulative percentage of grain size data
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
  
    
  
    
  
    
  
    
    
    def singleplot(self, samp=None, i=0, j=0):
        '''
        Grain size plots with selected statistics for single file(s) from class 
        path(s). All samples from the class path(s) will be plotted by default, 
        however, user-selected plots may be defined using the parameters. Plots
        saved in class path(s) directory.

        Parameters
        ----------
        samp : string, optional
            name of one sepcific sample to be plotted. The default is None.
        i : integer, optional
            starting index value of specific sample(s) to be plotted. The 
            default is 0.
        j : integer, optional
            ending index value of specific sample(s) to be plotted. The 
            default is 0.

        Returns
        -------
        None.

        '''
        path = self.path
        data = self.data()
        cp = self.cump()
        st = self.stats()
        bins = self.bins()
        idx = 0
        
        # samp, i, and j arguments allows one, slice, or all samples to be plotted
        if type(samp) != str:   
            if i==0 and j==0:
                samples = self.samplenames()
            else:
                samples = self.samplenames()[i:j]
        else:
            samples=[samp]
        
        
        # plot all samples (default) or user-specified sample(s)
        for sample in samples:
            
            # create figure and axes in Kentucky Geological Survey format
            fig, ax, ax2, ax3 = gsplot()
            
            ax.set_ylim(0, max(data[sample]) + 0.25)
            ax.set_title(sample, size=18, weight='bold', style='italic')
            
            # plot bin volumes % bars
            ax.bar(bins['phi'], data[sample], width=0.1, color='0.7', align='edge', edgecolor='k', lw=0.2)
        
            # plot cumulative relative frequency line
            ax2.plot(bins['phi'], cp[sample].replace(0, np.nan), color='#00008B', linewidth=1.5)
            
            # plot stats
            med_ln = ax.axvline(st[sample].loc['median'], color='blue', lw=2) 
            mean_ln = ax.axvline(st[sample].loc['mean'], color='#FF3333', lw=2)
            modes = st[sample].iloc[19::2]
            mode_label = []
            x = 1
            for mode in modes:
                modes_ln = ax.axvline(mode, color='#00CC00', lw=2, zorder=4)
                if mode != np.nan:
                    label = 'mode%d: '%x + str(round(modes[x-1],1)) + '\u03C6' + ', {}'.format(wentclass(modes[x-1]))
                    mode_label.append(label)
                x+=1
                                
            # legend and annotation text
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
            save_pdf = os.path.splitext(path[idx])[0] + '.pdf'
            plt.savefig(fname=save_pdf, dpi=300, bbox_inches='tight')
            save_jpg = os.path.splitext(path[idx])[0] + '.jpg'
            plt.savefig(fname=save_jpg, dpi=300, bbox_inches='tight')
            idx += 1
        
            plt.show()
            plt.close()
            
    '''
    Add option to NOT use KGS formatting?
    Can remove sampl parameter and just use index range?
    '''


    
    def meanplot(self):
        path = self.path[0]
        data_mn = self.data().iloc[:,-2:]
        cp_mn = self.cump().iloc[:,-2:]
        cp = self.cump().iloc[:,:-2]
        st = self.stats()['mean']
        bins = self.bins()['phi']
        loc = self.area
        mat = self.lith
        
        # create figure and axes in Kentucky Geological Survey format
        fig, ax, ax2, ax3 = gsplot()
        ax.set_ylim(0, max(data_mn['mean']) + 0.25)
        
        # set title and savefile name
        if type(loc) != str and type(mat) != str:
            title = 'Mean Grain Size Distribution'
            file = 'MeanGSD'
        elif type(loc) != str and type(mat) == str:
            title = 'Mean Grain Size Distribution' + ' - ' + mat
            file = 'MeanGSD_' + mat
        elif type(loc) == str and type(mat) != str:
            title = 'Mean Grain Size Distribution' + ' - ' + loc
        else:
            nm = '{0} ({1})'.format(mat, loc)
            title = 'Mean Grain Size Distribution' + ' - ' + nm
            file = 'MeanGSD_' + mat + '_' + loc
        ax.set_title(title, size=18, weight='bold', style='italic')
        
        # plot bin volumes bars of average
        ax.bar(bins, data_mn['mean'], width=0.1, color='0.7', align='edge', edgecolor='k', lw=0.2)
    
        # plot cumulative average line and error
        ax2.plot(bins, cp_mn['mean'].replace(0,np.nan), color='white', linewidth=2, zorder=2.2)
        
        # plot error of cumulative frequency line
        cp_mn['count'] = cp.replace(0, np.nan).count(axis=1)
        cp_mn['df'] = cp_mn['count'] - 1
        cp_mn[cp_mn['df'] < 0] = 0
        cp_mn['SEM'] = cp_mn['std'] / np.sqrt(cp_mn['count'])
        cp_mn['ME'] = np.nan
 
        
 
    
 
        # # calculate Margin of Error from normal or t distribution
        # cp_mn[cp_mn['count'] >= 30]:
        #     st.zscore
        # elif cp_mn[0 < cp_mn['count'] < 30]:
            
            
        # cp_mn['ME'] = st.t.interval(alpha=0.95, df=cp_mn['df'], loc=cp_mn['mean'], scale=cp_mn['SEM'])
        
        # ci95_high
        # ci95_low
            
            
            
            
        cphigh = cp_mn['mean'] + cp_mn['std']
        #cphigh = cp_mn['mean'] + st.t.interval(alpha=0.95, df=len(cp_mn_arr)-1, loc=cp_mn['mean'])
        cplow = cp_mn['mean'] - cp_mn['std']
        ax2.fill_between(bins, cphigh, cplow, color='#00008B', alpha=0.5, zorder=2)
        ax2.plot(bins, cp.replace(0,np.nan), color='k', linewidth=0.5, zorder=2.1)




        # plot stats
        # med_ln = ax.axvline(st.loc['median'], color='blue', lw=2)
        
        # mean_ln = ax.axvline(st.loc['mean'], color='#FF3333', lw=2)
        
        # modes = st.iloc[19::2]
        # mode_label = []
        # x = 1
        # for mode in modes:
        #     modes_ln = ax.axvline(mode, color='#00CC00', lw=2, zorder=4)
        #     if mode != np.nan:
        #         label = 'mode%d: '%x + str(round(modes[x-1],1)) + '\u03C6' + ', {}'.format(wentclass(modes[x-1]))
        #         mode_label.append(label)

        # legend
        sed = st.loc['sediment_class']
        sort = st.loc['sorting_class']
        sand = str(round(st.loc['sand'], 1))
        silt = str(round(st.loc['silt'], 1))
        clay = str(round(st.loc['clay'], 1))
        ax.annotate('{0}, {1}  -  sand: {2}%,  silt: {3}%,  clay: {4}%'.format(
            sed, sort, sand, silt, clay), xy=(0.5, -0.105), xycoords='axes fraction', 
            horizontalalignment='center')

        # save figure in directory with sample files
        filesave = path.replace(os.path.basename(path), file)

        save_pdf =  filesave + '.pdf'
        plt.savefig(fname=save_pdf, dpi=300, bbox_inches='tight')
        save_jpg = filesave + '.jpg'
        plt.savefig(fname=save_jpg, dpi=300, bbox_inches='tight')
            
        plt.show()
        plt.close()

        return cp_mn

    '''
    plot fill area of 95% CI instead of standard deviation
    '''
    
    
    
    

# Testing


path = selectdata()

test = Grainsize(path)
