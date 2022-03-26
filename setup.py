#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Matthew Massey",
    author_email='mamass1@g.uky.edu',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Geology/Science/Research/GIS',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python package for compiling, analyzing, visualizing, and interpreting grain size distribution data.",
    entry_points={
        'console_scripts': [
            'grainpy=grainpy.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='grainpy',
    name='grainpy',
    packages=find_packages(include=['grainpy', 'grainpy.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/masseygeo/grainpy',
    version='0.1.0',
    zip_safe=False,
)
