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
Created on Nov 4, 2015

@author: Konrad Kaczkowski
'''

class AuthenticationService(object):
    
    def __init__(self, data_storage):
        pass
    
    def get_data(self):
        raise NotImplementedError()
    
    def set_data(self):
        raise NotImplementedError()