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
Created on Oct 31, 2015

@author: Konrad Kaczkowski
'''

from wlscli.service.curl import CurlDataContract
from wlscli.service.curl import CurlManager
from wlscli.common.utils import MessageType
from wlscli.common.utils import Operation

class ApplicationManager(object):
    def __init__(self, model):
        ''' Constructor '''
        self.model = model
        self.curl_manager = CurlManager()
        
    def run(self, operation):
        target = self.model.data_storage.target 
        target = target if target is not None else self.model.data_storage.deployment_name
        
        uri = self.model.get_uri(operation, target)
        data_contract = self.create_curl_data(uri, operation)
        self.curl_manager.create_agent(data_contract)
        result, output = self.curl_manager.execute_agent()  
        
        self.model.update(MessageType.JSON, output)
        self.model.update(MessageType.STATUS_CODE, result)
        
        return int(result)
            
    def create_curl_data(self, uri, operation):
        data_contract = CurlDataContract()
        data_storage = self.model.data_storage
        data_contract.url = data_storage.adminserver_url + uri
        data_contract.certs = data_storage.curl_certs
        data_contract.user_pwd = data_storage.user_pwd
        data_contract.cookie_file = data_storage.cookie_path
        data_contract.cookie_jar = data_storage.cookie_path
        data_contract.netrc = data_storage.netrc
        data_contract.ssl_verifypeer = True if not data_storage.test else False
        if operation != Operation.App.STATUS:
            data_contract.set_empty_postfield()    
        
        return data_contract