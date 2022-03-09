#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 18:56:21 2021

@author: Matthew Massey
"""



__all__ = [
    "selectdata",
    "gems",
    "gsdplot",
    "gsdmultiplot",
]



import tkinter as tk
from tkinter import filedialog
import os
from datetime import date
import pandas as pd
import numpy as np
#from scipy.signal import find_peaks, peak_prominences
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle



def selectdata():
    """
    Select file(s) using file dialog window

    Returns
    -------
    path : tuple
        file paths selected by user

    """

    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilenames(title='Select files...', filetypes=(
        [('Excel files', '*.xlsx *.xls')]))
    root.destroy()

    return path




# new function to check input data consistency
    # bins all same (or rounded)
    # same number of rows in data? maybe doesn't matter?



# update to work with current class
# re-format for current gems grain size fields
def gems(gsclass):
    """
    Export grain size data into GeMS table format; saves .xlsx file in directory
    where Grainsize class object is located

    Parameters
    ----------
    gsclass : class
        Object of Grainsize class

    """
    path = gsclass.path
    bins = gsclass.bins()
    data = gsclass.data().iloc[:,:-2]
    st = gsclass.stats().iloc[:,:-1]
    area = gsclass.area
    lith = gsclass.lith
    pre = str(date.today()).replace('-','') + '_'
    cols = ['Microns_' + str(i) for i in bins['microns']]
    
    comp = pd.DataFrame(data, copy=True).T
    comp.index.name = 'FieldLocationID'
    comp.columns = cols
    comp = comp.drop(['Microns_2000.0'], axis=1)
    comp.insert(0, 'Sand', st.loc['sand'])
    comp.insert(1, 'Silt', st.loc['silt'])
    comp.insert(2, 'Clay', st.loc['clay'])
    comp.insert(3, 'Silt_Clay', st.loc['silt_clay'])
    
    if area is None:
        if lith is None:
            name = pre + 'GS_gems.xlsx'
        else:
            name = pre + lith + '_gems.xlsx'
    else:
        if lith is None:
            name = pre + area + '_gems.xlsx'
        else:
            name = pre + area + '_' + lith + '_gems.xlsx'
    
    filesave = path[0].replace(os.path.basename(path[0]), name)
    comp.to_excel(filesave)  


        
# Grain Size Distribution Plot - individual sample
def gsp_single(gs_class, i=0, j=0):
    '''
    Grain size distribution plot(s) with selected statistics of single samples
    from Grainsize class path(s). All samples from the class path(s) will be 
    plotted by default, however, select subset using the i and j parameters. Plots
    saved in class path(s) directory.

    Parameters
    ----------
    gs_class : object
        Grainsize class instance.
    i : integer, optional
        starting index value of subset of sample(s) to be plotted. The 
        default is 0.
    j : integer, optional
        ending index value of subset of sample(s) to be plotted. The 
        default is 0.

    Returns
    -------
    None.

    '''
    path = gs_class.path
    bins = gs_class.bins()
    data = gs_class.data()
    cp = gs_class.cump()
    st = gs_class.stats()
    idx = 0
    
    # Collect sample names to be plotted. Either all (default) or slice (i,j)
    if i==0 and j==0:
            samples = gs_class.samplenames()[i:j]
    else:
            samples = gs_class.samplenames()


    
    # plot all samples (default) or user-specified sample(s)
    for sample in samples:
        
        # create figure and axes
        fig, ax = plt.subplots(1, 1, figsize=(8,8), dpi=300)
        ax2 = ax.twinx()
        ax3 = ax.twiny()

        # format axes
        ax.tick_params(axis='x', width=0.5, labelsize=10)
        ax.tick_params(axis='y', color='0.5', width=0.5, labelsize=10, labelcolor='0.5')
        ax.set_xlim(-1, 12)
        ax.set_ylim(0, max(data[sample]) + 0.25)
        ax.set_xlabel('Grain size (\u03C6)', size=12, weight='bold', style='italic')
        ax.set_ylabel('Bin volume (%)', size=12, weight='bold', style='italic', color='0.5')
        ax.set_title(sample, size=18, weight='bold', style='italic')
        
        ax2.set_ylim(0,100)
        ax2.tick_params(axis='y', color='#00008B', width=0.5, labelsize=10, labelcolor='#00008B')
        ax2.set_ylabel('Cumulative volume (%)', size=12, weight='bold', style='italic', color='#00008B')
        ax2.spines['left'].set(color='0.5')
        #ax2.spines['left'].set_visible(False)
        ax2.spines['right'].set(color='#00008B')
        ax2_xtick_loc = [i for i in range(-1,13,1)]
        ax2_ytick_loc = [i for i in range(0,101,10)]
        ax2.set(xticks=ax2_xtick_loc)
        ax2.set(yticks=ax2_ytick_loc)
        
        ax3.set_xlim(2, 0.00024)
        ax3.tick_params(axis='x', color='k', width=0.5, labelsize=10, labelcolor='k', pad=-1)
        ax3.set_xlabel('Grain size (mm)', size=12, weight='bold', style='italic', color='k')
        ax3.set_xscale('log', base=2)
        ax3.spines['right'].set_visible(False)
        ax3.spines['left'].set_visible(False)
        ax3_xtick_loc = [2, 0.0625, 0.0039]
        ax3_xtick_lab = ['2', '0.0625', '0.0039']
        ax3.set(xticks=ax3_xtick_loc)
        ax3.set(xticklabels=ax3_xtick_lab)
        ax3.annotate('-sand-', xy=(0.18, 1.01), xycoords='axes fraction', horizontalalignment='center', style='italic')
        ax3.annotate('-silt-', xy=(0.54, 1.01), xycoords='axes fraction', horizontalalignment='center', style='italic')
        ax3.annotate('-clay-', xy=(0.85, 1.01), xycoords='axes fraction', horizontalalignment='center', style='italic')

        # background lines and color patches for Wentworth grain size divisions
        for i in range(0,9,1):
            ax.plot([i,i], [0,100], color='0.8', linewidth=0.25, zorder=0)

        ax.add_patch(Rectangle((-1,0), 1, 100, color='#FFDAB9', alpha=0.5, zorder=0))
        ax.add_patch(Rectangle((0,0), 1, 100, color='#FFE4B5', alpha=0.5, zorder=0))
        ax.add_patch(Rectangle((1,0), 1, 100, color='#FFEFD5', alpha=0.5, zorder=0))
        ax.add_patch(Rectangle((2,0), 1, 100, color='#FFFACD', alpha=0.6, zorder=0))
        ax.add_patch(Rectangle((3,0), 1, 100, color='#FFFFE0', alpha=0.3, zorder=0))
        ax.add_patch(Rectangle((4,0), 1, 100, color='#0080FF', alpha=0.3, zorder=0))
        ax.add_patch(Rectangle((5,0), 1, 100, color='#3399FF', alpha=0.3, zorder=0))
        ax.add_patch(Rectangle((6,0), 1, 100, color='#66B2FF', alpha=0.3, zorder=0))
        ax.add_patch(Rectangle((7,0), 1, 100, color='#99CCFF', alpha=0.3, zorder=0))
        ax.add_patch(Rectangle((8,0), 4, 100, color='#6B8E23', alpha=0.1, zorder=0))
        
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
                            
        # format legend and annotation text
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
        



# Grain Size Distribution Plot - mean plot of multiple samples
def meanplot(self):
    path = self.path[0]
    data_mn = self.data().iloc[:,-2:]
    cp_mn = self.cump().iloc[:,-2:]
    cp = self.cump().iloc[:,:-2]
    st = self.stats()['mean']
    bins = self.bins()['phi']
    loc = self.area
    mat = self.lith
    
    # create figure and axes
    fig, ax, ax2, ax3 = gsplot()
    
    # format axes
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

        


# Peak prominence utility
def modeprom(gsclass):
    #data = gsclass.data().iloc[:,:-2]
    
    # find peaks
    
    # find prominences
    
    # plot histogram or bar chart of prominences for user to then apply to class object
    
    # no return
    
    pass



# def gsplot():
#     fig, ax = plt.subplots(1, 1, figsize=(8,8), dpi=300)

#     ax.tick_params(axis='x', width=0.5, labelsize=10)
#     ax.tick_params(axis='y', color='0.5', width=0.5, labelsize=10, labelcolor='0.5')
#     ax.set_xlim(-1, 12)
#     ax.set_xlabel('Grain size (\u03C6)', size=12, weight='bold', style='italic')
#     ax.set_ylabel('Bin volume (%)', size=12, weight='bold', style='italic', color='0.5')
    
#     ax2 = ax.twinx()
#     ax2.set_ylim(0,100)
#     ax2.tick_params(axis='y', color='#00008B', width=0.5, labelsize=10, labelcolor='#00008B')
#     ax2.set_ylabel('Cumulative volume (%)', size=12, weight='bold', style='italic', color='#00008B')
#     ax2.spines['left'].set(color='0.5')
#     ax2.spines['right'].set(color='#00008B')
#     ax2_xtick_loc = [i for i in range(-1,13,1)]
#     ax2_ytick_loc = [i for i in range(0,101,10)]
#     ax2.set(xticks=ax2_xtick_loc)
#     ax2.set(yticks=ax2_ytick_loc)

#     ax3 = ax.twiny()
#     ax3.set_xlim(2, 0.00024)
#     ax3.tick_params(axis='x', color='k', width=0.5, labelsize=10, labelcolor='k', pad=-1)
#     ax3.set_xlabel('Grain size (mm)', size=12, weight='bold', style='italic', color='k')
#     ax3.set_xscale('log', base=2)
#     ax3.spines['right'].set_visible(False)
#     ax3.spines['left'].set_visible(False)
#     ax3_xtick_loc = [2, 0.0625, 0.0039]
#     ax3_xtick_lab = ['2', '0.0625', '0.0039']
#     ax3.set(xticks=ax3_xtick_loc)
#     ax3.set(xticklabels=ax3_xtick_lab)
#     ax3.annotate('-sand-', xy=(0.18, 1.01), xycoords='axes fraction', horizontalalignment='center', style='italic')
#     ax3.annotate('-silt-', xy=(0.54, 1.01), xycoords='axes fraction', horizontalalignment='center', style='italic')
#     ax3.annotate('-clay-', xy=(0.85, 1.01), xycoords='axes fraction', horizontalalignment='center', style='italic')

#     # background lines and patches for Wentworth grain size divisions
#     for i in range(0,9,1):
#         ax.plot([i,i], [0,100], color='0.8', linewidth=0.25, zorder=0)

#     ax.add_patch(Rectangle((-1,0), 1, 100, color='#FFDAB9', alpha=0.5, zorder=0))
#     ax.add_patch(Rectangle((0,0), 1, 100, color='#FFE4B5', alpha=0.5, zorder=0))
#     ax.add_patch(Rectangle((1,0), 1, 100, color='#FFEFD5', alpha=0.5, zorder=0))
#     ax.add_patch(Rectangle((2,0), 1, 100, color='#FFFACD', alpha=0.6, zorder=0))
#     ax.add_patch(Rectangle((3,0), 1, 100, color='#FFFFE0', alpha=0.3, zorder=0))
#     ax.add_patch(Rectangle((4,0), 1, 100, color='#0080FF', alpha=0.3, zorder=0))
#     ax.add_patch(Rectangle((5,0), 1, 100, color='#3399FF', alpha=0.3, zorder=0))
#     ax.add_patch(Rectangle((6,0), 1, 100, color='#66B2FF', alpha=0.3, zorder=0))
#     ax.add_patch(Rectangle((7,0), 1, 100, color='#99CCFF', alpha=0.3, zorder=0))
#     ax.add_patch(Rectangle((8,0), 4, 100, color='#6B8E23', alpha=0.1, zorder=0))

#     return fig, ax, ax2, ax3
