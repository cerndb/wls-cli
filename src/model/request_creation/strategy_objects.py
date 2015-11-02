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
from rest_agent_creation import RESTAgentCreator
from nm_agent_creation import NMAgentCreator
from strategy_base import Strategy
from strategy_base import RESTGeneralStrategy
from strategy_base import RESTTargetStrategy
from common.utils import Operation
    
class StartObject(Strategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to start servers in target_list
    '''

    def __init__(self):
        ''' Constructor '''
        super(StartObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        agents_list = list()
        operation_type = data_wrapper.operation_type
        operation = Operation.START_SERVERS
        target_list = super(StartObject, self).create_target_list(data_wrapper)
        
        if operation_type == "NM":
            agent_creator = NMAgentCreator()
            for server in target_list:
                agents_list.append(agent_creator.create_agent(data_wrapper, operation, server))
        
        elif operation_type == "REST":
            agent_creator = RESTAgentCreator()
            for server in target_list:
                if server == data_wrapper.adminserver_name:
                    #data_wrapper.operation_type = "NM"
                    admin_creator = NMAgentCreator()
                    agents_list.append(admin_creator.create_agent(data_wrapper, operation, server))
                    continue
                agents_list.append(agent_creator.create_agent(data_wrapper, operation, server))
        
        else:
            raise Exception("Unknown operation type.")
        return agents_list
    
class StopObject(Strategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to stop servers in target_list
    '''

    def __init__(self):
        ''' Constructor '''
        super(StopObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        agents_list = list()
        operation_type = data_wrapper.operation_type
        operation = Operation.STOP_SERVERS
        target_list = super(StopObject, self).create_target_list(data_wrapper)
        
        if operation_type == "NM":
            agent_creator = NMAgentCreator()
            for server in target_list:
                agents_list.append(agent_creator.create_agent(data_wrapper, operation, server))
        
        elif operation_type == "REST":
            agent_creator = RESTAgentCreator()
            for server in target_list:
                if server == data_wrapper.adminserver_name:
                    #data_wrapper.operation_type = "NM"
                    admin_creator = NMAgentCreator()
                    agents_list.append(admin_creator.create_agent(data_wrapper, operation, server))
                    continue
                agents_list.append(agent_creator.create_agent(data_wrapper, operation, server))
        
        else:
            raise Exception("Unknown operation type.")
        return agents_list
       
class StatusObject(Strategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to get status from servers in target_list
    '''

    def __init__(self):
        ''' Constructor '''
        super(StatusObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        agents_list = list()
        operation_type = data_wrapper.operation_type
        operation = Operation.STATUS_SERVERS
        target_list = super(StatusObject, self).create_target_list(data_wrapper)
 
        if operation_type == "NM":
            raise Exception("Cannot perform this operation with NM.")
 
        elif operation_type == "REST":
            agent_creator = RESTAgentCreator()
            for server in target_list:
                agents_list.append(agent_creator.create_agent(data_wrapper, operation, server))
 
        else:
            raise Exception("Unknown operation type.")
        return agents_list

class RestartObject(RESTTargetStrategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to restart servers in target_list
    '''

    def __init__(self):
        ''' Constructor '''
        super(RestartObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.RESTART_SERVERS
        return super(RestartObject, self).execute(data_wrapper, operation)
    
class SuspendObject(RESTTargetStrategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to suspend servers in target_list
    '''

    def __init__(self):
        ''' Constructor '''
        super(SuspendObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.SUSPEND_SERVERS
        return super(SuspendObject, self).execute(data_wrapper, operation)
    
class ResumeObject(RESTTargetStrategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to resume servers in target_list
    '''

    def __init__(self):
        ''' Constructor '''
        super(ResumeObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.RESUME_SERVERS
        return super(ResumeObject, self).execute(data_wrapper, operation)

class TargetsObject(RESTGeneralStrategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to make WebLogic show list of targets (servers/clusters)
    '''

    def __init__(self):
        ''' Constructor '''
        super(TargetsObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.LIST_TARGETS
        return super(TargetsObject, self).execute(data_wrapper, operation)
    
class ListLibrariesObject(RESTGeneralStrategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to make WebLogic show list of deployed libraries
    '''

    def __init__(self):
        ''' Constructor '''
        super(ListLibrariesObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.LIST_LIBRARIES
        return super(ListLibrariesObject, self).execute(data_wrapper, operation)
    
class StartEditObject(RESTGeneralStrategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to make WebLogic start administration changes (lock)
    '''

    def __init__(self):
        ''' Constructor '''
        super(StartEditObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.START_ADMIN_CHANGES
        return super(StartEditObject, self).execute(data_wrapper, operation)
    
class CancelEditObject(RESTGeneralStrategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to make WebLogic cancel administration changes (unlock)
    '''

    def __init__(self):
        ''' Constructor '''
        super(CancelEditObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.CANCEL_ADMIN_CHANGES
        return super(CancelEditObject, self).execute(data_wrapper, operation)
    
class ActivateObject(RESTGeneralStrategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to make WebLogic activate administration changes (unlock)
    '''

    def __init__(self):
        ''' Constructor '''
        super(ActivateObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.ACTIVATE_ADMIN_CHANGES
        return super(ActivateObject, self).execute(data_wrapper, operation)
    
class ListAppsObject(RESTGeneralStrategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to make WebLogic show list of deployed applications
    '''

    def __init__(self):
        ''' Constructor '''
        super(ListAppsObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.LIST_APPS
        return super(ListAppsObject, self).execute(data_wrapper, operation)
    
class StartAppObject(RESTTargetStrategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to start an app in target_list
    '''

    def __init__(self):
        ''' Constructor '''
        super(StartAppObject, self).__init__()
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.START_APP
        return super(StartAppObject, self).execute(data_wrapper, operation)
        
        
class StopAppObject(RESTTargetStrategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to stop an app in target_list
    '''

    def __init__(self):
        ''' Constructor '''
        super(StopAppObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.STOP_APP
        return super(StopAppObject, self).execute(data_wrapper, operation)
    
class StatusAppObject(RESTTargetStrategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to get status from an app in target_list
    '''

    def __init__(self):
        ''' Constructor '''
        super(StatusAppObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.STATUS_APP
        return super(StatusAppObject, self).execute(data_wrapper, operation)
    
class UpdateAppObject(RESTTargetStrategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to update an app in target_list
    '''

    def __init__(self):
        ''' Constructor '''
        super(UpdateAppObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.UPDATE_APP
        return super(UpdateAppObject, self).execute(data_wrapper, operation)
   
   
class RedeployAppObject(RESTTargetStrategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to redeploy an app in target_list
    '''

    def __init__(self):
        ''' Constructor '''
        super(RedeployAppObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = data_wrapper.operation
        return super(RedeployAppObject, self).execute(data_wrapper, operation)
    
class RedeployLibObject(RESTTargetStrategy):
    '''
    Strategy object, creates agents to be executed.
    Agents are destined to redeploy a lib in target_list
    '''

    def __init__(self):
        ''' Constructor '''
        super(RedeployLibObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = data_wrapper.operation
        return super(RedeployLibObject, self).execute(data_wrapper, operation)
    
    
class HttpAccessLogObject(RESTTargetStrategy):
    '''
    classdocs
    '''

    def __init__(self):
        ''' Constructor '''
        super(HttpAccessLogObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.SHOW_HTTP_ACCESS_LOGS
        return super(HttpAccessLogObject, self).execute(data_wrapper, operation)
    
class DatasourceLogObject(RESTTargetStrategy):
    '''
    classdocs
    '''

    def __init__(self):
        ''' Constructor '''
        super(DatasourceLogObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.SHOW_DATASOURCE_LOGS
        return super(DatasourceLogObject, self).execute(data_wrapper, operation)
    
class ServerLogObject(RESTTargetStrategy):
    '''
    classdocs
    '''

    def __init__(self):
        ''' Constructor '''
        super(ServerLogObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.SHOW_SERVER_LOGS
        return super(ServerLogObject, self).execute(data_wrapper, operation)
    
    
class DomainLogObject(RESTTargetStrategy):
    '''
    classdocs
    '''

    def __init__(self):
        ''' Constructor '''
        super(DomainLogObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.SHOW_DOMAIN_LOGS
        return super(DomainLogObject, self).execute(data_wrapper, operation)
    
class DeployLocalAppObject(RESTGeneralStrategy):
    '''
    classdocs
    '''

    def __init__(self):
        ''' Constructor '''
        super(DeployLocalAppObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.DEPLOY_LOCAL_APP
        return super(DeployLocalAppObject, self).execute(data_wrapper, operation)
    
class DeployUploadedAppObject(RESTGeneralStrategy):
    '''
    classdocs
    '''

    def __init__(self):
        ''' Constructor '''
        super(DeployUploadedAppObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.DEPLOY_UPLOADED_APP
        return super(DeployUploadedAppObject, self).execute(data_wrapper, operation)
    
class UndeployAppObject(RESTTargetStrategy):
    '''
    classdocs
    '''

    def __init__(self):
        ''' Constructor '''
        super(UndeployAppObject, self).__init__()
        
    def execute(self, data_wrapper):
        operation = Operation.UNDEPLOY_APP
        return super(UndeployAppObject, self).execute(data_wrapper, operation)
    
    
class DeployLocalLibObject(RESTGeneralStrategy):
    '''
    classdocs
    '''

    def __init__(self):
        ''' Constructor '''
        super(DeployLocalLibObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.DEPLOY_LOCAL_LIB
        return super(DeployLocalLibObject, self).execute(data_wrapper, operation)
    
class DeployUploadedLibObject(RESTGeneralStrategy):
    '''
    classdocs
    '''

    def __init__(self):
        ''' Constructor '''
        super(DeployUploadedLibObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.DEPLOY_UPLOADED_LIB
        return super(DeployUploadedLibObject, self).execute(data_wrapper, operation)
    
class UndeployLibObject(RESTTargetStrategy):
    '''
    classdocs
    '''

    def __init__(self):
        ''' Constructor '''
        super(UndeployLibObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.UNDEPLOY_LIB
        return super(UndeployLibObject, self).execute(data_wrapper, operation)
    
class ShowJobsObject(RESTGeneralStrategy):
    '''
    classdocs
    '''

    def __init__(self):
        ''' Constructor '''
        super(ShowJobsObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.SHOW_JOBS
        return super(ShowJobsObject, self).execute(data_wrapper, operation)
    
class GetDomainDataObject(RESTGeneralStrategy):
    '''
    classdocs
    '''

    def __init__(self):
        ''' Constructor '''
        super(GetDomainDataObject, self).__init__()
        
    def execute(self, data_wrapper):
        ''' execute '''
        operation = Operation.GET_DOMAIN_DATA
        return super(GetDomainDataObject, self).execute(data_wrapper, operation)
    
