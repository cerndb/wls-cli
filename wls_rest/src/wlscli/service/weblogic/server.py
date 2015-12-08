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

from wlscli.common.utils import Operation
from wlscli.common.utils import TargetType
from wlscli.service.curl import CurlDataContract
from wlscli.service.curl import CurlManager
from wlscli.common.utils import MessageType
from wlscli.service.node_manager import NMManager
from wlscli.service.node_manager import NMDataContract
from wlscli.common import Constans
import time

class ServersManager(object):
    
    def __init__(self, model):
        ''' Constructor '''
        self.model = model
    
    def run(self, operation):
        target_type = self.model.data_storage.target_type
        result = 0
        self.server_service = ServerService(self.model)
        
        if target_type == TargetType.CLUSTER:
            result += self.execute_cluster(operation)         
        elif target_type == TargetType.DOMAIN:
            result += self.execute_domain_request(operation)        
        else:
            if self.model.data_storage.target == Constans.ADMINSERVER_NAME and \
                (operation == Operation.Server.START or operation == Operation.Server.STOP):
                result += self.server_service.run_NM(operation)
            else:
                result += self.server_service.run(operation, self.model.data_storage.target)
            
        self.model.update(MessageType.STATUS_CODE, result)
    
    def execute_cluster(self, operation):
        result = 0
        # delegate further processing to the cluster manager
        cluster_manager = ClusterDataService(self.model)
        result += cluster_manager.run()
        #for cluster in self.model.data_storage.clusters.itervalues():
        cluster = self.model.data_storage.clusters.get(self.model.data_storage.target)
        for server in cluster:
            result += self.server_service.run(operation, server)
        return result
            
    def execute_domain_request(self, operation):
        result = 0
        # delegate further processing to the cluster manager
        cluster_manager = ClusterDataService(self.model)
        
        if operation == Operation.Server.START:
            #result += self.server_service.run(operation, self.model.data_storage.adminserver_name)
            result += self.server_service.run_NM(operation)
            if result != 0: 
                time.sleep(10)
        
        result += cluster_manager.run()
        
        if operation == Operation.Server.STATUS:
            result += self.server_service.run(operation, self.model.data_storage.adminserver_name)
            
        for cluster in self.model.data_storage.clusters.itervalues():
            for server in cluster:
                result += self.server_service.run(operation, server)
                
        if operation == Operation.Server.STOP:
            #result += self.server_service.run(operation, self.model.data_storage.adminserver_name)
            result += self.server_service.run_NM(operation)
        return result
    
class ServerService(object):
    
    def __init__(self, model):
        ''' Constructor '''
        self.model = model
        self.curl_manager = CurlManager()
        self.nm_manager = NMManager()
        self.curl_data_dispatcher = {Operation.Server.START: self.create_curl_POST_data,
                                     Operation.Server.STOP: self.create_curl_POST_data,
                                     Operation.Server.STATUS: self.create_curl_data,
                                     Operation.Server.RESTART: self.create_curl_POST_data,
                                     Operation.Server.SUSPEND: self.create_curl_POST_data,
                                     Operation.Server.RESUME: self.create_curl_POST_data}
    
    def run(self, operation, target):
        uri = self.model.get_uri(operation, target)
        uri = self.modify_uri(uri)
        data_contract = self.curl_data_dispatcher[operation](uri)
        self.curl_manager.create_agent(data_contract)
        result, output = self.curl_manager.execute_agent()  
        self.model.update(MessageType.JSON, output)
        return int(result)
    
    def run_NM(self, operation):
        data_contract = self.create_nm_data(operation)
        self.nm_manager.create_agent(data_contract)
        result, output = self.nm_manager.execute_agent()  
        self.model.update(MessageType.INFO, output)
        return int(result)
    
    def create_nm_data(self, operation):
        data_contract = NMDataContract()
        data_storage = self.model.data_storage
        data_contract.target = Constans.ADMINSERVER_NAME
        data_contract.operation = "START" if operation == Operation.Server.START else "KILL"
        data_contract.wls_dir = data_storage.wls_dir
        data_contract.domain_name = data_storage.domain_name
        data_contract.domain_dir = data_storage.domain_dir
        return data_contract
            
    def create_curl_data(self, uri):
        data_contract = CurlDataContract()
        data_storage = self.model.data_storage
        data_contract.url = data_storage.adminserver_url + uri
        data_contract.certs = data_storage.curl_certs
        data_contract.user_pwd = data_storage.user_pwd
        data_contract.cookie_file = data_storage.cookie_path
        data_contract.cookie_jar = data_storage.cookie_path
        data_contract.netrc = data_storage.netrc
        data_contract.ssl_verifypeer = True if not self.model.data_storage.test else False
        return data_contract
    
    def create_curl_POST_data(self, uri):
        data_contract = self.create_curl_data(uri)
        data_contract.set_empty_postfield()    
        return data_contract
    
    def modify_uri(self, uri):
        modified_uri = uri
        data_storage = self.model.data_storage
        
        if data_storage.forceOperation:
            modified_uri += "?force=true"
        
        return modified_uri
        

class ClusterDataService(object):
    
    def __init__(self, model):
        ''' Constructor '''
        self.model = model
        self.curl_manager = CurlManager()
    
    def run(self):
        uri = "/management/tenant-monitoring/clusters"
        data_contract = self.create_curl_data(uri)
        self.curl_manager.create_agent(data_contract)
        result, json_data = self.curl_manager.execute_agent()
        self.model.data_storage.clusters = self.map_cluster_data_from_REST(json_data)
        self.model.update(MessageType.INFO, "Retrieved clusters data")
        #self.model.update(MessageType.JSON, json_data)
        return int(result)
            
    def create_curl_data(self, uri):
        data_contract = CurlDataContract()
        data_storage = self.model.data_storage
        data_contract.url = data_storage.adminserver_url + uri
        data_contract.certs = data_storage.curl_certs
        data_contract.user_pwd = data_storage.user_pwd
        data_contract.cookie_file = data_storage.cookie_path
        data_contract.cookie_jar = data_storage.cookie_path
        data_contract.netrc = data_storage.netrc
        data_contract.ssl_verifypeer = True if not data_storage.test else False
        return data_contract
    
    def map_cluster_data_from_REST(self, json_data):
        ''' Interpreting the data from the request - servers and clusters data. '''
        clusters = dict() 
        
        for cluster_data in json_data["body"]["items"]:
            cluster = list()
            for server in cluster_data["servers"]:
                cluster.append(server["name"])
            clusters[cluster_data["name"]] = cluster
            
        return clusters