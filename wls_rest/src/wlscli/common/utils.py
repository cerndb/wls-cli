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
Created on Jul 23, 2015

@author: Konrad Kaczkowski
'''
from enum import Enum

class Operation(object):
    '''
    Enumeration class that represents program operations
    '''
    
    class Server(Enum):
        SUSPEND = (0, "suspend servers")
        RESUME = (1, "resume servers")
        START = (2, "start servers")
        STOP = (3, "stop servers")
        STATUS = (4, "status servers")
        RESTART = (5, "restart servers")
    
    class AdmChange(Enum):
        START_CHANGES = (6, "start admin changes")
        CANCEL_CHANGES = (7, "cancel admin changes")
        ACTIVATE_CHANGES = (8, "activate admin changes")
        
    class App(Enum):
        START = (9, "start an app")
        STOP = (10, "stop an app")
        STATUS = (11, "status app")
        UPDATE = (12, "update an app")
        
    class Deployment(Enum):
        DEPLOY_LOCAL_APP = (13, "deploy an app from local source")
        DEPLOY_UPLOADED_APP = (14, "deploy uploaded app")
        DEPLOY_LOCAL_LIB = (15, "deploy a library from local source")
        DEPLOY_UPLOADED_LIB = (16, "deploy uploaded lib")
        REDEPLOY_LOCAL_APP = (17, "redeploy an app from local source")
        REDEPLOY_UPLOADED_APP = (18, "redeploy uploaded app")
        REDEPLOY_LOCAL_LIB = (19, "redeploy a lib from local source")
        REDEPLOY_UPLOADED_LIB = (20, "redeploy uploaded lib")
        UNDEPLOY_APP = (21, "undeploy an app")
        UNDEPLOY_LIB = (22, "undeploy a library")
            
    class Show(Enum):
        LIBRARIES = (23, "show libraries")
        APPS = (24, "show apps")
        TARGETS = (25, "show targets")
        JOBS = (26, "show jobs")
        
    class Logs(Enum):
        HTTP_ACCESS = (27, "show HTTP access logs")
        DATASOURCE = (28, "show datasource logs")
        SERVER = (29, "show server logs")
        DOMAIN = (30, "show domain logs")
        
    class PreService(Enum):
        CHECK_AUTHENTICATION = (31, "check credentials")
        GET_DOMAIN_DATA = (32, "get domain data")
        GET_CERN_DATA = (33, "get CERN specific data")
  
class State(Enum):
    '''
    Enumeration class that represents possible entity specifications
    '''
    GET_EVENT = (0, "Started processing.")
    AUTHENTICATE = (1, "Authenticating.")
    GET_CLUSTERS_DATA = (2, "Getting domain data (servers, clusters) using: REST.")
    PREPARE_MODEL = (3, "Preparing model.")
    PREPARE_AGENTS = (4, "Preparing request.")
    OPERATE_REQUEST = (5, "Operating request:")
    FINISH = (6, "Finish.")
        
class AuthOperation(Enum):
    '''
    Enum class that represents authorisation operations
    '''
    COOKIE = (0, "interactive, auth with cookie")
    INTERACTIVE = (1, "interactive, authorisation without cookie")
    NETRC = (2, "auth with .netrc")
    SCRIPT = (3, "auth with script")
    CREDS_IN_PARAMETERS = (4, "credentials given in parameters")
    CERN_DATA = (5, "auth with CERN infr")
    
class RequestType(object):
    REST = 0
    NM = 1
    
class MessageType(object):
    INFO = 0
    DEBUG = 1
    ERROR = 2
    JSON = 3
    STATUS_CODE = 4
    
class TargetType(object):
    '''
    Enumeration class that represents possible target types
    '''
    SERVER = 0
    CLUSTER = 1
    DOMAIN = 2
    APP = 3
    LIB = 4
    NO_TARGET = 5
    
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
class Mockup(object):
    '''
    Mockup class for View layer
    '''
    def __init__(self, message_type, message):
        ''' Constructor '''
        self.raw = False
        self.test = False
        self.servlets = False
        self.long_print = False
        self.status_code = -1
        self.message_type = message_type
        self.message = message
    