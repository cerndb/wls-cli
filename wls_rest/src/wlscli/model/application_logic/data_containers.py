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
Created on Jun 2, 2015

@author: Konrad Kaczkowski
'''

from wlscli.common import Constans

class UserProperties(object):
    '''
    Class storing properties that are set in user request
    '''
    current_operation = None
    #operation = None
    operation_type = None
    target_type = None
    target = None
    deployment_name = None
    source = None
    async = None
    verbose = None
    verbose2 = None

class ViewProperties(object):
    '''
    Class storing properties that have impact on view console
    '''
    long = False
    servlets = None
    raw = False

class SettingsProperties(object):
    '''
    Class storing properties that are general and set from default
    '''
    test = False
    is_get_domain_data_op = False
    timeout = Constans.TIMEOUT
    connect_timeout = Constans.CONNECT_TIMEOUT
    version = Constans.TOOL_VERSION
    adminserver_name = Constans.ADMINSERVER_NAME
    maxResults = Constans.MAX_RESULTS
    forceOperation = Constans.FORCE_OPERATION
        
class DomainProperties(object):
    '''
    Class storing properties that concern admin server / admin account
    '''
    adminserver_url = None
    username = None
    passwd = None
    user_pwd = None
    usession = None
    passwd_script = None
    netrc = None
    cookie_path = None
    #auth_operation = None
    clusters = None
    
class CERNSpecificProperties(object):
    '''
    Class storing properties that concern domain
    '''
    syscontrol_top = None
    syscontrol_top_script = Constans.syscontrol_top_script
    syscontrol_top_arguments = Constans.syscontrol_top_arguments
    get_passwd_path = Constans.get_passwd_path
    get_passwd_arguments = Constans.get_passwd_arguments
    wlstab_path = Constans.wlstab_path
    wlstab_arguments = Constans.wlstab_arguments
    webtab_path = Constans.webtab_path
    webtab_arguments = Constans.webtab_arguments
    domain_name = None
    domain_dir = None
    wls_dir = None
    curl_certs = Constans.CURL_CERTS
    CERN_username = Constans.CERN_USERNAME