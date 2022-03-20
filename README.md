<p align="center": center; style="font-size": 20px>GrainPy</p>
      
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
GrainPy is a Python package for compiling, analyzing, visualizing, and interpreting grain size distribution data. The idea for GrainPy started with an abundance of grain size distribution data that wasn't being fully utilized. Initially, GrainPy was developed to quickly compare multiple grain size distribution analyses with geologic statistics and publication-quality plots. It is now evident that the potential for modern grain size analyses extends well beyond these basic, yet necessary, features, and GrainPy will continue to add user-friendly functionality.

### Features
      
<p align="right">(<a href="#top">back to top</a>)</p>



## Getting Started

### Installation
We reccomend installation using Conda as below...\
```
conda install python=3 grainpy
```

### Example
The basic functionality of GrainPy is explained below, however, please refer to the [documentation](https://example.com) for more detailed information and tutorials.

_**Input data structure**_
> Grain size distribution data can be collected from a variety of methods, including sieve analysis, hydrometer method, and laser diffraction particle size analyzer. GrainPy uses the raw data from any type of analysis to be organized in an Excel table (.xlsx or .xls) consisting of the bins used for the analysis and the data collected for each bin (relative percentage).
> 
> _image of tables in correct format...sieve data, hydrometer data, beckman-coulter_

_**Grain size distribution curves**_
> Grain size data can then be compiled into a usable format with GrainPy, used to calculate a variety of statistics, and produce publication-quality grain size distribution plots of individual or multiple samples.
> 
> _image of single plot...and multi plot_

<p align="right">(<a href="#top">back to top</a>)</p>



## Roadmap
- [ ] Initial build
- [ ] Package 0.1.0 release
- [ ] Added functionalities
     - [ ] Object compatibility with multiple types/sources of grain size distribution data
     - [ ] More geotechnical statistics
     - [ ] Multiple object comparitive plots and distributions (MLR? PCA?)
     - [ ] Sediment mixing models
- [ ] Integrate with GIS

See the [open issues](https://github.com/masseygeo/GrainPy/issues) for a list of features currently in development.

<p align="right">(<a href="#top">back to top</a>)</p>




## Contributions & Feedback
Any contributions or feedback you make is greatly appreciated!

🔥 If you have a suggestion that you think would make this better, you can simply [create a new issue](https://github.com/masseygeo/GrainPy/issues/new) with the  **enhancement** label...OR...fork the repo and create a pull request: 

     - Fork the Project
     - Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
     - Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
     - Push to the Branch (`git push origin feature/AmazingFeature`)
     - Open a Pull Request

🐛 If something isn't working, [create an issue](https://github.com/masseygeo/GrainPy/issues/new)

🌟 If you think GrainPy is pretty cool, please give it a star!

🗣️ If you need to get in touch for other reasons, [send me an email](mamass1@g.uky.edu)

<p align="right">(<a href="#top">back to top</a>)</p>



## License
[![License: GPLv3](https://img.shields.io/badge/GrainPy%20license-GNUv3-lightgrey)](https://github.com/masseygeo/GrainPy/blob/main/LICENSE)

<p align="right">(<a href="#top">back to top</a>)</p>
