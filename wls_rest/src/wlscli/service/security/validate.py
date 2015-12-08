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
from wlscli.service.curl import CurlDataContract
from wlscli.service.curl import CurlManager

class SecurityValidator(object):
    
    def __init__(self, data_storage):
        self.data_storage = data_storage
        self.curl_manager = CurlManager()
    
    def validate_security_data(self):
        data_contract = self.create_curl_data()
        self.curl_manager.create_agent(data_contract)
        self.curl_manager.execute_agent()
            
    def create_curl_data(self):
        data_contract = CurlDataContract()
        data_contract.url = self.data_storage.adminserver_url + \
             "/management/wls/latest"
        data_contract.certs = self.data_storage.curl_certs
        data_contract.user_pwd = self.data_storage.user_pwd
        data_contract.cookie_file = self.data_storage.cookie_path
        data_contract.cookie_jar = self.data_storage.cookie_path
        data_contract.netrc = self.data_storage.netrc
        data_contract.ssl_verifypeer = True if not self.data_storage.test else False
        
        return data_contract