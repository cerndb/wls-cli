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
Created on Oct 31, 2015

@author: Konrad Kaczkowski
'''

from wlscli.common.utils import Operation

class Logs(object):
    
    base_uri = "/management/wls/latest/servers/id/"
    context_mapping = {Operation.Logs.DATASOURCE: "/logs/id/DataSourceLog",
                Operation.Logs.DOMAIN: "/logs/id/DomainLog",
                Operation.Logs.HTTP_ACCESS: "/logs/id/HTTPAccessLog",
                Operation.Logs.SERVER: "/logs/id/ServerLog" }
    
    def get_uri(self, operation, target):
        return Logs.base_uri + target + Logs.context_mapping[operation]