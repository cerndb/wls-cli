#*******************************************************************************
# Copyright (C) 2015, CERN
# This software is distributed under the terms of the GNU General Public
# License version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.
#
#
#*******************************************************************************'''
'''
Created on Jun 4, 2015

@author: Konrad Kaczkowski
'''
import logging


class LoggerWrapper(object):
    '''
    Class that wraps logger
    '''
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoggerWrapper, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        ''' Constructor '''
        self._logger = logging.getLogger("Logger")
        self._logger.setLevel(logging.DEBUG)
        
        if not self._logger.handlers:
            # create formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s ' + \
            '- %(levelname)s - %(message)s')
            self.create_console_handler(formatter)
            #self.create_file_handler(formatter)
        
    def set_level(self, mode):
        self._logger.setLevel(mode)
        
    def get_level_name(self, name):
        return logging.getLevelName(name)
        
    def set_logger_context(self, context):
        self._logger = logging.getLogger(context)
        
    @property
    def logger(self):
        ''' Property of a logger '''
        return self._logger
    
    def create_console_handler(self, formatter):
        ''' Creates console handler with a higher log level, adds formatter to the handler '''
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
    
    def create_file_handler(self, formatter):
        ''' Creates file handler which logs even debug messages, adds formatter to the handler '''
        file_handler = logging.FileHandler('application.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
        
        
    