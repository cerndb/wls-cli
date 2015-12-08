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
import os

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
    timeout = 600
    connect_timeout = 2
    version = Constans.TOOL_VERSION
    adminserver_name = Constans.ADMINSERVER_NAME
    maxResults = 100
    forceOperation = True
        
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
    syscontrol_top_script = "/etc/init.d/syscontrol"
    syscontrol_top_arguments = " sc_configuration_directory"
    get_passwd_path = "/projects/systools/bin/get_passwd"
    get_passwd_arguments = " password_weblogic_"
    wlstab_path = "/bin/wlstab.sh"
    wlstab_arguments = " sc_entity server_name cluster_name " + \
        "server_listen_address server_ssl_listen_port " + \
        "domain_directory"
    webtab_path = "/bin/webtab.sh"
    webtab_arguments = " sc_installation_directory2"
    domain_name = None
    domain_dir = None
    wls_dir = None
    #curl_certs = "/ORA/dbs01/syscontrol/etc/certs/ca/CERNDB-bundle.crt"
    curl_certs = os.path.join(os.path.split(__file__)[0], \
                              '../../../../cert/certificate.crt')
    CERN_username = "weblogic"