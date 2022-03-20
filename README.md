<h1 align="center": center; font-size: 100>GrainPy</h1>
      
<p align="center">
  <a href="#about">About</a> •
  <a href="#features">Features</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#installation">Installation</a> •
  <a href="#example">Example</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#contributions&feedback">Contributions & Feedback</a> •
  <a href="#license">License</a>
</p>

---

## About
GrainPy is a Python package for compiling, analyzing, visualizing, and interpreting grain size distribution data. The idea for GrainPy started with an abundance of grain size distribution data that wasn't being fully utilized. Initially, GrainPy was developed to quickly compare multiple grain size distribution analyses with geologic statistics and publication-quality plots. GrainPy will continue to add modern, user-friendly tools for the interpretation and presentation of sediment analyses.

### Features
      
<p align="right">(<a href="#top">back to top</a>)</p>



## Getting Started

### Installation
We reccomend installation using Conda as below...
```
conda install python=3 grainpy
```

### Examples
The basic functionality of GrainPy is explained below, however, please refer to the [documentation](https://example.com) for more detailed information and tutorials.

***Data compilation***
> Grain size distribution data comes from a variety of methods, including sieve, hydrometer, and laser diffraction particle size analyses. GrainPy collects and organizes this data (table of bins used and percentages) for single or multiple samples, calculates cumulative percentages, and a variety of sample statistics.
> 
> _images of input table...and output tables (data, cumulative, stats)_

***Grain size distribution curves***
> Grain size data can then be compiled into a usable format with GrainPy, used to calculate a variety of statistics, and produce publication-quality grain size distribution plots of individual or multiple samples.
>
> <p align="center">
>  <img alt="plots" src="https://i.imgur.com/oUCbnrL.png" ></p>
> </p>
> _Grain size distribution plots. Single sample plot (left) shows histogram of binned data, cumulative percentage curve, vertical lines for mean, median, and modes. Multiple sample plot (right) shows individual sample and mean with 95% confidence interval cumulative percentage curve._

<p align="right">(<a href="#top">back to top</a>)</p>



## Roadmap
- [ ] Initial build
- [ ] Package 0.1.0 release
- [ ] Compatibility with multiple types/sources of grain size distribution data
- [ ] Additional statistics
- [ ] Comparison of multiple objects (More plots? MLR? PCA?)
- [ ] Sediment mixing models
- [ ] Integrate with GIS

See the [open issues](https://github.com/masseygeo/GrainPy/issues) for a list of features currently in development.

<p align="right">(<a href="#top">back to top</a>)</p>




## Contributions & Feedback
Any contributions or feedback you make is greatly appreciated!

🔥 If you have a suggestion that you think would make this better, you can either:
>- [Create a new issue](https://github.com/masseygeo/GrainPy/issues/new) with the enhancement label 🏷️\
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;***...OR...***
>- Fork the Project.
>- Create your Feature Branch. `git checkout -b feature/amazingfeature`
>- Commit your Changes. `git commit -m 'Add some AmazingFeature'`
>- Push to the Branch. `git push origin feature/AmazingFeature`
>- Open a [Pull request](https://github.com/masseygeo/GrainPy/pulls).

🐛 If something isn't working, [create an issue](https://github.com/masseygeo/GrainPy/issues/new)

🌟 If you think GrainPy is pretty cool, please give it a star!

🗣️ If you need to get in touch for other reasons, [send me an email](mamass1@g.uky.edu)

<p align="right">(<a href="#top">back to top</a>)</p>



## License
Copyright 2021-2022 Matthew A. Massey\
_GrainPy is free software: you can redistribute it and/or modify it under the terms 
of the GNU General Public License as published by the Free Software Foundation, 
either version 3 of the License, or (at your option) any later version. GrainPy is 
distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without 
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE._\
_See the GNU General Public License for more details._

[![License: GPLv3](https://img.shields.io/badge/GrainPy%20license-GNUv3-lightgrey)](https://github.com/masseygeo/GrainPy/blob/main/LICENSE)

<p align="right">(<a href="#top">back to top</a>)</p>
