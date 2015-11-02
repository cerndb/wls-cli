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
Created on Jun 4, 2015

@author: Konrad Kaczkowski
'''
import pycurl, json
from common import LoggerWrapper
from common.utils import Operation
from common.utils import AuthOperation
from dictionary import StrategyDictionary
class RESTAgentCreator(object):
    '''
    Class responsible for creating agents executed with REST
    '''

    def __init__(self):
        ''' Constructor '''
        
    def create_agent(self, data_wrapper, command, target):
        ''' REST request construction - Curl parameters '''
        dictionary_wrapper = StrategyDictionary(command)
        dictionary = dictionary_wrapper.get_tuple()
        if_postfields = dictionary['postfields']
        http_method = dictionary['HTTP']
        operation = dictionary['REST']
        target_url = data_wrapper.adminserver_url
        url_context = dictionary['url_context']
        if target is not None and target != "":
            opt = self.create_url_opts(data_wrapper, command)
            url = target_url + url_context + target + "/" + operation + opt
        else:
            url = target_url + url_context + operation
        #self.logger_debug_print(url)
        curl_agent = RESTAgent(data_wrapper, url, http_method, if_postfields)
        return curl_agent
    
    def create_url_opts(self, data_wrapper, command):
        ''' adding additional parameters '''
        opt = "?__detached=true" if data_wrapper.async else ""
        if 'log' in repr(command): 
            opt = opt + "?maxResults=" + str(data_wrapper.maxResults)
        elif ('start' in repr(command) or 'stop' in repr(command)) \
        and data_wrapper.forceOperation:
            opt = opt + "?force=true"
        return opt
    
    def logger_debug_print(self, message):
        logger_wrapper = LoggerWrapper()
        logger_wrapper.logger.debug(message)
    
class RESTAgent(object):
    '''
    Class representing REST agent (pycurl wrapper)
    - object containing all data necessary to perform Curl request
    '''

    def __init__(self, data_wrapper, url, http_method, if_postfields):
        ''' Constructor '''
        self.curl_agent = pycurl.Curl()
        self.set_connection_parameters(data_wrapper, url)
        self.is_get_domain_data_op = data_wrapper.is_get_domain_data_op
        
        if data_wrapper.test:
            # equivalent to curl's --insecure
            self.curl_agent.setopt(pycurl.SSL_VERIFYPEER, False) 
        if(http_method == "POST" and not if_postfields):
            self.set_POST_without_postfields(data_wrapper)
        elif(http_method == "POST" and if_postfields):
            self.set_POST_with_postfields(data_wrapper)   
        elif(http_method == "DELETE"):
            self.curl_agent.setopt(pycurl.CUSTOMREQUEST, "DELETE") 
            
    def set_connection_parameters(self, data_wrapper, url):
        ''' setting connection parameters '''
        self.WRITEFUNCTION = self.curl_agent.WRITEFUNCTION
        self.curl_agent.setopt(pycurl.URL, str(url))
        self.curl_agent.setopt(pycurl.CAINFO, data_wrapper.curl_certs)
        self.curl_agent.setopt(pycurl.HTTPHEADER, ['X-Requested-By: MyClient',\
                                                   'Accept: application/json'])
        self.set_credentials(data_wrapper)
        
        self.curl_agent.setopt(pycurl.CONNECTTIMEOUT, data_wrapper.connect_timeout) 
        self.curl_agent.setopt(pycurl.TIMEOUT, data_wrapper.timeout)
        self.raw = data_wrapper.raw and not data_wrapper.is_get_domain_data_op
        if data_wrapper.verbose2:
            self.curl_agent.setopt(pycurl.VERBOSE, 1)
            
    def set_credentials(self, data_wrapper):
        auth_operation = data_wrapper.auth_operation
        if auth_operation == AuthOperation.COOKIE:
            cookie_path = data_wrapper.cookie_path
            self.curl_agent.setopt(pycurl.COOKIEFILE, cookie_path)
            
        elif auth_operation == AuthOperation.COOKIE_CRED:
            user_pwd = data_wrapper.username + ":" + data_wrapper.passwd
            self.curl_agent.setopt(pycurl.USERPWD, user_pwd)
            cookie_path = data_wrapper.cookie_path
            self.curl_agent.setopt(pycurl.COOKIEJAR, cookie_path)
            
        elif auth_operation == AuthOperation.CERN_DATA or \
        auth_operation == AuthOperation.CREDS_IN_PARAMETERS or \
        auth_operation == AuthOperation.INTERACTIVE or \
        auth_operation == AuthOperation.SCRIPT:
            user_pwd = (data_wrapper.CERN_username + ":" + data_wrapper.passwd).strip()
            self.curl_agent.setopt(pycurl.USERPWD, user_pwd)
            
        elif auth_operation == AuthOperation.NETRC:
            self.curl_agent.setopt(pycurl.NETRC, 1)
            
    def set_POST_without_postfields(self, data_wrapper):
        ''' setting POST method without postfield '''
        post = json.dumps(None)
        self.curl_agent.setopt(pycurl.POSTFIELDS, post)
        self.curl_agent.setopt(pycurl.POST, 1)
            
    def set_POST_with_postfields(self, data_wrapper):
        ''' setting POST method with postfield '''
        if data_wrapper.operation == Operation.DEPLOY_LOCAL_APP or \
        data_wrapper.operation == Operation.DEPLOY_LOCAL_LIB:
            self.set_deploy_local(data_wrapper)  
                
        elif data_wrapper.operation == Operation.DEPLOY_UPLOADED_APP or \
        data_wrapper.operation == Operation.DEPLOY_UPLOADED_LIB:
            self.set_deploy_uploaded(data_wrapper)
            
        elif data_wrapper.operation == Operation.REDEPLOY_LOCAL_APP or \
        data_wrapper.operation == Operation.REDEPLOY_LOCAL_LIB:
            self.set_redeploy_local(data_wrapper)
        elif data_wrapper.operation == Operation.REDEPLOY_UPLOADED_APP or \
        data_wrapper.operation == Operation.REDEPLOY_UPLOADED_LIB:
            self.set_redeploy_uploaded(data_wrapper)
            
    def set_deploy_uploaded(self, data_wrapper):   
        ''' setting deploy uploaded app / lib operation '''  
        path = data_wrapper.source
        data = json.dumps({"name": data_wrapper.deployment_name, \
                            "deploymentPath": path, \
                            "targets": data_wrapper.target } )
        self.curl_agent.setopt(pycurl.POST, 1)
        self.curl_agent.setopt(pycurl.POSTFIELDS, data)
        self.curl_agent.setopt(pycurl.HTTPHEADER, \
                            ['X-Requested-By: MyClient','Content-Type: application/json' , \
                             'Accept: application/json'])         
            
    def set_deploy_local(self, data_wrapper):   
        ''' setting deploy local app / lib operation '''    
        path = data_wrapper.source
        model = json.dumps({"name": data_wrapper.deployment_name, \
                            "targets": data_wrapper.target } )
        send = [("model", model), ('deployment', (pycurl.FORM_FILE, path)),]
        self.curl_agent.setopt(pycurl.HTTPPOST, send)   
        
    def set_redeploy_uploaded(self, data_wrapper):   
        ''' setting redeploy uploaded app / lib operation '''  
        path = data_wrapper.source
        data = json.dumps({"deploymentPath": path} )
        self.curl_agent.setopt(pycurl.POST, 1)
        self.curl_agent.setopt(pycurl.POSTFIELDS, data)
        self.curl_agent.setopt(pycurl.HTTPHEADER, \
                            ['X-Requested-By: MyClient','Content-Type: application/json' , \
                             'Accept: application/json'])         
            
    def set_redeploy_local(self, data_wrapper):   
        ''' setting redeploy local app / lib operation ''' 
        path = data_wrapper.source
        send = [('deployment', (pycurl.FORM_FILE, path))]
        self.curl_agent.setopt(pycurl.HTTPPOST, send)  
            
    def close(self):
        ''' closing pycurl object '''
        self.curl_agent.close()
            
    def setopt(self, key, value):
        ''' setting parameter to the pycurl object '''
        self.curl_agent.setopt(key, value)
        
    def get_http_code(self):
        return self.curl_agent.getinfo(pycurl.HTTP_CODE)
            
    def perform(self):
        ''' executing pycurl object '''
        self.curl_agent.perform()
        
        
        