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

class ChangeManager(object):
    
    base_uri = "/management/wls/latest/changeManager/"
    context_mapping = {Operation.AdmChange.ACTIVATE_CHANGES: "startEdit",
                Operation.AdmChange.CANCEL_CHANGES: "cancelEdit",
                Operation.AdmChange.START_CHANGES: "activate" }
    
    def get_uri(self, operation):
        return ChangeManager.base_uri + ChangeManager.context_mapping[operation]