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
from parsing_rules import ParsingRulesSetter
from argument_validation import ArgumentValidator
from argument_interpretation import ArgumentInterpretator

class RequestParser(object):
    '''
    Class - module facade, responsible for parsing user request.
    '''

    def __init__(self):
        '''Constructor'''
        self.parser = ParsingRulesSetter()
        self.validator = ArgumentValidator(self.parser.parser)
        self.interpretator = ArgumentInterpretator()
        
    def parse(self, request, data_wrapper):
        '''Parsing, validating and interpretating user request'''
        args = self.parser.set_parser_rules(request, data_wrapper)
        is_test = self.interpretator.interpretate_args(data_wrapper, args, request)
        self.validator.validate_args(data_wrapper, args, request)
        
        return is_test