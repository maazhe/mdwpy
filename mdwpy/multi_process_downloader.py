#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Multiprocess download implementation.
 
    Usage:
 
    >>> from spyd_downloader import Downloader
    >>> downloader = Downloader(url=url, filename=filename, usr= usr, pwd=pwd, directory=directory)
    >>> downloader.run()
"""

import concurrent.futures as futures
import os
import shutil
import requests
from requests.auth import HTTPBasicAuth

## LOGGER / Optional
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class Downloader:

    ## INIT METHOD ##
    def __init__(self, **kwargs):

        try:
            self.url = kwargs.get('url', None)
            self.filename = kwargs.get('filename', 'default_filename')

            if not self.url:
                raise Exception('Url should be defined')

            self.auth = HTTPBasicAuth(kwargs.get('usr', None), kwargs.get('pwd', None))
            self.directory = kwargs.get('directory', './')

            self.file_parts = self.get_file_parts()

        except Exception as e:
            logger.error('Error in Downloader: {0}'.format(str(e)))

    # RUN METHOD 
    # Run the download of each part of the file in different core
    def run(self):

        self.clean_data()
        success = 0
        with futures.ProcessPoolExecutor() as executor:
            for size, file in executor.map(self.download_parts, self.file_parts):
                if size:
                    logger.info('Process Success for {}'.format(file))
                    success += 1
                else:
                    logger.info('Processing Error for {}'.format(file))

        if success == len(self.file_parts):  
          self.build_file()
        else:
          self.clean_data()
          raise Exception('Error during download')

    # CLEAN_DATA METHOD 
    # clean the filesystem to avoid error
    def clean_data(self):
        logger.info('--- Entering clean_data method ---')
        for p in self.file_parts:
            if os.path.exists(p['directory'] + p['filename']):
                os.remove(p['directory'] + p['filename'])
        if os.path.exists(self.directory + self.filename):
            os.remove(self.directory + self.filename)

    # BUILD_FILE METHOD
    # build the final file using the downloaded file parts
    def build_file(self):
        logger.info('--- Entering build_file method ---')
        with open(self.directory + self.filename, 'wb') as f:
            for p in self.file_parts:
                f.write(open(self.directory + p['filename'], 'rb').read())
                os.remove(self.directory + p['filename'])

    # DOWNLOAD_PARTS METHOD 
    # download a file part, retry download until complete or until reach max try
    def download_parts(self, file_part):
        logger.info('--- Entering download_parts method ---')

        filesize = 0
        expected_size = file_part['size']
        count_try = 0

        # Set count_try to 10
        while(filesize != expected_size and count_try < 10):
            
            if os.path.exists(file_part['directory'] + file_part['filename']):
                filesize = os.path.getsize(file_part['directory'] + file_part['filename'])
            
            headers = {'Range': 'bytes=%d-%d' % (file_part['start_pos'] + filesize, file_part['end_pos'])}
            req = requests.get(file_part['url'], headers=headers, stream=True, auth=file_part['auth'])

            with open(file_part['directory'] + file_part['filename'], 'ab') as f:
                shutil.copyfileobj(req.raw, f)

            filesize = os.path.getsize(file_part['directory'] + file_part['filename'])
            count_try += 1
        
        return filesize, file_part['filename']

    # GET_FILE_SIZE METHOD 
    # return the size of the complete file
    def get_file_size(self):
        logger.info('--- Entering get_file_size method ---')
        req = requests.head(self.url, stream=True, auth=self.auth)
        return int(req.headers['Content-Length'])

    # GET_FILE_PARTS METHOD 
    # return a list of each file part information as a dict
    def get_file_parts(self):
        logger.info('--- Entering get_file_parts method ---')
        size = self.get_file_size()
        logger.info('Filesize is {0}'.format(size))
        core_nb = len(os.sched_getaffinity(0))
        part_size = int(size / core_nb)
        file_parts = []

        for i in range(core_nb):
            start_pos = i * part_size

            if i == (core_nb - 1):
                end_pos = size
                p_size = end_pos - start_pos
            else:
                end_pos = ((i+1) * part_size) - 1
                p_size = end_pos + 1 - start_pos

            file_parts.append({
                'start_pos': start_pos,
                'end_pos' : end_pos,
                'size' : p_size,
                'filename' : self.filename + '.' + str(i),
                'directory': self.directory,
                'auth': self.auth,
                'url': self.url
            })
        return file_parts
