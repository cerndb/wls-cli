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
Created on Jul 23, 2015

@author: Konrad Kaczkowski
'''

class EnumMeta(type):
    '''
    Meta class that describes behaviour of its classes
    '''
    def __getattribute__(self, name):
        actual_value = super(EnumMeta, self).__getattribute__(name)
        if isinstance(actual_value, self):
            return actual_value
        else:
            new_value = self(actual_value)
            super(EnumMeta, self).__setattr__(name, new_value)
            return new_value
    
class Enum(object):
    '''
    Class that represents Enumeration with two values:
    - int (id)
    - str (operation description)
    - type (operation type)
    '''
    __metaclass__ = EnumMeta

    def __init__(self, value):
        ''' Constructor '''
        super(Enum, self).__init__()

        self.value = value[0]
        self.repr = value[1]

    def __repr__(self):
        ''' returns string representation '''
        return str(self.repr)