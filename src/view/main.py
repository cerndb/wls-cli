#*******************************************************************************
# Copyright (C) 2015, CERN
# This software is distributed under the terms of the GNU General Public
# License version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.
#
#
#*******************************************************************************
'''
Created on May 28, 2015

@author: Konrad Kaczkowski
'''
from common import LoggerWrapper
import result_parse

class View(object):
    '''
    View class - facade. Responsible for gathering request and 
    presenting results to the end user.
    '''

    def __init__(self):
        ''' Constructor '''
        self.logger_wrapper = LoggerWrapper()
        
    def handle_output(self, data_mockup, is_get_domain_data_op = False):
        ''' Gets output from mockup and sends it to output parser. '''
        output = data_mockup.view_result_to_parse
        operation_type = data_mockup.view_operation_type
        if operation_type == "REST":
            result_parser = result_parse.RESTParser(data_mockup)
        elif operation_type == "NM" :
            result_parser = result_parse.NMParser(data_mockup)
        status_code = result_parser.parse(output, is_get_domain_data_op)
        return status_code
    
    def logger_print(self, message, mode = "INFO", status_code = -1):
        ''' Gets output from mockup and sends it to output parser.'''
        message = str(message) if status_code == -1 else str(message) \
        + "\nStatus code: " + str(status_code)
        
        if mode == "INFO":
            self.logger_wrapper.logger.info(message)
        elif mode == "DEBUG":
            self.logger_wrapper.logger.debug(message)
        elif mode == "ERROR":
            self.logger_wrapper.logger.error(message)

