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
Created on Oct 26, 2015

@author: Konrad Kaczkowski
'''

from wlscli.model.data import data_containers

class DataStorage(object):
    '''
    Facade class for the data that is needed during processing request.
    '''
    def __init__(self):
        ''' Constructor - subclasses creation '''
        self._settings_wrapper = data_containers.SettingsProperties()
        self._user_wrapper = data_containers.UserProperties()
        self._view_wrapper = data_containers.ViewProperties()
        self._domain_wrapper = data_containers.DomainProperties()
        self._cern_data_wrapper = data_containers.CERNSpecificProperties()
        
    def __setattr__(self, attribute, value):
        ''' Setter that is reaching subclasses for setting attribute '''
        if attribute[0] == '_':
            return super(DataStorage, self).__setattr__(attribute, value)
        
        if hasattr(self._settings_wrapper, attribute):
            return setattr(self._settings_wrapper, attribute, value)
        elif hasattr(self._user_wrapper, attribute):
            return setattr(self._user_wrapper, attribute, value)
        elif hasattr(self._view_wrapper, attribute):
            return setattr(self._view_wrapper, attribute, value)
        elif hasattr(self._domain_wrapper, attribute):
            return setattr(self._domain_wrapper, attribute, value)
        elif hasattr(self._cern_data_wrapper, attribute):
            return setattr(self._cern_data_wrapper, attribute, value)

        
    def __getattr__(self, attribute):
        ''' Getter that is reaching subclasses for getting attribute '''
        try:
            return getattr(self._settings_wrapper, attribute)
        except AttributeError: pass
        try:
            return getattr(self._domain_wrapper, attribute)
        except AttributeError: pass
        try:
            return getattr(self._user_wrapper, attribute)
        except AttributeError: pass
        try:
            return getattr(self._view_wrapper, attribute)
        except AttributeError: pass
        try:
            return getattr(self._cern_data_wrapper, attribute)
        except AttributeError: pass