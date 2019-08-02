mdwpy - Multi process downloader in python
========================================================

This module is usefull to download files faster than usual.
It split the file into parts and download each part on different process

## INSTALL

    pip install mdwpy

## USAGE

    >>> from mdwpy.downloader import Downloader
    >>> downloader = Downloader(url=url, filename=filename, usr= usr, pwd=pwd, directory=directory, progress=True)
    >>> downloader.run()

![Exemple](out.gif)

## LICENCE

Licence [BEERWARE](https://spdx.org/licenses/Beerware.html)