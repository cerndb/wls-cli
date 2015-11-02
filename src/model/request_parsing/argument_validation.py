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
from common.utils import Operation

class ArgumentValidator(object):
    '''
    Class responsible for validating arguments in user request.
    '''

    def __init__(self, parser):
        '''Constructor'''
        self.parser = parser
        self.operation_dispatcher = {
                 Operation.START_SERVERS: self.servers_validation, 
                 Operation.STOP_SERVERS: self.servers_validation,
                 Operation.STATUS_SERVERS: self.servers_validation, 
                 Operation.RESTART_SERVERS: self.servers_validation,
                 Operation.SUSPEND_SERVERS: self.servers_validation,
                 Operation.RESUME_SERVERS: self.servers_validation,
                 Operation.LIST_TARGETS: self.list_validation,
                 Operation.START_ADMIN_CHANGES: self.admin_op_validation,
                 Operation.CANCEL_ADMIN_CHANGES: self.admin_op_validation,
                 Operation.ACTIVATE_ADMIN_CHANGES: self.admin_op_validation,
                 Operation.LIST_LIBRARIES: self.list_validation,
                 Operation.LIST_APPS: self.list_validation,
                 Operation.SHOW_JOBS: self.list_validation,
                 Operation.START_APP: self.apps_validation,
                 Operation.STOP_APP: self.apps_validation,
                 Operation.REDEPLOY_LOCAL_APP: self.deployments_validation,
                 Operation.REDEPLOY_UPLOADED_APP: self.deployments_validation,
                 Operation.REDEPLOY_LOCAL_LIB: self.deployments_validation,
                 Operation.REDEPLOY_UPLOADED_LIB: self.deployments_validation,
                 Operation.UPDATE_APP: self.apps_validation,
                 Operation.STATUS_APP: self.apps_validation,
                 Operation.SHOW_DOMAIN_LOGS: self.logs_validation,
                 Operation.SHOW_SERVER_LOGS: self.logs_validation,
                 Operation.SHOW_HTTP_ACCESS_LOGS: self.logs_validation,
                 Operation.SHOW_DATASOURCE_LOGS: self.logs_validation,
                 Operation.DEPLOY_LOCAL_APP: self.deployments_validation,
                 Operation.DEPLOY_UPLOADED_APP: self.deployments_validation,
                 Operation.UNDEPLOY_APP: self.deployments_validation,
                 Operation.DEPLOY_LOCAL_LIB: self.deployments_validation,
                 Operation.DEPLOY_UPLOADED_LIB: self.deployments_validation,
                 Operation.UNDEPLOY_LIB: self.deployments_validation             
                 }
        
    def validate_args(self, data_wrapper, args, request):
        '''Validation arguments. General and specific, according to the type of operation'''
        self.data_wrapper = data_wrapper
        operation = data_wrapper.operation
        self.general_validation(args, request)
        self.operation_dispatcher[operation](args, request)
        
    def general_validation(self, args, request):
        '''Validation that is applied regardless of the type of operation'''
        
        self.credentials_parameters_validation(args, request)
        
        if args.servlets and not('--show' in request and args.target_type == 'apps') and \
        not("--status" in request and 'app' in request):    
            self.parser.error('Cannot set servlets option for this operation.')        
        if args.maxResults and not '--logs' in request:
            self.parser.error('Cannot set maxResults option for this operation.')                 
        if args.lib and not ('--deploy' in request or '--undeploy' in request or \
                             '--redeploy' in request):
            self.parser.error('Cannot set lib option for this operation.')         
        if args.long and not('--status' in request or args.target_type == 'apps' or \
                             '--show' in request):
            self.parser.error('Cannot set long option for this operation.')
        if '--targets' in request and not(args.deploy or args.undeploy or args.redeploy):
            self.parser.error('--targets option can be set only for deploy / undeploy.')
        if args.adminfs and not('--deploy' in request or '--redeploy' in request):
            self.parser.error('--adminfs option can be set only for deploy.')
        if args.source and not ('--deploy' in request or \
                                '--redeploy' in request or '--undeploy' in request):
            self.parser.error('Cannot set --file option for this operation.')   
            
    def credentials_parameters_validation(self, args, request):
        if args.username and not (args.passwd_script or args.passwd):
            self.parser.error('Cannot set --user option for this operation.')
            
        if (args.passwd or args.passwd_script) and not args.username:
            self.parser.error('Missing --user USERNAME argument.')
            
        if args.entity and (args.username or args.passwd or args.usession or args.netrc):
            self.parser.error('Invalid arguments for -i ENTITY_NAME operation')
            
    def servers_validation(self, args, request):
        '''Validation of 'servers' operations'''
        if (not args.target or not args.target_type) and not args.target_type == 'domain':
            self.parser.error('--target option or target_type argument is required.')
        if ('--suspend' in request or '--restart' in request or '--resume' in request) \
        and (args.target_type == "domain") or (args.target_type == "app"):
            self.parser.error('Cannot perform this operation for: ' + args.target_type)  
        if args.target == self.data_wrapper.adminserver_name and '--restart' in request:
            self.parser.error('Cannot perform this operation for: ' + args.target)
        if args.target_type == 'domain' and '--target' in request:
            self.parser.error('Cannot set target for: ' + args.target_type)
        if '--redeploy' in request and args.source:
            print self.parser.prog + ": info: " +\
            "Cannot set file source for this operation. File option ignored."
    
    def apps_validation(self, args, request):
        '''Validation of 'apps' operations'''
        if not args.app_name:
            self.parser.error('--appname option is required.')
        if '--target' in request or '--targets' in request:
            print self.parser.prog + ": info: " +\
            "Cannot set target for this operation. Target option ignored."
    
    def logs_validation(self, args, request):
        '''Validation of 'logs' operations'''
        if ('datasource' in request or 'server' in request or \
            'httpaccess' in request) and not args.target:
            self.parser.error('--target option with argument is required.')
    
    def list_validation(self, args, request):
        '''Validation of 'show' operations'''
        if '--target' in request:
            self.parser.error('Cannot set target for this operation.')
        if args.long and not("jobs" in args.target_type or "apps" in args.target_type or \
                             "libs" in args.target_type):
            print self.parser.prog + ": info: " +\
            "Cannot set long for this operation. Long option ignored."
    
    def deployments_validation(self, args, request):
        '''Validation of 'deployment' operations'''
        if args.lib and not args.lib_name:
            self.parser.error('--libname option is required.')
        elif not args.lib_name and not args.app_name:
            self.parser.error('--appname or --libname option is required.')
            
        if '--deploy' in request and \
         (not args.target or not args.source):
            self.parser.error('--targets, --appname, --file options are required.')
            
        if (args.undeploy or args.redeploy) and \
        ('--targets' in request or '--target' in request):
            print self.parser.prog + ": info: " +\
            "Cannot set target for this operation. Target option ignored."
        if args.undeploy and args.source:
            print self.parser.prog + ": info: " +\
            "Cannot set file source for this operation. File option ignored."
        if '--deploy' in request and '--target' in request:
            self.parser.error("Please use --targets option for this operation.")
        if args.redeploy:
            if args.source and args.adminfs:
                print self.parser.prog + ": info: " +\
                "Cannot set file source for this operation. File option ignored."
            elif not args.adminfs and not args.source:
                self.parser.error("Please specify --file of --adminfs option for this operation.")
    
    def admin_op_validation(self, args, request):
        '''Validation of 'admin_change' operations'''
        if '--target' in request:
            self.parser.error('Cannot set target for this operation.')