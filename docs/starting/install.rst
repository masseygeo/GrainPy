.. GrainPy documentation master file, created by
   sphinx-quickstart on Tue Mar 29 20:33:40 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Installation
============

Create a Virtual Environment
----------------------------

It is common practice to set up and work within virtual environments, as it helps avoid potential dependency conflicts, and represents good practice. It is also strongly recommended	to do that here with GrainPy. GrainPy was built and continues to be developed using `Conda <https://conda.io/projects/conda/en/latest/>`_ and `Anaconda <https://www.anaconda.com/>`_ environment, although it is not required and we present several command line procedures below for creating (first line) and activating (second line) your new virtual environment.

Conda...
^^^^^^^^
::

   conda create -n CoolNewGrainPyVirtualEnvironment
   conda activate CoolNewGrainPyVirtualEnvironment

Mac OSX...
^^^^^^^^^^
::

   python3 -m venv CoolNewGrainPyVirtualEnvironment
   source CoolNewGrainPyVirtualEnvironment/bin/activate

Windows...
^^^^^^^^^^
::

   pip install virtualenv
   virtualenv -p /usr/bin/python3 CoolNewGrainPyVirtualEnvironment   




Installation
-------------

Once your virtual environment is created and activated, installing GrainPy is similar across each of the three platforms discussed above.

Current Release
^^^^^^^^^^^^^^^^
Each released version of GrainPy is also indexed on `PyPi <https://pypi.org/project/grainpy/>`_, and it is recommended to install this package using `pip <https://pypi.org/project/pip/>`_. 

::

   python3 -m pip install grainpy
   # Note for Windows: "python3" should be substituted with "py"


Congratulations! the most current stable release of GrainPy is now installed and ready to use!



Developmental Version
^^^^^^^^^^^^^^^^^^^^^^

In some cases, the user may want to install the current working version of GrainPy, which can be done directly from Github.

::

   python3 -m pip install git+https://github.com/masseygeo/GrainPy@main
   # Note for Windows: "python3" should be substituted with "py"


Congratulations! the most current, developmental version of GrainPy is now installed and ready to use! If you experience bugs, please `create a new issue on Github <https://github.com/masseygeo/GrainPy/issues/new>`_ with the appropriate label


