#!/usr/bin/env python
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
Created on Oct 25, 2015
@author: Konrad Kaczkowski
'''

class Decorator(object):
    def __new__(cls, decoratee):
        cls = type('decorated',
                   (cls, decoratee.__class__),
                   decoratee.__dict__)
        return object.__new__(cls)