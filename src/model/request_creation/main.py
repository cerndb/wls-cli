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
import strategy_objects
from common.utils import Operation

class AgentCreator(object):
    '''
    Class responsible for creating strategy object 
    according to the operation set in request parser
    '''

    def __init__(self):
        ''' Constructor '''
        
        self.operation_dispatcher = {
                 Operation.START_SERVERS: strategy_objects.StartObject, 
                 Operation.STOP_SERVERS: strategy_objects.StopObject,
                 Operation.STATUS_SERVERS: strategy_objects.StatusObject, 
                 Operation.RESTART_SERVERS: strategy_objects.RestartObject,
                 Operation.SUSPEND_SERVERS: strategy_objects.SuspendObject,
                 Operation.RESUME_SERVERS: strategy_objects.ResumeObject,
                 Operation.LIST_TARGETS: strategy_objects.TargetsObject,
                 Operation.START_ADMIN_CHANGES: strategy_objects.StartEditObject,
                 Operation.CANCEL_ADMIN_CHANGES: strategy_objects.CancelEditObject,
                 Operation.ACTIVATE_ADMIN_CHANGES: strategy_objects.ActivateObject,
                 Operation.LIST_LIBRARIES: strategy_objects.ListLibrariesObject,
                 Operation.LIST_APPS: strategy_objects.ListAppsObject,
                 Operation.START_APP: strategy_objects.StartAppObject,
                 Operation.STOP_APP: strategy_objects.StopAppObject,
                 Operation.REDEPLOY_LOCAL_APP: strategy_objects.RedeployAppObject,
                 Operation.REDEPLOY_UPLOADED_APP: strategy_objects.RedeployAppObject,
                 Operation.REDEPLOY_LOCAL_LIB: strategy_objects.RedeployLibObject,
                 Operation.REDEPLOY_UPLOADED_LIB: strategy_objects.RedeployLibObject,
                 Operation.UPDATE_APP: strategy_objects.UpdateAppObject,
                 Operation.STATUS_APP: strategy_objects.StatusAppObject,
                 Operation.SHOW_DOMAIN_LOGS: strategy_objects.DomainLogObject,
                 Operation.SHOW_SERVER_LOGS: strategy_objects.ServerLogObject,
                 Operation.SHOW_HTTP_ACCESS_LOGS: strategy_objects.HttpAccessLogObject,
                 Operation.SHOW_DATASOURCE_LOGS: strategy_objects.DatasourceLogObject,
                 Operation.SHOW_JOBS: strategy_objects.ShowJobsObject,
                 Operation.DEPLOY_LOCAL_APP: strategy_objects.DeployLocalAppObject,
                 Operation.DEPLOY_UPLOADED_APP: strategy_objects.DeployUploadedAppObject,
                 Operation.UNDEPLOY_APP: strategy_objects.UndeployAppObject,
                 Operation.DEPLOY_LOCAL_LIB: strategy_objects.DeployLocalLibObject,
                 Operation.DEPLOY_UPLOADED_LIB: strategy_objects.DeployUploadedLibObject,
                 Operation.UNDEPLOY_LIB: strategy_objects.UndeployLibObject,
                 Operation.GET_DOMAIN_DATA: strategy_objects.GetDomainDataObject
                 }
    
    def execute(self, data_wrapper, operation = None):
        ''' function executes concrete strategy object and 
        returns agent (to be executed) list with operation message '''
        if operation is not None:
            self.operation = operation
            data_wrapper.is_get_domain_data_op = True
        else:
            self.operation = data_wrapper.operation
            data_wrapper.is_get_domain_data_op = False
        strategy = self.operation_dispatcher[self.operation]()
        object_list = strategy.execute(data_wrapper)
        
        return object_list
    
    