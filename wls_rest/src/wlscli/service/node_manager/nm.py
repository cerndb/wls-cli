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
Created on Oct 26, 2015

@author: Konrad Kaczkowski

This module hides PyCurl library abstraction and implements Curl functionality.

'''
import subprocess
from wlscli.common import LoggerWrapper

class NMAgent(object):
    '''
    Class representing Node Manager agent
    - object containing all data necessary to perform Node Manager request
    '''

    def __init__(self, data_contract):
        ''' Constructor '''
        self.wls_dir = data_contract.wls_dir
        self.domain_name = data_contract.domain_name
        self.domain_dir = data_contract.domain_dir
        self.target = data_contract.target
        self.operation = data_contract.operation
        
    def execute(self):
        ''' executing agent object - request for NM '''
        try:
            bash_command = self.wls_dir + "/common/bin/wlscontrol.sh -d " + \
            self.domain_name + " -r " + self.domain_dir + " -s " + self.target + \
            " " + self.operation
        except TypeError:
            raise TypeError ("Some CERN data is missing. " + \
                "Use '-i ENTITY_NAME except for --url URL.")
        
        proc = subprocess.Popen(bash_command, stdout = subprocess.PIPE, 
                                stderr = subprocess.PIPE, shell = True)
        message_tuple = proc.communicate()
        status = proc.returncode
        message = message_tuple[0] + message_tuple[1]
        result = self.substitute_message(self.operation, message, self.target)
        return status, result
    
    def logger_debug_print(self, message):
        logger_wrapper = LoggerWrapper()
        logger_wrapper.logger.debug(message) 
        
    def substitute_message(self, operation, message, target):
        ''' changing default result message for similarity with REST result'''
        if self.operation == "START":
            if message == "":
                result = "Started the server '" + target + "'. : SUCCESS"
                return result
            return message
        elif self.operation == "KILL":
            if message == "":
                result = "Shutdown the server '" + target + "'. : SUCCESS"
                return result
            return message