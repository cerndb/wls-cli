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
from abc import ABCMeta, abstractmethod
from rest_agent_creation import RESTAgentCreator
from common.utils import Operation
from common.utils import TargetType

class Strategy(object):
    '''
    Parent classes for strategy design pattern.
    '''
    __metaclass__ = ABCMeta
        
    @abstractmethod
    def execute(self, data_wrapper):
        ''' execute method '''
        raise NotImplementedError('subclasses must override execute()!')
    
    def create_target_list(self, data_wrapper):
        ''' create target_list regarding target type '''
        target_list = list()
        if (data_wrapper.target_type == TargetType.DOMAIN):
            self.append_domain(data_wrapper, target_list)
        elif(data_wrapper.target_type == TargetType.CLUSTER):
            try:
                self.append_cluster(data_wrapper.clusters[data_wrapper.target], target_list)         
            except KeyError:
                raise Exception("Not recognized target: " + str(data_wrapper.target))      
        elif(data_wrapper.target_type == TargetType.SERVER or \
             data_wrapper.target_type == TargetType.APP):
            self.append_server(data_wrapper.target, target_list)
        else:
            raise Exception("Unrecognized target type: " + str(data_wrapper.target_type))
        return target_list
    
    def append_cluster(self, cluster, target_list):
        ''' adding all servers in cluster to the target_list '''
        for target in cluster:
            self.append_server(target, target_list)
    
    def append_domain(self, data_wrapper, target_list):
        ''' adding all servers in domain to the target_list '''
        adminserver_name = data_wrapper.adminserver_name
        try:
            if_stop = (data_wrapper.operation == Operation.STOP_SERVERS)
        except AttributeError: pass
        if (if_stop):
            for cluster in data_wrapper.clusters.itervalues():
                self.append_cluster(cluster, target_list)
            self.append_server(adminserver_name, target_list)       
        else:
            self.append_server(adminserver_name, target_list)     
            for cluster in data_wrapper.clusters.itervalues():
                self.append_cluster(cluster, target_list)
    
    def append_server(self, target, target_list):
        ''' adding selected server to the target_list '''
        target_list.append(target)   
    
class RESTGeneralStrategy(Strategy):
    '''
    Class representing strategy for operations without target
    '''

    def __init__(self):
        ''' Constructor '''
        super(RESTGeneralStrategy, self).__init__()
        
    def execute(self, data_wrapper, operation):
        ''' execute strategy - create and add agent object to the agents list'''
        agents_list = list()
        operation_type = data_wrapper.operation_type
        
        if operation_type == "NM":
            raise Exception("Cannot perform this operation with NM.")
        
        elif operation_type == "REST":
            agent_creator = RESTAgentCreator()
            agents_list.append(agent_creator.create_agent(data_wrapper, operation, ""))
        
        else:
            raise Exception("Unknown operation type.")
        
        return agents_list
    
    
class RESTTargetStrategy(Strategy):
    '''
    Class representing strategy for operations with target
    '''

    def __init__(self):
        ''' Constructor '''
        super(RESTTargetStrategy, self).__init__()
        
    def execute(self, data_wrapper, operation):
        ''' execute strategy - set proper agents list from target list'''
        operation_type = data_wrapper.operation_type
        
        if data_wrapper.deployment_name is not None:
            target_list = [ data_wrapper.deployment_name ]
        else:
            target_list = super(RESTTargetStrategy, self).create_target_list(data_wrapper)
        agents_list = list()
        
        if operation_type == "NM":
            raise Exception("Cannot perform this operation with NM.")
        
        elif operation_type == "REST":
            agent_creator = RESTAgentCreator()
            #agents_list.append(agent_creator.create_agent(data_wrapper, operation, target))
            for target in target_list:
                agents_list.append(agent_creator.create_agent(data_wrapper, operation, target))
            
        else:
            raise Exception("Unknown operation type.")
        return agents_list
