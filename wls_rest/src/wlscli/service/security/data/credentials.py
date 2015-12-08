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
import getpass

class CredentialsAuthenticationService(AuthenticationService):
    
    def __init__(self, data_storage):
        ''' Constructor '''
        self.data_storage = data_storage
        self.credentials_manager = CredentialsManager()
        
    def get_data(self):
        username, passwd = self.get_credentials_from_user()
        self.set_credentials_passwd(username, passwd)
        
    def get_credentials_from_user(self):
        username = self.credentials_manager.get_username()
        passwd = self.credentials_manager.get_password()   
        return username, passwd 
        
    def set_credentials_passwd(self, username, passwd):
        self.data_storage.user_pwd = \
        (username + ":" + passwd).strip()

class CredentialsManager(object):
    '''
    Class responsible for getting credentials from a user
    '''
    
    def get_username(self):
        ''' getting username from a user '''
        print "Username: ",
        username = raw_input()
        return username
        
    def get_password(self):
        ''' getting password from a user '''
        passwd = getpass.getpass("Give password: ")
        return passwd