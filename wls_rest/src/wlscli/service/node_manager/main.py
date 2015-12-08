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
from wlscli.service.node_manager.nm import NMAgent

class NMManager(object):
    
    def create_agent(self, data_contract):
        self.nm_agent = NMAgent(data_contract)
        
        #if data_wrapper.test:
        #    raise Exception("Unimplemented test case: testing NM.")
    
    def execute_agent(self):
        result, output = self.nm_agent.execute()
        return result, output