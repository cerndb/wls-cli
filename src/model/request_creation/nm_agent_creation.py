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
Created on Jun 4, 2015

@author: Konrad Kaczkowski
'''
import subprocess
from common import LoggerWrapper
from dictionary import StrategyDictionary

class NMAgentCreator(object):
    '''
    Class responsible for creating agents executed with Node Manager
    '''

    def __init__(self):
        ''' Constructor '''
        
    def create_agent(self, data_wrapper, command, target):
        ''' NM request construction - script parameters '''
        dictionary_wrapper = StrategyDictionary(command)
        dictionary = dictionary_wrapper.get_tuple()
        operation = dictionary['NM']
        
        if data_wrapper.test:
            raise Exception("Unimplemented test case: testing NM.")
        
        agent = NMAgent(data_wrapper.wls_dir, data_wrapper.domain_name, \
                        data_wrapper.domain_dir, target)
        agent.setopt(operation)     
        return agent    
    
class NMAgent(object):
    '''
    Class representing Node Manager agent
    - object containing all data necessary to perform Node Manager request
    '''

    def __init__(self, wls_dir, domain_name, domain_dir, target):
        ''' Constructor '''
        self.wls_dir = wls_dir
        self.domain_name = domain_name
        self.domain_dir = domain_dir
        self.target = target
        
    def setopt(self,  operation_nm):
        ''' setting operation to be executed '''
        self.operation_nm = operation_nm
        
    def perform(self):
        ''' executing agent object - request for NM '''
        bash_command = self.wls_dir + "/common/bin/wlscontrol.sh -d " + \
        self.domain_name + " -r " + self.domain_dir + " -s " + self.target + \
        " " + self.operation_nm
        proc = subprocess.Popen(bash_command, stdout = subprocess.PIPE, 
                                stderr = subprocess.PIPE, shell = True)
        message_tuple = proc.communicate()
        message = message_tuple[0] + message_tuple[1]
        result = self.substitute_message(self.operation_nm, message, self.target)
        return result
    
    def logger_debug_print(self, message):
        logger_wrapper = LoggerWrapper()
        logger_wrapper.logger.debug(message) 
        
    def substitute_message(self, operation_nm, message, target):
        ''' changing default result message for similarity with REST result'''
        if self.operation_nm == "START":
            if message == "":
                result = "Started the server '" + target + "'. : SUCCESS"
                return result
            return message
        elif self.operation_nm == "KILL":
            if message == "":
                result = "Shutdown the server '" + target + "'. : SUCCESS"
                return result
            return message
        