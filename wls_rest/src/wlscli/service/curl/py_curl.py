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

This module hides PyCurl library abstraction and implements Curl functionality.

'''
from io import BytesIO
import json, pycurl
from wlscli.common.error import AuthenticationError
    
class CurlAgent(object):
    '''
    Class representing REST agent (pycurl wrapper)
    - object containing all data necessary to perform Curl request
    '''

    def __init__(self, data_contract):
        ''' Constructor '''
        self.curl_agent = pycurl.Curl()
        self.raw = False
        self.WRITEFUNCTION = self.curl_agent.WRITEFUNCTION
        
        self.optional_data_dispatcher = {
            pycurl.POST: 1,
            pycurl.POSTFIELDS: data_contract.postfield,
            pycurl.NETRC: data_contract.netrc,
            pycurl.USERPWD: data_contract.user_pwd, 
            pycurl.COOKIEJAR: data_contract.cookie_jar,
            pycurl.COOKIEFILE: data_contract.cookie_file, 
        }
        self.set_compulsory_opts(data_contract)
        self.set_optional_opts(data_contract)

    def set_compulsory_opts(self, data_contract):
        self.curl_agent.setopt(pycurl.URL, str(data_contract.url))
        self.curl_agent.setopt(pycurl.CAINFO, data_contract.certs)
        self.curl_agent.setopt(pycurl.HTTPHEADER, data_contract.http_header)
        self.curl_agent.setopt(pycurl.SSL_VERIFYPEER, data_contract.ssl_verifypeer) 
        self.raw = data_contract.raw
    
    def set_optional_opts(self, data_contract):
        
        if data_contract.netrc is not None:
            self.setopt(pycurl.NETRC, data_contract.netrc)

        if data_contract.user_pwd is not None:
            self.setopt(pycurl.USERPWD, data_contract.user_pwd)
        
        if data_contract.cookie_jar is not None:
            self.setopt(pycurl.COOKIEJAR, data_contract.cookie_jar)
            
        if data_contract.cookie_file is not None:
            self.setopt(pycurl.COOKIEFILE, data_contract.cookie_file)
        
        if data_contract.postfield is not None:
            self.setopt(pycurl.POSTFIELDS, data_contract.postfield)
            self.setopt(pycurl.POST, 1)
            
        if data_contract.verbose is not None:
            self.curl_agent.setopt(pycurl.VERBOSE, 1)
            
        if data_contract.delete:
            self.curl_agent.setopt(pycurl.CUSTOMREQUEST, "DELETE") 
        
        try:
            send = [("model", data_contract.model), ('deployment', \
                    (pycurl.FORM_FILE, data_contract.form_file)),]
            self.curl_agent.setopt(pycurl.HTTPPOST, send)   
        except (KeyError, TypeError): 
            try:
                send = [('deployment', \
                    (pycurl.FORM_FILE, data_contract.form_file)),]
                self.curl_agent.setopt(pycurl.HTTPPOST, send)   
            except TypeError: pass
        
    def close(self):
        ''' closing pycurl object '''
        self.curl_agent.close()
            
    def setopt(self, key, value):
        ''' setting parameter to the pycurl object '''
        try:
            self.curl_agent.setopt(key, value)
        except TypeError: pass
        
    def get_http_code(self):
        return self.curl_agent.getinfo(pycurl.HTTP_CODE)
        
    def execute(self):
        data = BytesIO()
        result = 0
        
        self.curl_agent.setopt(self.curl_agent.WRITEFUNCTION, data.write)
        try:
            self.curl_agent.perform()
            http_code = self.get_http_code()
            result = 0 if http_code >= 200 and http_code < 300 else 1
            self.curl_agent.close()
            dictionary = json.loads(data.getvalue())
            if self.raw:
                dictionary = json.dumps(dictionary, indent = 4, sort_keys = True)
        except ValueError as exception:
            if http_code == 401:
                raise AuthenticationError("Unauthorised")
            raise Exception(exception)
        
        except pycurl.error as exception:
            msg = str(exception) if exception[0] != 26 else \
                str(exception) + ". Please check file path if passed."
            raise Exception(msg)
        
        return result, dictionary
