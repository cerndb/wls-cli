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

class Deployments(object):
    
    base_uri = "/management/wls/latest/deployments/"
    
    context_mapping = {Operation.Deployment.DEPLOY_LOCAL_APP: ("application/", ""),
                       Operation.Deployment.DEPLOY_LOCAL_LIB: ("library/", ""),
                       Operation.Deployment.DEPLOY_UPLOADED_APP: ("application/", ""), 
                       Operation.Deployment.DEPLOY_UPLOADED_LIB: ("library/", ""),
                       Operation.Deployment.UNDEPLOY_APP: ("application/id/", ""),
                       Operation.Deployment.UNDEPLOY_LIB: ("library/id/", ""),
                       Operation.Deployment.REDEPLOY_LOCAL_APP: ("application/id/", ""),
                       Operation.Deployment.REDEPLOY_LOCAL_LIB: ("application/id/", ""),
                       Operation.Deployment.REDEPLOY_UPLOADED_APP: ("application/id/", ""),
                       Operation.Deployment.REDEPLOY_UPLOADED_LIB: ("library/id/", ""),
                       Operation.App.UPDATE: ("application/id/", "update"),
                       Operation.App.START: ("application/id/", "start"),
                       Operation.App.STOP: ("application/id/", "stop"),
                       Operation.App.STATUS: ("application/id/", ""),
                       Operation.Show.APPS: ("application/", ""),
                       Operation.Show.LIBRARIES: ("library/", "") }
    
    def get_uri(self, operation, target = None):
        prefix, suffix = Deployments.context_mapping[operation]
        try:
            return Deployments.base_uri + prefix + target + "/" + suffix
        except TypeError:
            return Deployments.base_uri + prefix + suffix