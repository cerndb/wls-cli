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

class NMDataContract(object):
    
    def __init__(self):
        self.operation = None
        self.target = None
        self.wls_dir = None
        self.domain_name = None
        self.domain_dir = None