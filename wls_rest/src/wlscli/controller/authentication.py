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
Created on Aug 17, 2015

@author: Konrad Kaczkowski
'''
import getpass
import pycurl
from wlscli.service.main import WeblogicServicesFactory
from wlscli.common.utils import Operation
from wlscli.common.error import AuthenticationError

class AuthenticationController(object):
    '''
    Class responsible for setting authentication curl parameters.
    '''
    
    def __init__(self, model):
        ''' Constructor '''
        self.model = model
        self.data_wrapper = model.data_storage
        self.service_manager = WeblogicServicesFactory(Operation.PreService, model)
        
    def process_authentication(self, authentication_operation):
        
        try:
            # try to connect to the server
            self.service_manager.check_authentication(authentication_operation)
            self.model.update("Authentication succeeded")
        except AuthenticationError:
            self.service_manager.reauthenticate(authentication_operation)