#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
 
import mdwpy
 
setup(
    name='mdwpy',
    version=mdwpy.__version__,
    packages=find_packages(),
    author='Matthieu Bossennec',
    author_email="matthieubossennec@gmail.com",
    description="Multi process downloader in python",
    long_description=open('README.md').read(),
    # install_requires= ,
    include_package_data=True,
    url='http://github.com/maazhe',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: Beerware",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Topic :: Communications",
    ],
    # entry_points = {
    #     'console_scripts': [
    #         'mdwpy = mdwpy.multi_process_downloader:Downloader',
    #     ],
    # },
    license="BEERWARE"
)