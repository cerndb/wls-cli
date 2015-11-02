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
from request_creation import AgentCreator
from request_parsing import RequestParser
from data_access import DataGetter
from data_storage import DataWrapper
from session import AuthenticationManager

class Model(object):
    '''
    Model class - facade. Handles business logic: delegates user request to be parsed, 
    creates agents to be executed by Controller.
    '''

    def __init__(self):
        ''' Constructor '''
        self.agent_creator = AgentCreator()
        self.request_parser = RequestParser()
        self.data_getter = DataGetter()
        self.data_wrapper = DataWrapper()
        self.authentication_manager = AuthenticationManager(self.data_wrapper, \
                                                            self.data_getter)
    
    def handle_user_request(self, request):
        ''' parsing request, filling data wrapper '''
        is_test = self.request_parser.parse(request, self.data_wrapper)
        return is_test, self.data_wrapper.target_type

    def prepare_data_for_request(self):
        return self.data_wrapper._view_wrapper

    def prepare_request(self, operation = None):
        ''' creating request agents 
        returns package_to_execute: operation_message, agents_list '''
        return self.agent_creator.execute(self.data_wrapper, operation)
    
    def authenticate(self):
        ''' authenticate '''
        self.authentication_manager.set_auth_data()

    def invalidate_cookie(self):
        ''' delete cookie '''
        self.authentication_manager.invalidate_cookie()
        
    def fill_data_wrapper(self, domain_data):
        self.data_getter.map_cluster_data_from_REST(self.data_wrapper, domain_data)

    