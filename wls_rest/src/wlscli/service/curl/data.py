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
import json

class CurlDataContract(object):
    
    def __init__(self):
        self.url = None
        self.http_header = ['X-Requested-By: MyClient','Content-Type: application/json' , \
                                 'Accept: application/json']
        self.certs = None
        self.timeout = None
        self.connect_timeout = None
        self.verbose = None
        self.user_pwd = None
        self.cookie_file = None
        self.cookie_jar = None
        self.postfield = None
        self.form_file = None
        self.model = None
        self.netrc = None
        self.ssl_verifypeer = True
        self.raw = False
        self.delete = False
        
    def set_postfield(self, deployment_name, path, target):
        self.postfield = json.dumps({"name": deployment_name, \
                            "deploymentPath": path, \
                            "targets": target } )
            
    def set_form_file(self, deployment_name, path, target):
        self.model = json.dumps({"name": deployment_name, \
                            "targets": target } )
        self.form_file = path
        self.http_header = ['X-Requested-By: MyClient','Content-Type: multipart/form-data' , \
                                 'Accept: application/json']
            
    def set_delete(self):
        self.delete = True
        
    def set_empty_postfield(self):
        self.postfield = json.dumps(None)
        