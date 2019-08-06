#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
 
setup(
    name='mdwpy',
    version='1.2.1',
    packages=find_packages(),
    author='Matthieu Bossennec',
    author_email='mymail@protonmail.com',
    description="Multi process downloader in python",
    long_description=open('README.md').read(),
    # install_requires= ,
    include_package_data=True,
    url='https://github.com/maazhe/mdwpy',
    classifiers=[
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        # "Topic :: Download",
        # "Topic :: Python",
        # "Topic :: Multiprocessing",
        # "Topic :: Download fast",
    ],
    # entry_points = {
    #     'console_scripts': [
    #         'mdwpy = mdwpy.multi_process_downloader:Downloader',
    #     ],
    # },
    license="BEERWARE"
)
