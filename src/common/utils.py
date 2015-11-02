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
Created on Jul 23, 2015

@author: Konrad Kaczkowski
'''

class EnumMeta(type):
    '''
    Meta class that describes behaviour of its classes
    '''
    def __getattribute__(self, name):
        actual_value = super(EnumMeta, self).__getattribute__(name)
        if isinstance(actual_value, self):
            return actual_value
        else:
            new_value = self(actual_value)
            super(EnumMeta, self).__setattr__(name, new_value)
            return new_value
    
class Enum(object):
    '''
    Class that represents Enumeration with two values:
    - int (id)
    - str (operation description)
    '''
    __metaclass__ = EnumMeta

    def __init__(self, value):
        ''' Constructor '''
        super(Enum, self).__init__()

        self.value = value[0]
        self.repr = value[1]

    def __repr__(self):
        ''' returns string representation '''
        return str(self.repr)

class Operation(Enum):
    '''
    Enumeration class that represents program operations
    '''
    SUSPEND_SERVERS = (0, "suspend servers")
    RESUME_SERVERS = (1, "resume servers")
    START_SERVERS = (2, "start servers")
    START_APP = (3, "start an app")
    STOP_SERVERS = (4, "stop servers")
    STOP_APP = (5, "stop an app")
    STATUS_SERVERS = (6, "status servers")
    STATUS_APP = (7, "status app")
    RESTART_SERVERS = (8, "restart servers")
    REDEPLOY_LOCAL_APP = (9, "redeploy an app from local source")
    REDEPLOY_UPLOADED_APP = (10, "redeploy uploaded app")
    REDEPLOY_LOCAL_LIB = (11, "redeploy a lib from local source")
    REDEPLOY_UPLOADED_LIB = (12, "redeploy uploaded lib")
    UPDATE_APP = (13, "update an app")
    LIST_LIBRARIES = (14, "show libraries")
    LIST_APPS = (15, "show apps")
    LIST_TARGETS = (16, "show targets")
    SHOW_HTTP_ACCESS_LOGS = (17, "show HTTP access logs")
    SHOW_DATASOURCE_LOGS = (18, "show datasource logs")
    SHOW_SERVER_LOGS = (19, "show server logs")
    SHOW_DOMAIN_LOGS = (20, "show domain logs")
    START_ADMIN_CHANGES = (21, "start admin changes")
    CANCEL_ADMIN_CHANGES = (22, "cancel admin changes")
    ACTIVATE_ADMIN_CHANGES = (23, "activate admin changes")
    DEPLOY_LOCAL_APP = (24, "deploy an app from local source")
    DEPLOY_UPLOADED_APP = (25, "deploy uploaded app")
    DEPLOY_LOCAL_LIB = (26, "deploy a library from local source")
    DEPLOY_UPLOADED_LIB = (27, "deploy uploaded lib")
    UNDEPLOY_APP = (28, "undeploy an app")
    UNDEPLOY_LIB = (29, "undeploy a library")
    SHOW_JOBS = (30, "show jobs")
    GET_DOMAIN_DATA = (31, "get domain data")
    
class State(Enum):
    '''
    Enumeration class that represents possible entity specifications
    '''
    PARSE_REQUEST = (0, "Started parsing request.")
    PREPARE_MODEL = (1, "Preparing model.")
    PREPARE_AGENTS = (2, "Preparing request.")
    GET_CLUSTERS_DATA = (3, "Getting domain data (servers, clusters) using: REST.")
    AUTHENTICATE = (4, "Authenticating.")
    OPERATE_REQUEST = (5, "Operating request:")
    RENEW_COOKIE = (6, "Authentication failed.")
    FINISH = (7, "Finish.")
        
class AuthOperation(Enum):
    '''
    Enum class that represents authorisation operations
    '''
    COOKIE = (0, "interactive, auth with cookie")
    COOKIE_CRED = (1, "interactive, auth with cookie - need to get credentials")
    INTERACTIVE = (2, "interactive, authorisation without cookie")
    DESTROY_COOKIE = (3, "destroy cookie")
    NETRC = (4, "auth with .netrc")
    SCRIPT = (5, "auth with script")
    CREDS_IN_PARAMETERS = (6, "credentials given in parameters")
    CERN_DATA = (7, "auth with CERN infr")
    
class TargetType():
    '''
    Enumeration class that represents possible target types
    '''
    SERVER = 0
    CLUSTER = 1
    DOMAIN = 2
    APP = 3
    LIB = 4
    NO_TARGET = 5
    
class AuthenticationError(Exception):
    pass
    