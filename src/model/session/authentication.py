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
import os
from token import CookieHandler
from common.utils import AuthOperation

class AuthenticationManager(object):
    '''
    Class responsible for setting authentication curl parameters.
    '''
    
    def __init__(self, data_wrapper, data_getter):
        ''' Constructor '''
        self.credentials_manager = CredentialsManager()
        self.cookie_handler = CookieHandler()
        self.data_wrapper = data_wrapper
        self.data_getter = data_getter
        
        self.operation_mapping = {AuthOperation.COOKIE: self.operate_cookie,
           AuthOperation.INTERACTIVE: self.operate_get_credentials,
           AuthOperation.COOKIE_CRED: self.operate_get_credentials,
           AuthOperation.NETRC: self.operate_netrc,
           AuthOperation.SCRIPT: self.operate_script,
           AuthOperation.CERN_DATA: self.operate_CERN_data,
           AuthOperation.CREDS_IN_PARAMETERS: self.operate_credentials_already_given }
        
    def set_auth_data(self):
        auth_operation = self.data_wrapper.auth_operation
        self.operation_mapping[auth_operation]()
     
    def operate_cookie(self):
        self.data_wrapper.cookie_path, need_get_creds = self.cookie_handler.get_cookiejar()
        need_get_creds = need_get_creds if self.data_wrapper.usession else True
            
        if need_get_creds:
            self.data_wrapper.auth_operation = AuthOperation.COOKIE_CRED
            self.get_credentials()
        
    def operate_get_credentials(self):
        self.get_credentials()
        
    def operate_credentials_already_given(self):
        pass
    
    def operate_netrc(self):
        home_directory = os.path.expanduser("~")
        netrc_path = home_directory + "/.netrc"
        self.check_file_exists(netrc_path)
    
    def operate_script(self):
        if self.data_wrapper.username == None:
            raise Exception ("Username was not specified.")
        self.data_getter.get_script_data(self.data_wrapper)
    
    def operate_CERN_data(self):
        self.data_getter.get_CERN_specific_data(self.data_wrapper)
        
    def get_credentials(self):
        self.data_wrapper.username = self.credentials_manager.get_username()
        self.data_wrapper.passwd = self.credentials_manager.get_password()
        
    def set_cookie(self, curl_agent):
        token_path = self.cookie_handler.get_cookiejar()
        curl_agent.setopt(pycurl.COOKIEFILE, token_path)
        
    def invalidate_cookie(self):
        self.cookie_handler.invalidate_cookie()
        
    def check_file_exists(self, file_to_check):
        ''' Checking if file specified in parameter exists. '''
        if not os.path.isfile(file_to_check):
            raise Exception(file_to_check + " not found!")
    
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