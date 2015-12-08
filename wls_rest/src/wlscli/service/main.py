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
Created on Oct 25, 2015

@author: Konrad Kaczkowski
'''
from wlscli.common.utils import Operation
import weblogic
from wlscli.common.utils import AuthOperation
from wlscli.service import security
from wlscli.common.error import AuthenticationError
from wlscli.service.security.validate import SecurityValidator
from wlscli.common.utils import MessageType

class ServiceManager(object):
    
    def __init__(self, model):
        ''' Constructor '''
        self.model = model
        self.service_objects_mapping = \
            {AuthOperation.COOKIE: security.CookieAuthenticationService,
             AuthOperation.NETRC: security.NetrcAuthenticationService,
             AuthOperation.SCRIPT: security.ScriptAuthenticationService,
             AuthOperation.CERN_DATA: security.CERNAuthenticationService,
             AuthOperation.CREDS_IN_PARAMETERS: security.CredentialsAuthenticationService,
             AuthOperation.INTERACTIVE: security.CredentialsAuthenticationService}
        
    def authorise(self, auth_operation, omit_auth):
        try:
            self.get_security_data(auth_operation)
            if not omit_auth:
                self.validate_security_data()
            
        except AuthenticationError:
            self.handle_authentication_error()
    
    def get_security_data(self, auth_operation):
        self.auth_operation = auth_operation
        security_service_object = \
            self.service_objects_mapping[auth_operation](self.model.data_storage)
        security_service_object.get_data()
    
    def validate_security_data(self):
        validator = SecurityValidator(self.model.data_storage)
        validator.validate_security_data()
        self.model.update(MessageType.INFO, "Authentication succeeded.")
            
    def execute_request(self, operation):
        self.service_object = WeblogicServicesFactory(type(operation), self.model)
        #process the request
        return self.service_object.run(operation)
        
    def handle_authentication_error(self):
        
        if self.auth_operation == AuthOperation.COOKIE:
            self.display_error_msg("Cookie expired.")
            self.authorise(AuthOperation.INTERACTIVE)
            
        elif self.auth_operation == AuthOperation.NETRC:
            self.display_error_msg("Credentials in .netrc are invalid.")
            raise Exception()
        
        elif self.auth_operation == AuthOperation.SCRIPT:
            self.display_error_msg("Credentials provided by user script are invalid.")
            raise Exception()
        
        elif self.auth_operation == AuthOperation.CERN_DATA:
            self.display_error_msg("Credentials provided by CERN infrastructure are invalid.")
            raise Exception()
        
        elif self.auth_operation == AuthOperation.CREDS_IN_PARAMETERS:
            self.display_error_msg("Credentials are invalid.")
            raise Exception()
            
        elif self.auth_operation == AuthOperation.INTERACTIVE:
            self.display_error_msg("Credentials are invalid.")
            self.authorise(self.auth_operation)
            
        else:
            raise Exception("Unrecognized auth operation")
        
    def display_msg(self, message):
        self.model.update(MessageType.INFO, message)
        
    def display_error_msg(self, message):
        self.model.update(MessageType.ERROR, message)
class WeblogicServicesFactory(object):
    types = { Operation.Server: weblogic.ServersManager, Operation.App: weblogic.ApplicationManager, 
            Operation.Deployment: weblogic.DeploymentManager, Operation.Logs: weblogic.LogsManager, 
            Operation.Show: weblogic.ShowManager, Operation.AdmChange: weblogic.ChangeManager}

    def __new__(cls, service_type, model):
        return WeblogicServicesFactory.types[service_type](model)