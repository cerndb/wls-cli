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
import os.path

class CookieHandler(object):
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
    
    def get_cookiejar(self):
        ''' creates cookie jar, returns its path '''
        need_get_creds = False
        if not self.check_cookie():
            self.invalidate_cookie()
            cookie_jar = open(self.cookie_path, 'w+')
            cookie_jar.close()
            need_get_creds = True
        return self.cookie_path, need_get_creds
        
    def invalidate_cookie(self):
        ''' deletes cookie jar with cookie '''
        try:
            os.remove(self.cookie_path)
        except OSError: pass