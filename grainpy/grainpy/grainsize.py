# -*- coding: utf-8 -*-
"""
This module contains the class for grain size analysis data with GrainPy.


--------------------------------------
Copyright 2021-2022 Matthew A. Massey

This file is part of GrainPy.

GrainPy is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. GrainPy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with GrainPy. If not, see <https://www.gnu.org/licenses/>. 
"""


import os
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import scipy.stats
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from .classify import *


class GrainSizeDist():
    """
    Class for collecting, compiling, analyzing, and visualizing grain size distribution data.
    
    Parameters
    ----------
    path: list
        list of paths
    lith: string, optional
        indicator string of lithology; meant for mutliple samples of same lithology
    area: string, optional
        indicator string of area, location, or other; meant for multiple samples of same area
    
    """

    def __init__(self, path, lith=None, area=None):
        self.path = path
        self.lith = lith
        self.area = area

    def samplenames(self):
        '''
        Collects basenames of path(s), inferred to be sample names.

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
        Collects bins from first path only. Assumes bins represent lower channel thresholds, and in microns.

        Parameters
        ----------
        bin_min : integer or float, optional
            value of smallest grain size bin in microns used in analysis; default is 0.375198.
        bin_rows : integer, optional
            number of rows containing bin sizes; default is 93.
        bin_col : integer, optional
            vertical column number in data path file(s) containing bin sizes; default is 0.

        Returns
        -------
        bins : Dataframe
            Dataframe of bins used in grain size analysis in microns, millimeters, and phi units.

        '''
        bins = pd.DataFrame(columns=['phi', 'mm', 'microns'])
        x = 0

        # extract grain size bins from first file only
        for path in self.path:
            while x == 0:
                file = pd.read_excel(path, header=None)
                i, c = np.where(file == bin_min)

                bins['microns'] = file.iloc[i[0]:i[0] +
                                            bin_rows, bin_col].astype(float)
                bins['mm'] = bins['microns'] / 1000
                bins['phi'] = -1 * np.log2(bins['mm'])

                x += 1

        bins = bins.iloc[::-1].reset_index(drop=True)

        return bins

    def data(self, bin_min=0.375198, data_rows=93, data_col=1):
        '''
        Collects grain size data from path(s).

        Parameters
        ----------
        bin_min : integer or float, optional
            value of smallest grain size bin in microns used in analysis. The default is 0.375198.
        data_rows : integer, optional
            number of rows in data path(s) containing data and bin sizes. The default is 93.
        data_col : integer, optional
            vertical column number in data path file(s) containing data. The default is 1.

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
            data[names[x]] = file.iloc[i[0]:i[0] +
                                       data_rows, data_col].astype(float)
            x += 1

        # add new column of mean values
        data['mean'] = data.mean(axis=1)

        # reorganize for standard grain size distribution plots
        data = data.iloc[::-1].reset_index(drop=True).replace(np.nan, 0)

        return data

    def datacp(self):
        '''
        Calculates cumulative percentage of grain size data from path(s)

        Returns
        -------
        cp : Dataframe
            Dataframe of cumulative percentages of grain size data.

        '''

        cp = self.data().cumsum()

        return cp

    def datast(self, prom=0.1):
        '''
        Calculates statistics for grain size data from class path file(s)

        Parameters
        ----------
        prom : integer or float, optional
            Peak prominence used for collecting significant modes in multimodal samples. The default is 0.1.

        Returns
        -------
        st : Dataframe
            Dataframe of grain size statistics.

        '''
        data = self.data()
        cp = self.datacp()
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
            mode_sort = [y for x, y in sorted(zip(mode_val, mode_phi))]
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
        st.loc['silt+clay'] = [str(round(x)) + '+' + str(round(y))
                               for x, y in zip(m_list, c_list)]
        st.loc['sediment_class'] = [
            folk_sed(x, y, z) for x, y, z in zip(s_list, m_list, c_list)]
        st.loc['max'] = max_list
        st.loc['max_ww'] = [wentworth_gs(i) for i in max_list]
        st.loc['min'] = min_list
        st.loc['min_ww'] = [wentworth_gs(i) for i in min_list]
        st.loc['median'] = median_list
        st.loc['median_ww'] = [wentworth_gs(i) for i in median_list]
        st.loc['mean_folk'] = mean_list
        st.loc['mean_folk_ww'] = [wentworth_gs(i) for i in mean_list]
        st.loc['sorting_folk'] = sort_list
        st.loc['sorting_folk_class'] = [folk_sort(i) for i in sort_list]
        st.loc['skewness_folk'] = skew_list
        st.loc['skewness_folk_class'] = [folk_skew(i) for i in skew_list]
        st.loc['kurtosis_folk'] = kurt_list
        st.loc['kurtosis_folk_class'] = [folk_kurt(i) for i in kurt_list]

        # make all mode lists same length then add mode rows in st dataframe
        mode_num = len(max(mode_list, key=len))
        for modes in mode_list:
            while len(modes) < mode_num:
                modes.append(np.nan)

        x = 1
        while x <= mode_num:
            mode_label = 'mode' + str(x)
            st.loc[mode_label] = [modes[x-1] for modes in mode_list]
            st.loc[mode_label +
                   '_ww'] = [wentworth_gs(modes[x-1]) for modes in mode_list]
            x += 1

        return st

    def _gsd_format(self):
        """
        Hidden method to format grain size distribution plots.

        Returns
        -------
        fig : Matplotlib Figure instance
            New Matplotlib figure for plotting grain size distributions.
        ax : Matplotlib axes object
            Base axes for XY scales, Wentworth classification background, and data relative frequency plot for grain size distribution plots.
        ax2 : Matplotlib axes object
            Second axes object for cumulative frequency curve for grain size distribution plot.
        ax3 : Matplotlib axes object
            Third axes object for upper X axis.

        """

        # create figure and axes
        fig, ax = plt.subplots(1, 1, figsize=(8, 8), dpi=300)
        ax2 = ax.twinx()
        ax3 = ax.twiny()

        # format axes
        ax.tick_params(axis='x', width=0.5, labelsize=10)
        ax.tick_params(axis='y', color='0.5', width=0.5,
                       labelsize=10, labelcolor='0.5')
        ax.set_xlim(-1, 12)
        ax.set_xlabel('Grain diameter (\u03C6)', size=12, style='italic')
        ax.set_ylabel('Relative proportion (%)', size=12,
                      style='italic', color='0.5')

        ax2.set_ylim(0, 100)
        ax2.tick_params(axis='y', color='#AB2328', width=0.5,
                        labelsize=10, labelcolor='#AB2328')
        ax2.set_ylabel('Cumulative proportion (%)', size=12,
                       style='italic', color='#AB2328')
        ax2.spines['left'].set_visible(False)
        ax2.spines['right'].set(color='#AB2328')
        ax2_xtick_loc = [i for i in range(-1, 13, 1)]
        ax2_ytick_loc = [i for i in range(0, 101, 10)]
        ax2.set(xticks=ax2_xtick_loc)
        ax2.set(yticks=ax2_ytick_loc)

        ax3.set_xlim(2, 0.00024)
        ax3.tick_params(axis='x', color='k', width=0.5,
                        labelsize=10, labelcolor='k', pad=-1)
        ax3.set_xlabel('Grain diameter (mm)', size=12,
                       style='italic', color='k')
        ax3.set_xscale('log', base=2)
        ax3.spines['right'].set_visible(False)
        ax3.spines['left'].set_visible(False)
        ax3_xtick_loc = [2, 0.0625, 0.0039]
        ax3_xtick_lab = ['2', '0.0625', '0.0039']
        ax3.set(xticks=ax3_xtick_loc)
        ax3.set(xticklabels=ax3_xtick_lab)
        ax3.annotate('-sand-', xy=(0.18, 1.01), xycoords='axes fraction',
                     horizontalalignment='center', style='italic')
        ax3.annotate('-silt-', xy=(0.54, 1.01), xycoords='axes fraction',
                     horizontalalignment='center', style='italic')
        ax3.annotate('-clay-', xy=(0.85, 1.01), xycoords='axes fraction',
                     horizontalalignment='center', style='italic')

        # lines along Wentworth divisions
        for i in range(0, 9, 1):
            ax.plot([i, i], [0, 100], color='0.8', linewidth=0.25, zorder=0)

        # Patches for Wentworth sand divisions
        ax.add_patch(Rectangle((-1, 0), 1, 100,
                     color='#FFBA01', alpha=0.5, zorder=0))
        ax.add_patch(Rectangle((0, 0), 1, 100,
                     color='#FFC918', alpha=0.5, zorder=0))
        ax.add_patch(Rectangle((1, 0), 1, 100,
                     color='#FFD82F', alpha=0.5, zorder=0))
        ax.add_patch(Rectangle((2, 0), 1, 100,
                     color='#FEE745', alpha=0.6, zorder=0))
        ax.add_patch(Rectangle((3, 0), 1, 100,
                     color='#FEF65C', alpha=0.3, zorder=0))

        # Patches for Wentworth silt divisions
        ax.add_patch(Rectangle((4, 0), 1, 100,
                     color='#0080FF', alpha=0.3, zorder=0))
        ax.add_patch(Rectangle((5, 0), 1, 100,
                     color='#3399FF', alpha=0.3, zorder=0))
        ax.add_patch(Rectangle((6, 0), 1, 100,
                     color='#66B2FF', alpha=0.3, zorder=0))
        ax.add_patch(Rectangle((7, 0), 1, 100,
                     color='#99CCFF', alpha=0.3, zorder=0))

        # Patches for Wentworth clay division
        ax.add_patch(Rectangle((8, 0), 4, 100,
                     color='#6B8E23', alpha=0.1, zorder=0))

        return fig, ax, ax2, ax3

    def gsd_single(self, files=None, i=0, j=0):
        """
        Method to plot grain size distribution data as a histogram of binned sizes, cumulative percentage line, and statistics. Formatted to show Wentworth scale grain size divisions, x scales in phi units and millimeters, and legend with statistics. User has the option of plotting all files in the GrainSizeDist object (default) or slicing specific file(s) using list of specific sample name(s) or indexing (i, j). Plots are saved in jpeg and PDF formats in the same location as the data files.

        Parameters
        ----------
        files : list, optional
            List of strings of specific samples to be plotted. The default is None.
        i : integer, optional
            First index location for slicing specific files to be plotted. The default is 0.
        j : integer, optional
            Second index location for slicing specific files to be plotted. The default is 0.

        Returns
        -------
        None.

        """
        path = self.path
        bins = self.bins()
        data = self.data().iloc[:, :-1]
        cp = self.datacp().iloc[:, :-1]
        st = self.datast().iloc[:, :-1]

        # counter for saving files
        c = 0

        # Collect sample names to be plotted
        if files != None:
            samples = files
        elif i != 0 or j != 0:
            samples = self.samplenames()[i:j]
        else:
            samples = self.samplenames()

        # plot all samples
        for sample in samples:

            # create figure and axes
            fig, ax, ax2, ax3 = self._gsd_format()

            ax.set_ylim(0, max(data[sample]) + 0.25)
            ax.set_title(sample, size=18, weight='bold', style='italic')

            # plot bars of volume percentages within each bin
            ax.bar(bins['phi'], data[sample], width=0.105,
                   color='0.7', align='edge', edgecolor='k', lw=0.2)

            # plot cumulative percentage line
            ax2.plot(bins['phi'], cp[sample].replace(
                0, np.nan), color='#AB2328', linewidth=2.5)

            # plot statistic lines
            med_ln = ax.axvline(st[sample].loc['median'],
                                color='blue', ls=(0, (1, 1)), lw=1.5)
            mean_ln = ax.axvline(
                st[sample].loc['mean_folk'], color='blue', lw=1.5)
            modes = st[sample].iloc[19::2]
            mode_label = []
            x = 1
            for mode in modes:
                modes_ln = ax.axvline(mode, color='black', ls=(
                    0, (5, 1)), lw=1.5, zorder=4)
                if mode != np.nan:
                    label = 'mode%d: ' % x + \
                        str(round(modes[x-1], 1)) + '\u03C6' + \
                        ', {}'.format(wentworth_gs(modes[x-1]))
                    mode_label.append(label)
                x += 1

            # key and annotation text
            sed = st[sample].loc['sediment_class']
            sort = st[sample].loc['sorting_folk_class']
            sand = str(round(st[sample].loc['sand'], 1))
            silt = str(round(st[sample].loc['silt'], 1))
            clay = str(round(st[sample].loc['clay'], 1))
            ax.annotate('{0}, {1}  -  sand: {2}%,  silt: {3}%,  clay: {4}%'.format(
                sed, sort, sand, silt, clay), xy=(0.5, -0.105), xycoords='axes fraction',
                horizontalalignment='center')

            mean_lab = 'mean: {0:.1f}\u03C6, {1}'.format(st[sample].loc['mean_folk'],
                                                         st[sample].loc['mean_folk_ww'])
            med_lab = 'median: {0:.1f}\u03C6, {1}'.format(st[sample].loc['median'],
                                                          st[sample].loc['median_ww'])
            ax.legend(handles=[mean_ln, med_ln], labels=[mean_lab, med_lab],
                      bbox_to_anchor=(0.5, -0.133), ncol=2, fancybox=False,
                      frameon=False, loc='center')

            modelab = '  /  '.join(mode_label)
            ax2.legend(handles=[modes_ln], labels=[modelab], bbox_to_anchor=(0.5, -0.166),
                       fancybox=False, frameon=False, loc='center')

            skew = str(round(st[sample].loc['skewness_folk'], 2)) + ', {}'.format(
                st[sample].loc['skewness_folk_class'])
            kurt = str(round(st[sample].loc['kurtosis_folk'], 2)) + ', {}'.format(
                st[sample].loc['kurtosis_folk_class'])
            ax.annotate('skewness_folk: {0}     kurtosis_folk: {1}'.format(skew, kurt), xy=(0.5, -0.204),
                        xycoords='axes fraction', horizontalalignment='center')

            # save figure in directory with sample files
            save_pdf = os.path.splitext(path[c])[0] + '.pdf'
            plt.savefig(fname=save_pdf, dpi=300, bbox_inches='tight')

            save_jpg = os.path.splitext(path[c])[0] + '.jpg'
            plt.savefig(fname=save_jpg, dpi=300, bbox_inches='tight')

            # increase counter
            c += 1

            plt.show()
            plt.close()

    def gsd_multi(self, bplt=False, cplt=True, stplt=True, ci=True):
        """
        Method to plot grain size distribution data for multiple samples. Formatted to show Wentworth scale grain size divisions, x scales in phi units and millimeters, and legend with statistics. User has the options of plotting: (1) only cumulative frequency curves with 95% confidence interval of the mean (default); (2) only relative frequency histogram of binned data with 95% confidence interval; (3) both relative frequency data (left axis) and cumulative frequency data (left axis) with 95% confidence interval of cumulative curve. Plot is saved in jpeg and PDF formats in the directory where data files are located.

        Parameters
        ----------
        bplt : Bool, optional
            Option to plot data relative frequency histogram. The default is False.
        cplt : Bool, optional
            Option to plot cumulative frequency curve. The default is True.
        stplt : Bool, optional
            Option to plot data selected statistics and include in legend. The default is True.
        stplt : Bool, optional
            Option to plot 95% confidence interval of mean. The default is True.
        Returns
        -------
        None.

        """

        path = self.path[0]
        bins = self.bins()['phi']
        data = self.data().iloc[:, :-1]
        cp = self.datacp().iloc[:, :-1]
        st = self.datast()

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

        # default plot...cumulative curves only
        if bplt == False and cplt == True:
            # set axes and title...move cumulative axis to right side
            fig, ax, ax2, ax3 = self._gsd_format()
            ax2.set_visible(False)
            ax.set_title(title, size=18, weight='bold', style='italic')
            ax.set_ylim(0, 100)
            ax.tick_params(axis='y', color='#AB2328', width=0.5,
                           labelsize=10, labelcolor='#AB2328')
            ax.set_ylabel('Cumulative proportion (%)', size=12,
                          style='italic', color='#AB2328')
            ax_xtick_loc = [i for i in range(-1, 13, 1)]
            ax_ytick_loc = [i for i in range(0, 101, 10)]
            ax.set(xticks=ax_xtick_loc)
            ax.set(yticks=ax_ytick_loc)

            # plot all cumulative sample curves
            for column, contents in cp.replace(0, np.nan).iteritems():
                ax.plot(bins, contents, color='k', linewidth=0.5, zorder=2)

            # plot mean cumulative curve
            ax.plot(bins, cp.mean(axis=1).replace(0, np.nan), color='#AB2328',
                    linewidth=2.5, zorder=2.2)

            # 95% CI cumulative curve
            n = len(cp.columns)
            sem = cp.sem(axis=1)

            # use z (>=30) or t (<30) distribution
            if ci == True:
                if n >= 30:
                    ci = scipy.stats.norm.interval(
                        alpha=0.95, loc=cp.mean(axis=1), scale=sem)
                else:
                    ci = scipy.stats.t.interval(
                        alpha=0.95, df=n-1, loc=cp.mean(axis=1), scale=sem)

                ax.fill_between(bins, ci[1], ci[0],
                                color='#AB2328', alpha=0.3, zorder=2.1)

        # optional plot...both mean bars and mean cumulative
        elif bplt == True and cplt == True:
            # set axes and title
            fig, ax, ax2, ax3 = self._gsd_format()
            ax.set_ylim(0, max(data.mean(axis=1)) + 0.25)
            ax.set_title(title, size=18, weight='bold', style='italic')

            # plot bars of mean data
            ax.bar(bins, data.mean(axis=1), width=0.1, color='0.7', align='edge',
                   edgecolor='k', lw=0.2, zorder=1)

            # plot cumulative mean curve
            ax2.plot(bins, cp.mean(axis=1).replace(0, np.nan), color='#AB2328',
                     linewidth=2.5, zorder=2.2)

            # plot 95% CI cumulative curves
            n = len(cp.columns)
            sem = cp.sem(axis=1)

            # use z (>=30) or t (<30) distribution for CI
            if ci == True:
                if n >= 30:
                    ci = scipy.stats.norm.interval(
                        alpha=0.95, loc=cp.mean(axis=1), scale=sem)
                else:
                    ci = scipy.stats.t.interval(
                        alpha=0.95, df=n-1, loc=cp.mean(axis=1), scale=sem)

                ax2.fill_between(
                    bins, ci[1], ci[0], color='#AB2328', alpha=0.3, zorder=2.1)

        # optional plot...bars only
        else:
            # set axes and title...no cumulative axis on right
            fig, ax, ax2, ax3 = self._gsd_format()
            ax2.set_visible(False)
            ax.set_ylim(0, data.max().max() + 0.25)
            ax.set_title(title, size=18, weight='bold', style='italic')

            # plot all sample curves
            for column, contents in data.replace(0, np.nan).iteritems():
                ax.plot(bins, contents, color='k', linewidth=0.5, zorder=1.1)

            # plot mean bars
            ax.bar(bins, data.mean(axis=1), width=0.1, color='0.7', align='edge',
                   edgecolor='k', lw=0.2, zorder=1)

            # plot 95% CI curve
            n = len(data.columns)
            sem = data.sem(axis=1)

            if ci == True:
                if n >= 30:
                    ci = scipy.stats.norm.interval(
                        alpha=0.95, loc=data.mean(axis=1), scale=sem)
                else:
                    ci = scipy.stats.t.interval(
                        alpha=0.95, df=n-1, loc=data.mean(axis=1), scale=sem)

                ax.fill_between(bins, ci[1], ci[0],
                                color='#AB2328', alpha=0.3, zorder=1.2)

        # option to include selected stats with plot
        if stplt == True:

            # plot statistic lines
            med_ln = ax.axvline(st['mean'].loc['median'],
                                color='blue', ls=(0, (1, 1)), lw=1.5)
            mean_ln = ax.axvline(st['mean']['mean_folk'], color='blue', lw=1.5)

            modes = st['mean'].iloc[19::2]
            mode_label = []
            x = 1
            for mode in modes:
                modes_ln = ax.axvline(mode, color='black', ls=(
                    0, (5, 1)), lw=1.5, zorder=4)
                if mode != np.nan:
                    label = 'mode%d: ' % x + \
                        str(round(modes[x-1], 1)) + '\u03C6' + \
                        ', {}'.format(wentworth_gs(modes[x-1]))
                    mode_label.append(label)
                x += 1

            # means of selected statistics
            sand = round(st['mean'].loc['sand'], 1)
            silt = round(st['mean'].loc['silt'], 1)
            clay = round(st['mean'].loc['clay'], 1)

            sed = folk_sed(sand, silt, clay)

            sort = st['mean'].loc['sorting_folk_class']

            ax.annotate('{0}, {1}  -  sand: {2}%,  silt: {3}%,  clay: {4}%'.format(sed, sort, str(sand),
                        str(silt), str(clay)), xy=(0.5, -0.105), xycoords='axes fraction', horizontalalignment='center')

            # key and annotation text
            mean_lab = 'mean: {0:.1f}\u03C6, {1}'.format(st['mean'].loc['mean_folk'],
                                                         st['mean'].loc['mean_folk_ww'])
            med_lab = 'median: {0:.1f}\u03C6, {1}'.format(st['mean'].loc['median'],
                                                          st['mean'].loc['median_ww'])
            ax.legend(handles=[mean_ln, med_ln], labels=[mean_lab, med_lab],
                      bbox_to_anchor=(0.5, -0.133), ncol=2, fancybox=False,
                      frameon=False, loc='center')

            modelab = '  /  '.join(mode_label)
            ax3.legend(handles=[modes_ln], labels=[modelab], bbox_to_anchor=(0.5, -0.166),
                       fancybox=False, frameon=False, loc='center')

            skew = str(round(st['mean'].loc['skewness_folk'], 2)) + ', {}'.format(
                st['mean'].loc['skewness_folk_class'])
            kurt = str(round(st['mean'].loc['kurtosis_folk'], 2)) + ', {}'.format(
                st['mean'].loc['kurtosis_folk_class'])
            ax.annotate('skewness_folk: {0}     kurtosis_folk: {1}'.format(skew, kurt), xy=(0.5, -0.204),
                        xycoords='axes fraction', horizontalalignment='center')

        # save figure in sample file directory
        filesave = path.replace(os.path.basename(path), file)

        save_pdf = filesave + '.pdf'
        plt.savefig(fname=save_pdf, dpi=300, bbox_inches='tight')

        save_jpg = filesave + '.jpg'
        plt.savefig(fname=save_jpg, dpi=300, bbox_inches='tight')
