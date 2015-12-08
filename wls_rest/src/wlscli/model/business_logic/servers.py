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

from wlscli.common.utils import Operation

class Servers(object):
    
    base_uri = "/management/wls/latest/servers/id/"
    context_mapping = {Operation.Server.START: "start",
                Operation.Server.STOP: "shutdown",
                Operation.Server.SUSPEND: "suspend",
                Operation.Server.STATUS: "",
                Operation.Server.RESTART: "restart",
                Operation.Server.RESUME: "resume" }
    
    def get_uri(self, operation, target):
        return Servers.base_uri + target + "/" + Servers.context_mapping[operation]