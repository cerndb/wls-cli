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
from common.utils import TargetType
from common.utils import AuthOperation
from common import LoggerWrapper

class ArgumentInterpretator(object):
    '''
    Class responsible for interpretation of parsed request. 
    It is setting proper values to the data wrapper
    '''
    def __init__(self):
        ''' Constructor '''
        self.logger = LoggerWrapper()
        
    def interpretate_args(self, data_wrapper, args, request):
        ''' interpreting args- setting proper data wrapper properties '''
        self.define_target_type(data_wrapper, args)
        self.define_request_operation(data_wrapper, request, args)
        self.define_auth_operation(data_wrapper, args)
        self.define_operation_type(data_wrapper, args)
        self.define_additional_parameters(data_wrapper, args)
        self.define_domain_name(data_wrapper)
        return self.is_test(data_wrapper, args)
    
    def is_test(self, data_wrapper, args):
        if args.test: 
            data_wrapper.test = args.test
            return True
        return False
    
    def define_domain_name(self, data_wrapper):
        if data_wrapper.domain_name is None:
            adminserver_url = data_wrapper.adminserver_url
            # cut https://
            domain_name = adminserver_url.partition('//')[2].rstrip()
            # cut '-admin' part
            domain_name = domain_name.partition('-admin')[0].rstrip()
            # replace '-' with '_'
            domain_name = domain_name.replace('-', '_')
            data_wrapper.domain_name = domain_name
    
    def define_additional_parameters(self, data_wrapper, args):
        data_wrapper.async = args.async
        data_wrapper.raw = args.raw
        if args.maxResults:
            data_wrapper.maxResults = args.maxResults
        data_wrapper.long = args.long
        data_wrapper.servlets = args.servlets
        data_wrapper.verbose = args.verbose
        if not (args.verbose or args.verbose2):
            self.logger.set_level(self.logger.get_level_name('INFO'))
        data_wrapper.verbose2 = args.verbose2
        data_wrapper.forceOperation = not args.noforce
        data_wrapper.usession = args.usession
        data_wrapper.username = args.username
        data_wrapper.netrc = args.netrc
        data_wrapper.adminserver_url = args.admin_url
        data_wrapper.view_operation = data_wrapper.operation
        if args.curlTimeout: data_wrapper.timeout = args.curlTimeout
    
    def define_auth_operation(self, data_wrapper, args):
        if args.netrc: 
            data_wrapper.auth_operation = AuthOperation.NETRC
            return
        elif args.passwd_script: 
            data_wrapper.auth_operation = AuthOperation.SCRIPT
            data_wrapper.passwd_script = args.passwd_script
            return
        elif args.usession: 
            data_wrapper.auth_operation = AuthOperation.COOKIE
            return
        elif args.entity:
            data_wrapper.domain_name = args.entity
            data_wrapper.auth_operation = AuthOperation.CERN_DATA
            return
        elif args.passwd:
            data_wrapper.passwd = args.passwd
            data_wrapper.auth_operation = AuthOperation.CREDS_IN_PARAMETERS
            return
        data_wrapper.auth_operation = AuthOperation.INTERACTIVE
            
    def define_operation_type(self, data_wrapper, args):
        if(args.nm): data_wrapper.operation_type = 'NM'
        else: data_wrapper.operation_type = 'REST'
        data_wrapper.view_operation_type = data_wrapper.operation_type
        
    def define_target_type(self, data_wrapper, args):
        if args.target_type == "server":
            data_wrapper.target_type = TargetType.SERVER
        elif args.target_type == "cluster":
            data_wrapper.target_type = TargetType.CLUSTER
        elif args.target_type == "domain":
            data_wrapper.target_type = TargetType.DOMAIN
        elif args.target_type == "app":
            data_wrapper.target_type = TargetType.APP
        elif args.target_type == "lib":
            data_wrapper.target_type = TargetType.LIB
        else:
            data_wrapper.target_type = TargetType.NO_TARGET
    
    def define_request_operation(self, data_wrapper, request, args):
        ''' setting request operation - enum and operation type - REST / NM '''
        if args.target and len(args.target) < 2 and not '--deploy' in request: 
            args.target = args.target[0]
        data_wrapper.target = args.target
        if '--status' in request: self.define_status_operation(data_wrapper, args)
        elif '--suspend' in request: data_wrapper.operation = Operation.SUSPEND_SERVERS     
        elif '--resume' in request: data_wrapper.operation = Operation.RESUME_SERVERS   
        elif '--start' in request: self.define_start_operation(data_wrapper, args)
        elif '--stop' in request: self.define_stop_operation(data_wrapper, args)
        elif '--restart' in request: data_wrapper.operation = Operation.RESTART_SERVERS
        elif '--update' in request: self.define_update_app(data_wrapper, args)
        elif '--redeploy' in request: self.define_redeploy_operation(data_wrapper, args)
        elif '--show' in request: self.define_list_operation(data_wrapper, args)
        elif '--logs' in request: self.define_logs_operation(data_wrapper, args)
        elif '--admin_change' in request: self.define_admin_operation(data_wrapper, args)
        elif '--deploy' in request: self.define_deploy_operation(data_wrapper, args)
        elif '--undeploy' in request: self.define_undeploy_operation(data_wrapper, args)
        else:
            raise Exception("Not recognized operation.")
        
    def define_update_app(self, data_wrapper, args):  
        data_wrapper.target_type = TargetType.APP  
        data_wrapper.deployment_name = args.app_name 
        data_wrapper.operation = Operation.UPDATE_APP
        
    def define_redeploy_operation(self, data_wrapper, args):
        ''' setting proper deploy operation - LOCAL or UPLOADED '''
        data_wrapper.target_type = TargetType.APP
        data_wrapper.deployment_name = \
            args.app_name if args.app_name is not None else args.lib_name
        data_wrapper.source = args.source
        if args.adminfs:
            self.define_uploaded_redeploy_operation(args, data_wrapper)
            return
        self.define_local_redeploy_operation(args, data_wrapper)
        
    def define_undeploy_operation(self, data_wrapper, args):
        ''' setting proper undeploy operation - LIB or APP '''
        data_wrapper.target_type = TargetType.APP
        data_wrapper.deployment_name = \
            args.app_name if args.app_name is not None else args.lib_name
        if args.lib_name:
            data_wrapper.operation = Operation.UNDEPLOY_LIB
            return
        data_wrapper.operation = Operation.UNDEPLOY_APP
        
    def define_deploy_operation(self, data_wrapper, args):
        ''' setting proper deploy operation - LOCAL or UPLOADED '''
        data_wrapper.target_type = TargetType.APP
        data_wrapper.deployment_name = \
            args.app_name if args.app_name is not None else args.lib_name
        data_wrapper.source = args.source
        if args.adminfs:
            self.define_uploaded_deploy_operation(args, data_wrapper)
            return
        self.define_local_deploy_operation(args, data_wrapper)
    
    def define_local_deploy_operation(self, args, data_wrapper):
        ''' setting proper local deploy operation - APP or LIB '''
        if args.lib_name:
            data_wrapper.operation = Operation.DEPLOY_LOCAL_LIB
        else:
            data_wrapper.operation = Operation.DEPLOY_LOCAL_APP
    
    def define_uploaded_deploy_operation(self, args, data_wrapper):
        ''' setting proper uploaded deploy operation - APP or LIB '''
        if args.lib_name:
            data_wrapper.operation = Operation.DEPLOY_UPLOADED_LIB
        else:
            data_wrapper.operation = Operation.DEPLOY_UPLOADED_APP
            
    def define_local_redeploy_operation(self, args, data_wrapper):
        ''' setting proper local deploy operation - APP or LIB '''
        if args.lib_name:
            data_wrapper.operation = Operation.REDEPLOY_LOCAL_LIB
        else:
            data_wrapper.operation = Operation.REDEPLOY_LOCAL_APP
    
    def define_uploaded_redeploy_operation(self, args, data_wrapper):
        ''' setting proper uploaded deploy operation - APP or LIB '''
        if args.lib_name:
            data_wrapper.operation = Operation.REDEPLOY_UPLOADED_LIB
        else:
            data_wrapper.operation = Operation.REDEPLOY_UPLOADED_APP
        
        
    def define_admin_operation(self, data_wrapper, args):
        ''' setting proper admin operation - START or CANCEL or ACTIVATE '''
        if args.target_type == 'start':
            data_wrapper.operation = Operation.START_ADMIN_CHANGES
            return
        elif args.target_type == 'cancel':
            data_wrapper.operation = Operation.CANCEL_ADMIN_CHANGES
            return
        elif args.target_type == 'activate':
            data_wrapper.operation = Operation.ACTIVATE_ADMIN_CHANGES
            return
        raise Exception("Not recognized admin change type.")
        
    def define_logs_operation(self, data_wrapper, args):
        ''' setting proper logs operation - HTTPACCESS 
        or DATASOURCE or DOMAIN or SERVER '''
        data_wrapper.target_type = TargetType.SERVER
        if args.target_type == 'httpaccess':
            data_wrapper.operation = Operation.SHOW_HTTP_ACCESS_LOGS
            return
        elif args.target_type == 'datasource':
            data_wrapper.operation = Operation.SHOW_DATASOURCE_LOGS
            return
        elif args.target_type == 'server':
            data_wrapper.operation = Operation.SHOW_SERVER_LOGS
            return
        elif args.target_type == 'domain':
            data_wrapper.target = data_wrapper.adminserver_name
            data_wrapper.operation = Operation.SHOW_DOMAIN_LOGS
            return
        raise Exception("Not recognized logs type.")
        
    def define_list_operation(self, data_wrapper, args):
        ''' setting proper show operation - APPS or LIBRARIES or TARGETS '''
        if args.target_type == 'apps':
            data_wrapper.operation = Operation.LIST_APPS
            return
        elif args.target_type == 'libs':
            data_wrapper.operation = Operation.LIST_LIBRARIES
            return
        elif args.target_type == 'targets':
            data_wrapper.operation = Operation.LIST_TARGETS
            return
        elif args.target_type == 'jobs':
            data_wrapper.operation = Operation.SHOW_JOBS
            return
        raise Exception("Not recognized target type.")
        
    def define_start_operation(self, data_wrapper, args):
        ''' setting proper start operation - SERVERS or APPS '''
        if args.target_type == 'app':
            data_wrapper.operation = Operation.START_APP
            data_wrapper.deployment_name = \
            args.app_name if args.app_name is not None else args.lib_name
            return
        data_wrapper.operation = Operation.START_SERVERS
            
    def define_stop_operation(self, data_wrapper, args):
        ''' setting proper stop operation - SERVERS or APPS '''
        if args.target_type == 'app':
            data_wrapper.operation = Operation.STOP_APP
            data_wrapper.deployment_name = \
            args.app_name if args.app_name is not None else args.lib_name
            return
        data_wrapper.operation = Operation.STOP_SERVERS
            
    def define_status_operation(self, data_wrapper, args):
        ''' setting proper status operation - SERVERS or APPS '''
        if args.target_type == 'app':
            data_wrapper.operation = Operation.STATUS_APP
            data_wrapper.deployment_name = \
            args.app_name if args.app_name is not None else args.lib_name
            return
        data_wrapper.operation = Operation.STATUS_SERVERS