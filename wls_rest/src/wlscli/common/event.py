#!/usr/bin/env python
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
Created on Oct 31, 2015
@author: Konrad Kaczkowski
'''
from utils import Operation

class UserEvent(object):
    pass

class ConsoleUIEvent(object):
    def __init__(self, command):
        ''' Constructor '''
        self.command = command
        
class AdminChangeEvent(UserEvent):
    def __init__(self, operation):
        ''' Constructor '''
        self.auth_operation = None
        self.operation = operation
    
class AppEvent(UserEvent):
    def __init__(self, operation):
        ''' Constructor '''
        self.auth_operation = None
        self.operation = operation
    
class DeploymentEvent(UserEvent):
    def __init__(self, operation):
        ''' Constructor '''
        self.auth_operation = None
        self.operation = operation
    
class LogsEvent(UserEvent):
    def __init__(self, operation):
        ''' Constructor '''
        self.auth_operation = None
        self.operation = operation
    
class ServerEvent(UserEvent):
    def __init__(self, operation):
        ''' Constructor '''
        self.auth_operation = None
        self.operation = operation
    
class ShowEvent(UserEvent):
    def __init__(self, operation):
        ''' Constructor '''
        self.auth_operation = None
        self.operation = operation
        
class EventFactory(object):
    types = { Operation.Server: ServerEvent, Operation.App: AppEvent, 
            Operation.Deployment: DeploymentEvent, Operation.Logs: LogsEvent, 
            Operation.Show: ShowEvent, Operation.AdmChange: AdminChangeEvent}

    def __new__(cls, operation):
        return EventFactory.types[type(operation)](operation)
    