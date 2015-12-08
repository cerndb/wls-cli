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
Created on Nov 4, 2015

@author: Konrad Kaczkowski
'''
from wlscli.service.security import AuthenticationService
from wlscli.service.security.data.data_access import PasswdGetter

class ScriptAuthenticationService(AuthenticationService):
    
    def __init__(self, data_storage):
        ''' Constructor '''
        self.data_storage = data_storage
        self.data_getter = PasswdGetter()
        
    def get_data(self):
        if self.data_storage.username == None:
            raise Exception ("Username was not specified.")
        self.data_getter.get_script_data(self.data_storage)
        
        self.data_storage.user_pwd = (self.data_storage.username + ":" + self.data_storage.passwd).strip()