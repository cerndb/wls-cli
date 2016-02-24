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
'''
import inspect, os

class Constans(object):
    '''
    '''
    ADMINSERVER_NAME = "AdminServer"
    TOOL_VERSION = "v4.1"
    TIMEOUT = 2
    CONNECT_TIMEOUT = 600
    MAX_RESULTS = 100
    FORCE_OPERATION = True
    
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
    #curl_certs = "/ORA/dbs01/syscontrol/etc/certs/ca/CERNDB-bundle.crt"
    
    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    CURL_CERTS = os.path.join(os.path.split(current_dir)[0], \
                              '../../cert/certificate.crt')
    CERN_USERNAME = "weblogic"