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
Created on May 29, 2015

@author: Konrad Kaczkowski
'''
import argparse
#from common import LoggerWrapper
#import logging

class ParsingRulesSetter(object):
    '''
    Class responsible for setting proper parsing rules.
    '''

    def __init__(self):
        ''' Constructor '''
        self.parser = argparse.ArgumentParser(prog='WebLogic '+\
        'Server 12.1.3 CLI REST wrapper')
        
    def set_parser_rules(self, request, data_wrapper):
        ''' setting all parser rules and defining parameters '''
        functional_ex_group = self.parser.add_mutually_exclusive_group()
        entity_ex_group = self.parser.add_mutually_exclusive_group() 
        credentials_ex_group = self.parser.add_mutually_exclusive_group() 
        self.set_functional_group_rules(functional_ex_group, data_wrapper.version)
        self.set_entity_group_rules(entity_ex_group)
        self.set_credentials_group_rules(credentials_ex_group)
        self.set_additional_rules(self.parser)
        args = self.parser.parse_args(request)
        
        return args
        
    def set_functional_group_rules(self, ex_group, version):
        ''' defining parameters that cannot occur in one request together '''
        ex_group.add_argument('--status', dest='target_type', \
                              help='Print target status: domain / cluster / server / app', type = str)
        ex_group.add_argument('--start', dest='target_type', \
                              help='Start a target: domain / cluster / server / app', type = str)
        ex_group.add_argument('--stop', dest='target_type', \
                              help='Stop a target: domain / cluster / server / app', type = str)
        ex_group.add_argument('--restart', dest='target_type', \
                              help='Restart a target: server', type = str)
        ex_group.add_argument('--suspend', dest='target_type', \
                              help='Suspend a target: server', type = str)
        ex_group.add_argument('--resume', dest='target_type', \
                              help='Resume suspended target: server', type = str)
        ex_group.add_argument('--redeploy', action='store_true', dest="redeploy", \
                            help='Redeploy a target: app.')
        ex_group.add_argument('--update', action='store_true', dest="update", \
                            help='Update a target: app.')
        ex_group.add_argument('--admin_change', dest="target_type", \
                            help='Set administration edit: start / cancel / activate')
        ex_group.add_argument('--show', dest='target_type', \
                              help='Show: apps/libs/targets (WebLogic servers and clusters)', type = str)    
        ex_group.add_argument('--deploy', action='store_true', \
                            dest="deploy", help='Deploy an application: local / uploaded to a target: server / clusters')
        ex_group.add_argument('--undeploy', action='store_true', \
                            dest="undeploy", help='Undeploy a target: app.')
        ex_group.add_argument('--logs', dest="target_type", \
                            help='Show data logs of a target: server / domain. ' +\
                            'Default: 100 last entries. Possibilities: httpaccess / datasource' +\
                            '/server/domain')
        ex_group.add_argument('--version', action='version', \
                            version='%(prog)s ' + str(version))
        
    def set_entity_group_rules(self, ex_group):
        ''' defining parameters that cannot occur in one request together 
        1. -i ENTITY NAME
        2. --url ADMIN_URL
        '''
        ex_group.add_argument('-i', '--entity', action='store', dest='entity', \
                           help='CERN specific implementation', type = str)  
        ex_group.add_argument('--url', action='store', dest='admin_url', \
                           help='Admin URL', type = str)  
        
    def set_credentials_group_rules(self, ex_group):
        ''' defining parameters that cannot occur in one request together 
        1. cookie                   : --usession
        2. interactive              : default
        3. script                   : --passwd_script SCRIPT_TO_EXECUTE
        4. config file              : --netrc
        5. credentials in parameters: --passwd PASSWD --user USERNAME
        '''
        ex_group.add_argument('--netrc', action='store_true', dest="netrc", \
                            help='Use .netrc file to set scredentials')
        ex_group.add_argument('--passwd_script', action='store', dest='passwd_script', \
                           help='Use specified script to set password', type = str)  
        ex_group.add_argument('--usession', action='store_true', dest="usession", \
                            help='Use user session to store an HTTP cookie.')
        ex_group.add_argument('--passwd', dest='passwd',  \
                            help='Specify a password explicitly', type = str)
       
    def set_additional_rules(self, parser):
        ''' defining additional parameters '''
        parser.add_argument('--target', dest='target', \
                            help='Specify a target', type = str)
        parser.add_argument('--targets', dest='target', nargs='+', \
                            help='Specify targets for deployment', type = str)
        parser.add_argument('--adminfs', dest='adminfs', action='store_true', \
                            help='Specify that a file for deployment operation is in admin file system')
        parser.add_argument('--appname', dest='app_name',  \
                            help='Specify an application name', type = str)
        parser.add_argument('--libname', dest='lib_name',  \
                            help='Specify a library name', type = str)
        parser.add_argument('--file', dest='source',  \
                            help='Specify a path for application to be deployed', type = str)
        parser.add_argument('--user', dest='username',  \
                            help='Specify a username explicitly', type = str)
        parser.add_argument('--lib', action='store_true', \
                            dest="lib", help='Library deployment. Compulsary with --deploy option.')
        parser.add_argument('-l', '--long', action='store_true', \
                      dest="long", help='Print full status output')
        parser.add_argument('--async', action='store_true', \
                            dest="async", help='Execute asynchronously')
        parser.add_argument('-v', '--verbose', action='store_true', dest="verbose", \
                            help='Tool verbose communicates')
        parser.add_argument('-v2', '--verbose2', action='store_true', dest="verbose2", \
                            help='Tool and Curl verbose communicates')
        #parser.add_argument('--debug', action='store_true', \
        #                    dest="debug", help='For development purposes.')
        parser.add_argument('--nm', action='store_true', dest="nm", \
                            help='Use NM request. Use only from admin server machine.')
        parser.add_argument('--raw', action='store_true', dest="raw", \
                            help='Do not parse output, print raw')
        parser.add_argument('--servlets', action='store_true', dest="servlets", \
                            help='Show servlets in deployments')
        parser.add_argument('--noforce', action='store_true', dest="noforce", \
                            help='Do not force requested operation. Default: force')
        parser.add_argument('--test', action='store_true', dest="test", \
                            help='Testing purposes')
        parser.add_argument('--maxResults', dest='maxResults',  \
                            help='Specify amount of log entries. Use with: --logs {httpaccess / ' +\
                            'datasource / server / domain}', type = int)
        parser.add_argument('--operationTimeout', dest='curlTimeout',  \
                            help='Specify Curl operation timeout [in sec]. Default: 10 min', type = int)
        
    
    