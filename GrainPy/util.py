#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 18:56:21 2021

@author: Matthew Massey
"""

import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from openpyxl import load_workbook
#from scipy.signal import find_peaks, peak_prominences
#from datetime import date




def selectdata():
    """
    Function to select .xlsx or .xls file(s) using file dialog window.

    Returns
    -------
    path : list
        File paths selected by user.

    """

    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilenames(title='Select files...', filetypes=(
        [('Excel files', '*.xlsx *.xls')]))
    root.destroy()

    return list(path)


def datacheck(bmin=0.375198, brows=93, bcol=0):
    """
    Quality control check function for multiple files used in the Grainsize class. 
    Function checks consistency of minimum bin values and total number of bin rows
    with expected values defined by parameters. User is given option to change 
    minimum bin values if different than input by overwriting original files with 
    errors.
    
    Parameters
    ----------
    bmin : integer or float, optional
        Minimum bin size expected in all files. The default is 0.375198 microns.
    brows : integer, optional
        Total number of rows expected for bin values. The default is 93.
    bcol : integer, optional
        Column number for bins; must be same for all files. The default is 0 (Excel Column "A").

    Returns
    -------
    None.

    """
    path = selectdata()

    #empty lists for data checks
    bmin_check = []
    brows_check = []

    #loop through all files selected by user and examine bins
    for p in path:
        file = pd.read_excel(p, header=None)
        bins_df = pd.to_numeric(file.iloc[:, bcol], errors='coerce')

        #find minimum bin value in file and compare to expected
        bmin_val = bins_df.min()
        bmin_idx = np.where(bins_df == bmin_val)
        #if different, append path, value, and index to list
        if bmin_val != bmin:
            bmin_check.append([p, bmin_val, bmin_idx[0]])

        #find number of bin rows and compare to expected
        binrows = sum(bins_df >= bmin_val)
        if binrows != brows:
            brows_check.append([p, binrows])

    # results of checks
    if len(bmin_check) > 0:
        print("The following files have minimum bin values different than input of {}:".format(bmin))
        for i in bmin_check:
            print("{}, {}".format(i[0], i[1]))
    else:
        print("All files have consistent minimum bin values of {}".format(bmin))

    if len(brows_check) > 0:
        print("\nThe following files have total number of bin rows different than input of {}".format(brows))
        for i in brows_check:
            print("{}, {}".format(i[0], i[1]))
    else:
        print("\nAll files have consistent number of bin rows of {}".format(brows))

    # if error in minimum bin values, option to fix
    if len(bmin_check) > 0:

        value = input("Enter '1' to change value(s) in marked file(s) to expected value. WARNING! PERMANENT CHANGE IN FILE(S)!\nEnter any other key to ignore.\nEnter choice: ")

        #option 1, permanently change and save excel file(s)
        if value == "1":
            for i in bmin_check:
                error_path = i[0]
                wb = load_workbook(error_path)
                sheet = wb.active

                # convert column number to letter
                excol = chr(ord('@')+(bcol+1))

                # convert python row number to excel row number
                exrow = int(i[2]) + 1

                # excel coordinate string
                cellcoord = excol + str(exrow)

                # change to input minimum bin value
                sheet[cellcoord] = bmin

                # save file
                wb.save(error_path)



def df_ex(df):
    """
    Function to save dataframe as .csv or .xlsx file using file dialog window.

    Parameters
    ----------
    df : Pandas DataFrame object
        Dataframe to be saved.

    Returns
    -------
    None.

    """
    root = tk.Tk()
    root.withdraw()
    fs = filedialog.asksaveasfilename(title='Save data frame...', filetypes=(
        [('Comma Separated Values file', '*.csv'), ('Excel file', '*.xlsx')]), defaultextension='*.csv')
    root.destroy()
    
    if fs.endswith('.csv'):
        df.to_csv(fs)
    else:
        df.to_excel(fs)




def gems_ex(gsclass):
    """
    Function to save an object of the Grainsize class in a specific table format
    used by the Kentucky for GIS geodatabases. File saved as .csv or .xlsx.

    Parameters
    ----------
    gsclass : class
        Object of Grainsize class.
    
    Returns
    -------
    None.

    """
    bins = gsclass.bins().drop(index=0)
    data = gsclass.data().iloc[:,:-2].drop(index=0)
    st = gsclass.stats().iloc[:,:-1]
    
    # format bins titles
    cols = ['Lower' + str(i) for i in bins['microns']]
    
    
    # replacing decimal not working!!!!!!!!!!!!!
    for i in cols:
        i.replace('.', 'p')
    
    
    cols[0] = 'Upper2000' + cols[0]

    # create properly formatted df for export
    df = pd.DataFrame(data, copy=True).T
    df.columns = cols
    df.index.name = 'FieldLocationID'
    df.insert(0, 'SampleID', '')
    df.insert(1, 'BCSand', st.loc['sand'])
    df.insert(2, 'BCSilt', st.loc['silt'])
    df.insert(3, 'BCClay', st.loc['clay'])
    
    df_ex(df)






     
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
