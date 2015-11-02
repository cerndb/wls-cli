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
Created on May 28, 2015
@author: Konrad Kaczkowski
'''
from controller import Controller
from view import View
from model import Model
from Queue import Queue
import sys
import os
import errno

def main():
    '''
        Main method
    '''
    
    check_if_user_is_root()
    
    queue = Queue()
    view = View()
    model = Model()
    controller = Controller(model, view, queue)
    # put parameters (all except for first) to a queue - controller will receive it
    queue.put(sys.argv[1:])
    controller.run()
    
def check_if_user_is_root():
    if os.geteuid() == 0:
        print >> sys.stderr, "ERROR: Please do not run as root, Scherlock"
        sys.exit(1)

if __name__ == '__main__':
    main()