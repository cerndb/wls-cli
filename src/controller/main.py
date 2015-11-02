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
Created on May 28, 2015

@author: Konrad Kaczkowski
'''
from agents_executor import Executor
import sys
from common.utils import State
from common.utils import TargetType
from common.utils import Operation
from common.utils import AuthenticationError

class Controller(object):
    '''
    Controller class - facade. Steering Model and View.
    '''

    def __init__(self, model, view, queue):
        ''' Constructor '''
        self._queue = queue
        self._model = model
        self._view = view
        
        self.operation_dispatcher = {State.PARSE_REQUEST: self.operate_parse_request,
           State.PREPARE_MODEL: self.operate_prepare_model,
           State.PREPARE_AGENTS: self.operate_prepare_agents,
           State.AUTHENTICATE: self.operate_authenticate,
           State.RENEW_COOKIE: self.operate_renew_cookie,
           State.GET_CLUSTERS_DATA: self.operate_get_clusters_data,
           State.OPERATE_REQUEST: self.operate_request
        }
        
    def run(self):
        ''' Main function that operates user request and executes it. '''
        
        self.data_mockup = None
        self.is_test = False
        self.objects_to_execute = None
        self.target_type = None
        self.status_code = 0
        self.current_operation = State.PARSE_REQUEST
        self.authentication_error_counter = 0
            
        while self.current_operation != State.FINISH:
            try:
                self.print_current_operation(self.current_operation, self.data_mockup)
                self.operation_dispatcher[self.current_operation]()
            
            except AuthenticationError:
                self.authentication_error_counter = self.authentication_error_counter + 1
                self.current_operation = State.RENEW_COOKIE
                if self.authentication_error_counter > 1:
                    self.status_code = self.status_code + 1
                    self._view.logger_print(self.current_operation, "INFO", self.status_code)
                    self.current_operation = State.FINISH
            
            except Exception as exception:
            #except ArithmeticError as exception:
                self.handle_exception(exception, self.status_code)
                self.current_operation = State.FINISH
                
        self.exit(self.status_code, self.is_test)
        
    def operate_parse_request(self):
        user_request = self.get_request()
        self.is_test, self.target_type = self.parse_request(user_request)
        self.current_operation = State.AUTHENTICATE
    
    def operate_prepare_model(self):
        self.data_mockup = self._model.prepare_data_for_request()
        if self.target_type == TargetType.CLUSTER or \
        self.target_type == TargetType.DOMAIN:
            self.current_operation = State.GET_CLUSTERS_DATA
            return
        self.current_operation = State.PREPARE_AGENTS
    
    def operate_prepare_agents(self):
        self.objects_to_execute = self._model.prepare_request()
        self.current_operation = State.OPERATE_REQUEST
    
    def operate_authenticate(self):
        self._model.authenticate()
        self.current_operation = State.PREPARE_MODEL
    
    def operate_renew_cookie(self):
        self._model.invalidate_cookie()
        self.current_operation = State.AUTHENTICATE
    
    def operate_get_clusters_data(self):
        self.objects_to_execute = self._model.prepare_request(Operation.GET_DOMAIN_DATA)
        request_status_code = self.execute_request(self.objects_to_execute, \
                                                    self.data_mockup)
        self.status_code = self.status_code + request_status_code
        self._model.fill_data_wrapper(self.data_mockup.view_result_to_parse)
                    
        self.current_operation = State.PREPARE_AGENTS
    
    def operate_request(self):
        request_status_code = self.execute_request(self.objects_to_execute, \
                                                    self.data_mockup)
        self.status_code = self.status_code + request_status_code
        self.current_operation = State.FINISH
        if not self.is_test:
            self._view.logger_print(self.current_operation, "INFO", self.status_code)
        
    def print_current_operation(self, current_operation, data_mockup):
        if current_operation == State.OPERATE_REQUEST:
            operation = str(current_operation) + " '" + \
                str(data_mockup.view_operation) + "'" + \
                " using: " + str(data_mockup.view_operation_type)
            self._view.logger_print(operation, "INFO")
            return 
        elif current_operation == State.GET_CLUSTERS_DATA or \
        current_operation == State.PARSE_REQUEST:
            self._view.logger_print(current_operation, "INFO")
            return
        self._view.logger_print(current_operation, "DEBUG")
    
    def get_request(self):
        # controller receives arguments from view
        user_request =  self._queue.get()
        if len(user_request) == 0:
            raise Exception("No arguments")
        return user_request
    
    def parse_request(self, user_request):
        # controller orders model to handle user request
        is_test, target_type = self._model.handle_user_request(user_request)
        return is_test, target_type
    
    def execute_request(self, agents_list, data_mockup, status_code = 0):
        agents_executor = Executor()
        # controller sends ready agent objects to execute
        for agent in agents_list:
            agents_executor.execute(agent, data_mockup)
            try:
                status_code += self._view.handle_output(data_mockup, \
                                                    agent.is_get_domain_data_op)
            # in case of NMAgent
            except AttributeError: status_code += self._view.handle_output(data_mockup, \
                                                    False)
        return status_code
 
    def exit(self, status_code, is_test):
        #print "DEBUG: "+str(is_test)
        if not is_test:
            sys.exit(status_code)
        return

    def handle_exception(self, exception, status_code):
        ''' Sending exception to the View and finishing program with status code '''  
        status_code = 1 if status_code == 0 else status_code
        self._view.logger_print(exception, "ERROR", status_code) 
        exit(1)
