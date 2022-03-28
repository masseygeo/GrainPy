<p align="center">
<img alt="plots" src="https://i.imgur.com/6T1gtg7.png" height="500" /></p>
</p>
      
<p align="center">
  <a href="#about">About</a> •
  <a href="#installation">Installation</a> •
  <a href="#examples">Examples</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#contributions">Contributions</a> •
  <a href="#license">License</a>
</p>

---

## About
GrainPy is a Python package for compiling, analyzing, visualizing, and interpreting grain size distribution data. The idea for GrainPy started with an abundance of grain size distribution data that wasn't being fully utilized. Initially, GrainPy was developed to quickly compare multiple grain size distribution analyses with geologic statistics and publication-quality plots. GrainPy will continue to add modern, user-friendly tools for the interpretation and presentation of sediment analyses.
      
<p align="right">(<a href="#top">back to top</a>)</p>


## Installation
It is strongly recommended to ***set up a virtual environment*** before installation, as it represents good practice and helps avoid potential dependency conflicts. In your new virtual environment (including Conda or Anaconda), you can then install the current version of GrainPy using pip...
```
# from Mac OSX terminal (substitute "py" for "python3" on Windows)
python3 -m pip install grainpy
```
This should install GrainPy along with its dependency packages pandas, numpy, matplotlib, scipy, and openpyxl.

## Examples
The basic functionality of GrainPy is explained below, however, please refer to the [documentation](https://example.com) for more detailed information and tutorials.

### Data compilation
Grain size distribution data comes from a variety of methods, including sieve, hydrometer, and laser diffraction particle size analyses. GrainPy collects and organizes this data (table of bins used and percentages) for single or multiple samples, calculates cumulative percentages, and a variety of sample statistics.
>
> ```
> files = ['path(s) to grain size data files']
> # create Grainsize object using path(s)
> var = grainsize.GrainSizeDist(files)
> var.data()
> var.datacp()
> var.datast()
> ```
> <p align="center">
>  <img alt="plots" src="https://i.imgur.com/XtCbxh2.png" height="400" /></p>
> </p>
> 
> _Multiple raw data tables collected from grain size measurements (left) are collected and compiled by GrainPy into usable compilation tables of the data, cumulative frequencies, and statistics (right)._

### Grain size distribution plots
Data can then be visualized and interpreted with publication-quality grain size distribution plots.
>
> ```
> # grain size distribution plots of single samples and all samples
> var.gsd_single()
> var.gsd_multi(stplt=False)
> ```
> <p align="center">
>  <img alt="plots" src="https://i.imgur.com/ZFmjpiz.png" height="400" /></p>
> </p>
> 
> _Single samples can be plotted (left) to show histogram of binned data, cumulative percentage curve, vertical lines for mean, median, and modes. Multiple sample plots (right) show cumulative frequencies of all samples, the mean, and a 95% confidence interval._

<p align="right">(<a href="#top">back to top</a>)</p>



## Roadmap
- [x] Initial build
- [x] Package release, version 0.1.0
- [ ] Additional functionality
     - [ ] Compatibility with multiple data sources
     - [ ] Additional statistics
     - [ ] Compare multiple objects
- [ ] Sediment mixing models
- [ ] Integrate with GIS

See the [open issues](https://github.com/masseygeo/GrainPy/issues) for a list of features currently in development.

<p align="right">(<a href="#top">back to top</a>)</p>




## Contributions
🔥 If you have a suggestion that you think would make this better, you can either:
>- [Create a new issue](https://github.com/masseygeo/GrainPy/issues/new) with the _enhancement_ label 🏷️\
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;***...OR...***
>- Fork the Project.
>     - Create your Feature Branch. `git checkout -b feature/amazingfeature`
>     - Commit your Changes. `git commit -m 'Add some AmazingFeature'`
>     - Push to the Branch. `git push origin feature/AmazingFeature`
>     - Open a [Pull request](https://github.com/masseygeo/GrainPy/pulls).

🐛 If something isn't working, [create a new issue](https://github.com/masseygeo/GrainPy/issues/new) with the appropriate label 🏷️

🌟 If you think GrainPy is pretty cool, please give it a star!

🗣️ If you need to get in touch for other reasons, [send me an email](mamass1@g.uky.edu)

<p align="right">(<a href="#top">back to top</a>)</p>



## License
Copyright 2021-2022, Matthew A. Massey\
<sub>_GrainPy is free software: you can redistribute it and/or modify it under the terms 
of the GNU General Public License as published by the Free Software Foundation, 
either version 3 of the License, or (at your option) any later version. GrainPy is 
distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without 
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details._

[![License: GPLv3](https://img.shields.io/badge/GrainPy%20license-GNUv3-lightgrey)](https://github.com/masseygeo/GrainPy/blob/main/LICENSE)

<p align="right">(<a href="#top">back to top</a>)</p>
