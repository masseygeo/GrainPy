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




__all__ = [
    "selectdata",
    "datacheck",
    "df_ex",
    "gems_ex",
    "gsd_format",
]




import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from openpyxl import load_workbook




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




def datacheck(bin_min=0.375198, bin_rows=93, bin_col=0):
    """
    Quality control check function for multiple files used in the Grainsize class. 
    Function checks consistency of minimum bin values and total number of bin rows
    with expected values defined by parameters. User is given option to change 
    minimum bin values if different than input by overwriting original files with 
    errors.
    
    Parameters
    ----------
    bin_min : integer or float, optional
        Minimum bin size expected in all files. The default is 0.375198 microns.
    bin_rows : integer, optional
        Total number of rows expected for bin values. The default is 93.
    bin_col : integer, optional
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
        bins_df = pd.to_numeric(file.iloc[:, bin_col], errors='coerce')

        #find minimum bin value in file and compare to expected
        bmin_val = bins_df.min()
        bmin_idx = np.where(bins_df == bmin_val)
        #if different, append path, value, and index to list
        if bmin_val != bin_min:
            bmin_check.append([p, bmin_val, bmin_idx[0]])

        #find number of bin rows and compare to expected
        binrows = sum(bins_df >= bmin_val)
        if binrows != bin_rows:
            brows_check.append([p, binrows])

    # results of checks
    if len(bmin_check) > 0:
        print("The following files have minimum bin values different than input of {}:".format(bin_min))
        for i in bmin_check:
            print("{}, {}".format(i[0], i[1]))
    else:
        print("All files have consistent minimum bin values of {}".format(bin_min))

    if len(brows_check) > 0:
        print("\nThe following files have total number of bin rows different than input of {}".format(bin_rows))
        for i in brows_check:
            print("{}, {}".format(i[0], i[1]))
    else:
        print("\nAll files have consistent number of bin rows of {}".format(bin_rows))

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
                excol = chr(ord('@')+(bin_col+1))

                # convert python row number to excel row number
                exrow = int(i[2]) + 1

                # excel coordinate string
                cellcoord = excol + str(exrow)

                # change to input minimum bin value
                sheet[cellcoord] = bin_min

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




def gems_ex(gso):
    """
    Function to save an object of the Grainsize class in a specific table format
    for GIS geodatabases. Saved as .csv or .xlsx file using file dialog window.

    Parameters
    ----------
    gso : class
        Object of Grainsize class.
    
    Returns
    -------
    None.

    """
    bins = gso.bins().drop(index=0)
    data = gso.data().drop(index=0)
    st = gso.data_st()
    
    # format bin titles
    cols = ['Lower' + str(i).replace('.','p') for i in bins['microns']]
    cols[0] = 'Upper2000' + cols[0]

    # create df, modify for geodatabase format
    df = pd.DataFrame(data, copy=True).T
    df.columns = cols
    df.index.name = 'SampleID'
    df.insert(0, 'BCSand', st.loc['sand'])
    df.insert(1, 'BCSilt', st.loc['silt'])
    df.insert(2, 'BCClay', st.loc['clay'])
    
    df_ex(df)




def gsd_format(ww=True):
    
    # create figure and axes
    fig, ax = plt.subplots(1, 1, figsize=(8,8), dpi=300)
    ax2 = ax.twinx()
    ax3 = ax.twiny()

    # format axes
    ax.tick_params(axis='x', width=0.5, labelsize=10)
    ax.tick_params(axis='y', color='0.5', width=0.5, labelsize=10, labelcolor='0.5')
    ax.set_xlim(-1, 12)    
    ax.set_xlabel('Grain diameter (\u03C6)', size=12, style='italic')
    ax.set_ylabel('Bin %', size=12, style='italic', color='0.5')
        
    ax2.set_ylim(0,100)
    ax2.tick_params(axis='y', color='#00008B', width=0.5, labelsize=10, labelcolor='#00008B')
    ax2.set_ylabel('Cumulative %', size=12, style='italic', color='#00008B')
    ax2.spines['left'].set_visible(False)
    ax2.spines['right'].set(color='#00008B')
    ax2_xtick_loc = [i for i in range(-1,13,1)]
    ax2_ytick_loc = [i for i in range(0,101,10)]
    ax2.set(xticks=ax2_xtick_loc)
    ax2.set(yticks=ax2_ytick_loc)
    
    ax3.set_xlim(2, 0.00024)
    ax3.tick_params(axis='x', color='k', width=0.5, labelsize=10, labelcolor='k', pad=-1)
    ax3.set_xlabel('Grain diameter (mm)', size=12, style='italic', color='k')
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

    # optional background lines and patches for Wentworth grain size divisions
    if ww == True:
        # lines along Wentworth divisions
        for i in range(0,9,1):
            ax.plot([i,i], [0,100], color='0.8', linewidth=0.25, zorder=0)
    
        # Patches for Wentworth sand divisions   
        ax.add_patch(Rectangle((-1,0), 1, 100, color='#FFBA01', alpha=0.5, zorder=0))
        ax.add_patch(Rectangle((0,0), 1, 100, color='#FFC918', alpha=0.5, zorder=0))
        ax.add_patch(Rectangle((1,0), 1, 100, color='#FFD82F', alpha=0.5, zorder=0))
        ax.add_patch(Rectangle((2,0), 1, 100, color='#FEE745', alpha=0.6, zorder=0))
        ax.add_patch(Rectangle((3,0), 1, 100, color='#FEF65C', alpha=0.3, zorder=0))
        
        # Patches for Wentworth silt divisions   
        ax.add_patch(Rectangle((4,0), 1, 100, color='#0080FF', alpha=0.3, zorder=0))
        ax.add_patch(Rectangle((5,0), 1, 100, color='#3399FF', alpha=0.3, zorder=0))
        ax.add_patch(Rectangle((6,0), 1, 100, color='#66B2FF', alpha=0.3, zorder=0))
        ax.add_patch(Rectangle((7,0), 1, 100, color='#99CCFF', alpha=0.3, zorder=0))
        
        # Patches for Wentworth clay division  
        ax.add_patch(Rectangle((8,0), 4, 100, color='#6B8E23', alpha=0.1, zorder=0))
        
    return fig, ax, ax2, ax3





# Peak prominence utility
#def modeprom(gsclass):
    #data = gsclass.data().iloc[:,:-2]
    
    # find peaks
    
    # find prominences
    
    # plot histogram or bar chart of prominences for user to then apply to class object
    
    # no return
    
    #pass