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
from wlscli.service import ServiceManager
from wlscli.common.utils import MessageType
import sys

class Controller(object):
    '''
    Controller class - facade. Steering Model and View.
    '''

    def __init__(self, model, view, queue):
        ''' Constructor '''
        self.queue = queue
        self.model = model
        self.view = view
        self.service_manager = ServiceManager(self.model)
        self.model.register_observer(self)
        
    def run(self):
        ''' Main function that operates user request and executes it. '''
        event = self.get_request()
        try:
            self.service_manager.authorise(event.auth_operation, event.omit_auth)
            self.service_manager.execute_request(event.operation)
            
        except KeyboardInterrupt:
            self.model.update(MessageType.ERROR, "Interrupted by user")
        #except ArithmeticError as exception:   
        except Exception as exception:
            self.handle_exception(exception)
   
    def get_request(self):
        # controller receives arguments from view
        event = self.queue.get()
        return event
        
    def update(self, mockup):
        self.view.display(mockup)
        
    def handle_exception(self, exception):
        self.model.update(MessageType.ERROR, str(exception))
        self.model.update(MessageType.STATUS_CODE, 1)
        sys.exit(1)
