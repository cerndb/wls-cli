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
Created on May 29, 2015

@author: Konrad Kaczkowski
'''

from wlscli.controller.console.parsing_rules import ParsingRulesSetter
from wlscli.controller.console.argument_validation import ArgumentValidator
from wlscli.controller.console.argument_interpretation import ArgumentInterpreter
from wlscli.common.decorator import Decorator
from wlscli.common.utils import Operation
from wlscli.common.utils import TargetType
from wlscli.common.utils import MessageType

class ConsoleController(Decorator):
    '''
    Class - module facade, responsible for parsing user request.
    '''
        
    def __init__(self, decorated):
        ''' Constructor '''
        self.decorated = decorated
        self.parser = ParsingRulesSetter()
        self.validator = ArgumentValidator(self.parser.parser)
        self.interpreter = ArgumentInterpreter()
        self.view_model = decorated.model.data_storage
    
    def get_request(self):
        ui_event = self.decorated.get_request()
        command = ui_event.command
        if len(command) == 0:
            raise Exception("No arguments in command.")
        return self.parse(command)
    
    def parse(self, command):
        '''Parsing, validating and interpretating user request'''
        args = self.parser.set_parser_rules(command)
        try:
            event = self.interpreter.interpret_args(self.view_model, args, command)
            self.validator.validate_args(event.operation, args, command)
        except Exception as exception: 
            self.decorated.model.update(MessageType.ERROR, str(exception))
            return 1
        event.view_model = self.view_model
        
        admin_start = event.operation == Operation.Server.START and \
            event.view_model.target == event.view_model.adminserver_name
            
        admin_stop = event.operation == Operation.Server.STOP and \
            event.view_model.target == event.view_model.adminserver_name
            
        domain_start = event.view_model.target_type == TargetType.DOMAIN and \
            event.operation == Operation.Server.START
        
        event.omit_auth = self.view_model.test or admin_start or \
            admin_stop or domain_start
        return event