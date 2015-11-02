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
Created on Jun 1, 2015

@author: Konrad Kaczkowski
''' 
from model.data_access import dao

class DataGetter(object):
    '''
    Class used for getting the data from clusters request
    '''
        
    def map_cluster_data_from_REST(self, data_wrapper, json_data):
        ''' Interpreting the data from the request - servers and clusters data. '''
        clusters = dict() 
        
        for cluster_data in json_data["body"]["items"]:
            cluster = list()
            for server in cluster_data["servers"]:
                cluster.append(server["name"])
            clusters[cluster_data["name"]] = cluster
        data_wrapper.clusters = clusters
        
    def get_script_data(self, data_wrapper):
        password_dao = dao.PasswordDAO(data_wrapper)
        password_dao.get_data()
        
        
    def get_CERN_specific_data(self, data_wrapper):
        syscontrol_top_dao = dao.CERNSyscontrolTopDAO(data_wrapper)
        password_dao = dao.CERNPasswordDAO(data_wrapper)
        wlstab_dao = dao.CERNwlstabDAO(data_wrapper)
        webtab_dao = dao.CERNwebtabDAO(data_wrapper)
        
        syscontrol_top_dao.get_data()
        password_dao.get_data()
        wlstab_dao.get_data()
        webtab_dao.get_data()
        
        
               
        
    