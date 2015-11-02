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
Created on May 29, 2015

@author: Konrad Kaczkowski
'''
from io import BytesIO
import json
import pycurl
import time
from common.utils import AuthenticationError

class Executor(object):
    '''
    Main class that wraps REST / NM executor
    '''

    def __init__(self):
        ''' Constructor '''
        self.rest_executor = RESTExecutor()
        self.nm_executor = NMExecutor()
        
    def execute(self, agent, data_mockup):
        ''' chooses REST / NM exectutor and passes agent to be executed '''
        if str(type(agent)) == "<type 'pycurl.Curl'>" or \
        str(type(agent)) == "<class 'model.request_creation.rest_agent_creation.RESTAgent'>":
            command_executor = self.rest_executor
            operation_type = "REST"
        elif str(type(agent)) == "<class 'model.request_creation.nm_agent_creation.NMAgent'>":
            command_executor = self.nm_executor
            operation_type = "NM"
        else:
            raise Exception ("Unrecognized agent type: " + str(type(agent)))
        result = command_executor.execute(agent, data_mockup)
        self.fill_data(data_mockup, result, operation_type)
        
    def fill_data(self, data_mockup, result, operation_type):
        data_mockup.view_result_to_parse = result
        data_mockup.view_operation_type = operation_type
    
class RESTExecutor(object):
    '''
    Class that executes REST agent
    '''

    def execute(self, rest_agent, data_mockup):
        ''' executes REST agent and returns operation output '''
        data = BytesIO()
        rest_agent.setopt(rest_agent.WRITEFUNCTION, data.write)
        try:
            rest_agent.perform()
            http_code = rest_agent.get_http_code()
            rest_agent.close()
            dictionary = json.loads(data.getvalue())
            if rest_agent.raw:
                dictionary = json.dumps(dictionary, indent = 4, sort_keys = True)
        except (ValueError, pycurl.error) as exception:
            if isinstance(exception, ValueError) and http_code == 401:
                raise AuthenticationError
            raise Exception(exception)
        return dictionary

class NMExecutor(object):
    '''
    Class that executes NM agent
    '''
        
    def execute(self, nm_agent, data_mockup):
        ''' executes NM agent and returns operation output '''
        message = nm_agent.perform()
        if nm_agent.target == data_mockup.controller_adminserver_name:
            time.sleep(5)
        return message
        