
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
Created on June 18, 2015

@author: Konrad Kaczkowski
'''
from common.utils import Operation

class StrategyDictionary(object):
    '''
    Dictionary that contains data (command name, url context and other variables)
    that is necessary to create curl request. Data is stored in proper kind
    of dictionary
    '''
    _instance = None
    def __new__(cls, *args, **kwargs):
        ''' Singleton '''
        if not cls._instance:
            cls._instance = super(StrategyDictionary, cls).__new__(cls)
        return cls._instance

    def __init__(self, command):
        ''' Constructor '''
        self._strategy_tuple = dict()
        self.dictionary_mapping = {Operation.START_SERVERS: (ServersDictionary, 'start', self._strategy_tuple),
           Operation.SUSPEND_SERVERS: (ServersDictionary, 'suspend', self._strategy_tuple),
           Operation.RESUME_SERVERS: (ServersDictionary, 'resume', self._strategy_tuple),
           Operation.STOP_SERVERS: (ServersDictionary, 'stop', self._strategy_tuple),
           Operation.STATUS_SERVERS: (ServersDictionary, 'status', self._strategy_tuple),
           Operation.RESTART_SERVERS: (ServersDictionary, 'restart', self._strategy_tuple),        
           Operation.START_ADMIN_CHANGES: (ChangeManagerDictionary, 'start_edit', self._strategy_tuple),
           Operation.CANCEL_ADMIN_CHANGES: (ChangeManagerDictionary, 'cancel_edit', self._strategy_tuple),
           Operation.ACTIVATE_ADMIN_CHANGES: (ChangeManagerDictionary, 'activate', self._strategy_tuple),       
           Operation.LIST_TARGETS: (ListsDictionary, 'targets', self._strategy_tuple),     
           Operation.DEPLOY_LOCAL_APP: (DeploymentsDictionary, 'deploy_local_app', self._strategy_tuple),
           Operation.DEPLOY_UPLOADED_APP: (DeploymentsDictionary, 'deploy_uploaded_app', self._strategy_tuple),
           Operation.UNDEPLOY_APP: (DeploymentsDictionary, 'undeploy_app', self._strategy_tuple),
           Operation.DEPLOY_LOCAL_LIB: (DeploymentsDictionary, 'deploy_local_lib', self._strategy_tuple),
           Operation.DEPLOY_UPLOADED_LIB: (DeploymentsDictionary, 'deploy_uploaded_lib', self._strategy_tuple),
           Operation.UNDEPLOY_LIB: (DeploymentsDictionary, 'undeploy_lib', self._strategy_tuple),
           Operation.LIST_LIBRARIES: (ListsDictionary, 'library', self._strategy_tuple),
           Operation.SHOW_JOBS: (ListsDictionary, 'jobs', self._strategy_tuple),
           Operation.START_APP: (AppsDictionary, 'start_app', self._strategy_tuple),
           Operation.STOP_APP: (AppsDictionary, 'stop_app', self._strategy_tuple),
           Operation.REDEPLOY_LOCAL_APP: (DeploymentsDictionary, 'redeploy_app', self._strategy_tuple),
           Operation.REDEPLOY_UPLOADED_APP: (DeploymentsDictionary, 'redeploy_app', self._strategy_tuple),
           Operation.REDEPLOY_LOCAL_LIB: (DeploymentsDictionary, 'redeploy_lib', self._strategy_tuple),
           Operation.REDEPLOY_UPLOADED_LIB: (DeploymentsDictionary, 'redeploy_lib', self._strategy_tuple),
           Operation.UPDATE_APP: (AppsDictionary, 'update_app', self._strategy_tuple),
           Operation.STATUS_APP: (AppsDictionary, 'status_app', self._strategy_tuple),
           Operation.LIST_APPS: (ListsDictionary, 'apps', self._strategy_tuple),  
           Operation.GET_DOMAIN_DATA: (TenantMonitoringDictionary, 'clusters', self._strategy_tuple),      
           Operation.SHOW_HTTP_ACCESS_LOGS: (LogsDictionary, 'httpaccesslog', self._strategy_tuple),
           Operation.SHOW_DATASOURCE_LOGS: (LogsDictionary, 'datasourcelog', self._strategy_tuple),
           Operation.SHOW_SERVER_LOGS: (LogsDictionary, 'serverlog', self._strategy_tuple),
           Operation.SHOW_DOMAIN_LOGS: (LogsDictionary, 'domainlog', self._strategy_tuple)}
        
        self.fill_tuple(command)
        
    def fill_tuple(self, tuple_type):
        ''' Constructor '''
        cls, method, param = self.dictionary_mapping[tuple_type]
        dictionary = cls()
        getattr(dictionary, method)(param)
        
    def get_tuple(self):
        return self._strategy_tuple

class ServersDictionary(object):
    '''
    Dictionary containing data necessary for operations on servers/clusters/domain
    '''
    _instance = None
    def __new__(cls, *args, **kwargs):
        ''' Singleton '''
        if not cls._instance:
            cls._instance = super(ServersDictionary, cls).__new__(cls)
        return cls._instance

    def start(self, strategy_tuple):
        strategy_tuple.update({"NM":"START"})
        strategy_tuple.update({"REST":"start"})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/servers/id/"})  
    def stop(self, strategy_tuple):
        strategy_tuple.update({"NM":"KILL"})
        strategy_tuple.update({"REST":"shutdown"})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/servers/id/"}) 
    def status(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":""})
        strategy_tuple.update({"HTTP":"GET"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/servers/id/"})  
    def restart(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"restart"})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/servers/id/"})      
    def suspend(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"suspend"})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/servers/id/"})      
    def resume(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"resume"})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/servers/id/"})       
        
class TenantMonitoringDictionary(object):
    '''
    Dictionary containing data necessary for monitoring operations
    '''
    _instance = None
    def __new__(cls, *args, **kwargs):
        ''' Singleton '''
        if not cls._instance:
            cls._instance = super(TenantMonitoringDictionary, cls).__new__(cls)
        return cls._instance

    def clusters(self, strategy_tuple):
        strategy_tuple.update({"NM":""})
        strategy_tuple.update({"REST":""})
        strategy_tuple.update({"HTTP":"GET"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/tenant-monitoring/clusters"})  
        
        
class ChangeManagerDictionary(object):
    '''
    Dictionary containing data necessary for administration operations
    '''
    _instance = None
    def __new__(cls, *args, **kwargs):
        ''' Singleton '''
        if not cls._instance:
            cls._instance = super(ChangeManagerDictionary, cls).__new__(cls)
        return cls._instance
    
    def start_edit(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"startEdit"})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/changeManager/"})        
    def cancel_edit(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"cancelEdit"})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/changeManager/"})      
    def activate(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"activate"})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/changeManager/"})
        
class ListsDictionary(object):
    '''
    Dictionary containing data necessary for listing operations (show)
    '''
    _instance = None
    def __new__(cls, *args, **kwargs):
        ''' Singleton '''
        if not cls._instance:
            cls._instance = super(ListsDictionary, cls).__new__(cls)
        return cls._instance
    
    def targets(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"targets"})
        strategy_tuple.update({"HTTP":"GET"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/"})
    def apps(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"application"})
        strategy_tuple.update({"HTTP":"GET"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/deployments/"}) 
    def library(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"library"})
        strategy_tuple.update({"HTTP":"GET"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/deployments/"})  
    def jobs(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"jobs"})
        strategy_tuple.update({"HTTP":"GET"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/"})  
        
class LogsDictionary(object):
    '''
    Dictionary containing data necessary for operations on logs
    '''
    _instance = None
    def __new__(cls, *args, **kwargs):
        ''' Singleton '''
        if not cls._instance:
            cls._instance = super(LogsDictionary, cls).__new__(cls)
        return cls._instance
    
    def httpaccesslog(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"logs/id/HTTPAccessLog"})
        strategy_tuple.update({"HTTP":"GET"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/servers/id/"})      
    def datasourcelog(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"logs/id/DataSourceLog"})
        strategy_tuple.update({"HTTP":"GET"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/servers/id/"})    
    def serverlog(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"logs/id/ServerLog"})
        strategy_tuple.update({"HTTP":"GET"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/servers/id/"})     
    def domainlog(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"logs/id/DomainLog"})
        strategy_tuple.update({"HTTP":"GET"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/servers/id/"})
        
        
class AppsDictionary(object):
    '''
    Dictionary containing data necessary for operations on apps
    '''
    _instance = None
    def __new__(cls, *args, **kwargs):
        ''' Singleton '''
        if not cls._instance:
            cls._instance = super(AppsDictionary, cls).__new__(cls)
        return cls._instance
            
    def redeploy_app(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"redeploy"})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":True})
        strategy_tuple.update({"url_context":"/management/wls/latest/deployments/application/id/"})   
    def update_app(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"update"})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/deployments/application/id/"})    
    def start_app(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"start"})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/deployments/application/id/"})     
    def stop_app(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"stop"})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/deployments/application/id/"})    
    def status_app(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":""})
        strategy_tuple.update({"HTTP":"GET"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/deployments/application/id/"})      
        
class DeploymentsDictionary(object):
    '''
    Dictionary containing data necessary for deploy / undeploy operations
    '''
    _instance = None
    def __new__(cls, *args, **kwargs):
        ''' Singleton '''
        if not cls._instance:
            cls._instance = super(DeploymentsDictionary, cls).__new__(cls)
        return cls._instance  
    def redeploy_app(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"redeploy"})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":True})
        strategy_tuple.update({"url_context":"/management/wls/latest/deployments/application/id/"})     
    def redeploy_lib(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":"redeploy"})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":True})
        strategy_tuple.update({"url_context":"/management/wls/latest/deployments/library/id/"})   
    def deploy_local_app(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":""})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":True})
        strategy_tuple.update({"url_context":"/management/wls/latest/deployments/application/"})   
    def deploy_uploaded_app(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":""})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":True})
        strategy_tuple.update({"url_context":"/management/wls/latest/deployments/application/"})    
    def undeploy_app(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":""})
        strategy_tuple.update({"HTTP":"DELETE"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/deployments/application/id/"})     
    def deploy_local_lib(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":""})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":True})
        strategy_tuple.update({"url_context":"/management/wls/latest/deployments/library/"})   
    def deploy_uploaded_lib(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":""})
        strategy_tuple.update({"HTTP":"POST"})
        strategy_tuple.update({"postfields":True})
        strategy_tuple.update({"url_context":"/management/wls/latest/deployments/library/"})      
    def undeploy_lib(self, strategy_tuple):
        strategy_tuple.update({"NM":"EMPTY"})
        strategy_tuple.update({"REST":""})
        strategy_tuple.update({"HTTP":"DELETE"})
        strategy_tuple.update({"postfields":False})
        strategy_tuple.update({"url_context":"/management/wls/latest/deployments/library/id/"})