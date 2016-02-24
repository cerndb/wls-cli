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

from wlscli.model.application_logic import DataStorage
from wlscli.common.observer import Observable
from wlscli.common.utils import Operation
from wlscli.model import business_logic
from wlscli.common.utils import Mockup

class Model(Observable):
    '''
    Model class - facade. Handles business logic: delegates user request to be parsed, 
    creates agents to be executed by Controller.
    '''

    def __init__(self):
        ''' Constructor '''
        super(Model, self).__init__()
        self.data_storage = DataStorage()
        self.message = ""
        self.object_dispatcher = {Operation.Server: business_logic.Servers,
                Operation.App: business_logic.Deployments,
                Operation.Deployment: business_logic.Deployments,
                Operation.Logs: business_logic.Logs,
                Operation.Show: self.get_show_object,
                Operation.AdmChange: business_logic.ChangeManager}
     
    def update(self, message_type, message):
        mockup = Mockup(message_type, message)
        mockup.raw = self.data_storage.raw
        mockup.long_print = self.data_storage.long
        mockup.test = self.data_storage.test
        super(Model, self).update_observers(mockup)
        
    def get_uri(self, operation, target = None):
        self.operation = operation
        business_object = self.object_dispatcher[type(operation)]()
        try:
            return business_object.get_uri(operation, target)
        except TypeError: return business_object.get_uri(operation)
        
    def get_show_object(self):
        
        object_dispatcher = {Operation.Show.TARGETS: business_logic.Targets,
                Operation.Show.JOBS: business_logic.Jobs,
                Operation.Show.APPS: business_logic.Deployments,
                Operation.Show.LIBRARIES: business_logic.Deployments}
        
        return object_dispatcher[self.operation]()
        
    def register_observer(self, observer):
        super(Model, self).register(observer)
