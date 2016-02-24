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

from wlscli.view import View
from wlscli.common import LoggerWrapper
from wlscli.common.event import ConsoleUIEvent
from wlscli.view.console_ui import result_parse
from wlscli.common.utils import MessageType
from wlscli.common.utils import bcolors

class ConsoleUI(View):
    '''
    View class - facade. Responsible for gathering request and 
    presenting results to the end user.
    '''
    
    def __init__(self, queue, command = None):
        ''' Constructor '''
        self.queue = queue
        ui_event = ConsoleUIEvent(command)
        # put parameters to a queue - controller will receive it
        queue.put(ui_event)
        self.logger_wrapper = LoggerWrapper()
        self.parser = None
        
    def display(self, mockup):
        ''' Gets output from mockup and sends it to output parser. '''
        
        message = mockup.message
        message_type = mockup.message_type
        
        if mockup.test:
            return True
        
        if message_type == MessageType.INFO:
            message = bcolors.OKBLUE + message + bcolors.ENDC
            self.logger_wrapper.logger.info(message)
        elif message_type == MessageType.DEBUG:
            message = bcolors.WARNING + message + bcolors.ENDC
            self.logger_wrapper.logger.debug(message)
        elif message_type == MessageType.ERROR:
            message = bcolors.FAIL + message + bcolors.ENDC
            self.logger_wrapper.logger.error(message)
        elif message_type == MessageType.JSON:
            self.parser = result_parse.RESTParser()
            self.parser.parse(mockup)
        elif message_type == MessageType.STATUS_CODE:
            message = bcolors.BOLD + "Finished. Status code: "+str(message) + bcolors.ENDC
            self.logger_wrapper.logger.info(message)
        else:
            raise Exception("Unrecognized message type")
        return True