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
import os

class CookieAuthenticationService(AuthenticationService):
    
    def __init__(self, data_storage):
        ''' Constructor '''
        self.data_storage = data_storage
        self.cookie_manager = CookieManager()
        
    def get_data(self):
        cookie_path = self.cookie_manager.cookie_path
        self.data_storage.cookie_path = cookie_path
        
    def invalidate_cookie(self):
        self.cookie_manager.invalidate_cookie()
        
class CookieManager(object):
    '''
    Class responsible for handling HTTP cookie.
    '''
    
    def __init__(self):
        ''' Constructor '''
        home_directory = os.path.expanduser("~")
        cookie_name = "wls_cookie"
        self.cookie_path = home_directory + "/" + cookie_name
    
    def check_cookie(self):
        ''' checks if cookie token exists and is not empty'''
        return os.path.isfile(self.cookie_path) and \
            os.path.getsize(self.cookie_path) > 0
        
    def invalidate_cookie(self):
        ''' deletes cookie jar with cookie '''
        try:
            os.remove(self.cookie_path)
        except OSError: pass