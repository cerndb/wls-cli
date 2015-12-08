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
from wlscli.common.utils import Operation
from wlscli.common.utils import TargetType
from wlscli.common.utils import AuthOperation
from wlscli.common.utils import RequestType
from wlscli.common import LoggerWrapper
from wlscli.common import event

class ArgumentInterpretator(object):
    '''
    Class responsible for interpretation of parsed request. 
    It is setting proper values to the data wrapper
    '''
    def __init__(self):
        ''' Constructor '''
        self.logger = LoggerWrapper()
        
    def interpretate_args(self, view_model, args, request):
        ''' interpreting args- setting proper data wrapper properties '''
        self.define_target_type(view_model, args)
        event = self.define_request_operation(view_model, request, args)
        event.auth_operation = self.define_auth_operation(view_model, args)
        self.define_operation_type(view_model, args)
        self.define_additional_parameters(view_model, args)
        self.define_domain_name(view_model)
        self.set_is_test(view_model, args)
        
        return event
        
    def set_is_test(self, view_model, args):
        if args.test: 
            view_model.test = args.test
            return True
        return False
    
    def define_domain_name(self, view_model):
        if view_model.domain_name is None:
            adminserver_url = view_model.adminserver_url
            # cut https://
            domain_name = adminserver_url.partition('//')[2].rstrip()
            # cut '-admin' part
            domain_name = domain_name.partition('-admin')[0].rstrip()
            # replace '-' with '_'
            domain_name = domain_name.replace('-', '_')
            view_model.domain_name = domain_name
    
    def define_additional_parameters(self, view_model, args):
        view_model.async = args.async
        view_model.raw = args.raw
        if args.maxResults:
            view_model.maxResults = args.maxResults
        view_model.long = args.long
        view_model.servlets = args.servlets
        view_model.verbose = args.verbose
        if not (args.verbose or args.verbose2):
            self.logger.set_level(self.logger.get_level_name('INFO'))
        view_model.verbose2 = args.verbose2
        view_model.forceOperation = not args.noforce
        view_model.usession = args.usession
        view_model.username = args.username
        view_model.netrc = args.netrc
        view_model.adminserver_url = args.admin_url
        if args.curlTimeout: view_model.timeout = args.curlTimeout
    
    def define_auth_operation(self, view_model, args):
        if args.netrc: 
            return AuthOperation.NETRC
        elif args.passwd_script: 
            view_model.passwd_script = args.passwd_script
            return AuthOperation.SCRIPT
        elif args.usession: 
            return AuthOperation.COOKIE
        elif args.entity:
            view_model.domain_name = args.entity
            return AuthOperation.CERN_DATA
        elif args.passwd:
            view_model.passwd = args.passwd
            return AuthOperation.CREDS_IN_PARAMETERS
        return AuthOperation.INTERACTIVE
            
    def define_operation_type(self, view_model, args):
        if(args.nm): view_model.operation_type = RequestType.NM
        else: view_model.operation_type = RequestType.REST
        
    def define_target_type(self, view_model, args):
        if args.target_type == "server":
            view_model.target_type = TargetType.SERVER
        elif args.target_type == "cluster":
            view_model.target_type = TargetType.CLUSTER
        elif args.target_type == "domain":
            view_model.target_type = TargetType.DOMAIN
        elif args.target_type == "app":
            view_model.target_type = TargetType.APP
        elif args.target_type == "lib":
            view_model.target_type = TargetType.LIB
        else:
            view_model.target_type = TargetType.NO_TARGET
    
    def define_request_operation(self, view_model, request, args):
        ''' setting request operation - enum and operation type - REST / NM '''
        if args.target and len(args.target) < 2 and not '--deploy' in request: 
            args.target = args.target[0]
        view_model.target = args.target
        if '--status' in request: return self.define_status_operation(view_model, args)
        elif '--suspend' in request: return event.EventFactory(Operation.Server.SUSPEND)   
        elif '--resume' in request: return event.EventFactory(Operation.Server.RESUME)   
        elif '--start' in request: return self.define_start_operation(view_model, args)
        elif '--stop' in request: return self.define_stop_operation(view_model, args)
        elif '--restart' in request: return event.EventFactory(Operation.Server.RESTART)
        elif '--update' in request: return self.define_update_app(view_model, args)
        elif '--redeploy' in request: return self.define_redeploy_operation(view_model, args)
        elif '--show' in request: return self.define_show_operation(view_model, args)
        elif '--logs' in request: return self.define_logs_operation(view_model, args)
        elif '--admin_change' in request: return self.define_admin_operation(view_model, args)
        elif '--deploy' in request: return self.define_deploy_operation(view_model, args)
        elif '--undeploy' in request: return self.define_undeploy_operation(view_model, args)
        else:
            raise Exception("Not recognized operation.")
        
    def define_update_app(self, view_model, args):  
        view_model.target_type = TargetType.APP  
        view_model.deployment_name = args.app_name 
        return event.EventFactory(Operation.App.UPDATE)
        
    def define_redeploy_operation(self, view_model, args):
        ''' setting proper deploy operation - LOCAL or UPLOADED '''
        view_model.target_type = TargetType.APP
        view_model.deployment_name = \
            args.app_name if args.app_name is not None else args.lib_name
        view_model.source = args.source
        if args.adminfs:
            return self.define_uploaded_redeploy_operation(args, view_model)
        return self.define_local_redeploy_operation(args, view_model)
        
    def define_undeploy_operation(self, view_model, args):
        ''' setting proper undeploy operation - LIB or APP '''
        view_model.target_type = TargetType.APP
        view_model.deployment_name = \
            args.app_name if args.app_name is not None else args.lib_name
        if args.lib_name:
            return event.EventFactory(Operation.Deployment.UNDEPLOY_LIB)
        return event.EventFactory(Operation.Deployment.UNDEPLOY_APP)
        
    def define_deploy_operation(self, view_model, args):
        ''' setting proper deploy operation - LOCAL or UPLOADED '''
        view_model.target_type = TargetType.APP
        view_model.deployment_name = \
            args.app_name if args.app_name is not None else args.lib_name
        view_model.source = args.source
        if args.adminfs:
            return self.define_uploaded_deploy_operation(args, view_model)
        return self.define_local_deploy_operation(args, view_model)
    
    def define_local_deploy_operation(self, args, view_model):
        ''' setting proper local deploy operation - APP or LIB '''
        if args.lib_name:
            return event.EventFactory(Operation.Deployment.DEPLOY_LOCAL_LIB)
        return event.EventFactory(Operation.Deployment.DEPLOY_LOCAL_APP)
    
    def define_uploaded_deploy_operation(self, args, view_model):
        ''' setting proper uploaded deploy operation - APP or LIB '''
        if args.lib_name:
            return event.EventFactory(Operation.Deployment.DEPLOY_UPLOADED_LIB)
        return event.EventFactory(Operation.Deployment.DEPLOY_UPLOADED_APP)
            
    def define_local_redeploy_operation(self, args, view_model):
        ''' setting proper local deploy operation - APP or LIB '''
        if args.lib_name:
            return event.EventFactory(Operation.Deployment.REDEPLOY_LOCAL_LIB)
        return event.EventFactory(Operation.Deployment.REDEPLOY_LOCAL_APP)
    
    def define_uploaded_redeploy_operation(self, args, view_model):
        ''' setting proper uploaded deploy operation - APP or LIB '''
        if args.lib_name:
            return event.EventFactory(Operation.Deployment.REDEPLOY_UPLOADED_LIB)
        return event.EventFactory(Operation.Deployment.REDEPLOY_UPLOADED_APP)
        
    def define_admin_operation(self, view_model, args):
        ''' setting proper admin operation - START or CANCEL or ACTIVATE '''
        if 'start' in args.target_type:
            return event.EventFactory(Operation.AdmChange.START_CHANGES)
        elif 'cancel' in  args.target_type:
            return event.EventFactory(Operation.AdmChange.CANCEL_CHANGES)
        elif 'activate' in args.target_type:
            return event.EventFactory(Operation.AdmChange.ACTIVATE_CHANGES)
        raise Exception("Not recognized admin change type.")
        
    def define_logs_operation(self, view_model, args):
        ''' setting proper logs operation - HTTPACCESS 
        or DATASOURCE or DOMAIN or SERVER '''
        view_model.target_type = TargetType.SERVER
        if 'httpaccess' in args.target_type:
            return event.EventFactory(Operation.Logs.HTTP_ACCESS)
        elif 'datasource' in args.target_type:
            return event.EventFactory(Operation.Logs.DATASOURCE)
        elif 'server' in args.target_type:
            return event.EventFactory(Operation.Logs.SERVER)
        elif 'domain' in args.target_type:
            view_model.target = view_model.adminserver_name
            return event.EventFactory(Operation.Logs.DOMAIN)
        
        print "DEBYG: "+str(args.target_type)
        raise Exception("Not recognized logs type.")
        
    def define_show_operation(self, view_model, args):
        ''' setting proper show operation - APPS or LIBRARIES or TARGETS '''
        if 'apps' in args.target_type:
            return event.EventFactory(Operation.Show.APPS)
        elif 'libs' in args.target_type:
            return event.EventFactory(Operation.Show.LIBRARIES)
        elif 'targets' in args.target_type:
            return event.EventFactory(Operation.Show.TARGETS)
        elif 'jobs' in args.target_type:
            return event.EventFactory(Operation.Show.JOBS)
        raise Exception("Not recognized target type.")
        
    def define_start_operation(self, view_model, args):
        ''' setting proper start operation - SERVERS or APPS '''
        if 'app' in args.target_type:
            view_model.deployment_name = \
            args.app_name if args.app_name is not None else args.lib_name
            return event.EventFactory(Operation.App.START)
        return event.EventFactory(Operation.Server.START)
            
    def define_stop_operation(self, view_model, args):
        ''' setting proper stop operation - SERVERS or APPS '''
        if 'app' in args.target_type:
            view_model.deployment_name = \
            args.app_name if args.app_name is not None else args.lib_name
            return event.EventFactory(Operation.App.STOP)
        return event.EventFactory(Operation.Server.STOP)
            
    def define_status_operation(self, view_model, args):
        ''' setting proper status operation - SERVERS or APPS '''
        if 'app' in args.target_type:
            view_model.deployment_name = \
            args.app_name if args.app_name is not None else args.lib_name
            return event.EventFactory(Operation.App.STATUS)
        return event.EventFactory(Operation.Server.STATUS)