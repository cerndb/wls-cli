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
Created on Jun 30, 2015

@author: Konrad Kaczkowski
'''
from abc import ABCMeta, abstractmethod
import subprocess
import os

class DAO(object):
    '''
    Parent DAO class with interface.
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_data(self):
        ''' get main parameter of the class '''
        raise NotImplementedError('subclasses must override execute()!')
    
    @abstractmethod
    def map_data(self):
        ''' get main parameter of the class '''
        raise NotImplementedError('subclasses must override execute()!')

    def check_file_exists(self, file_to_check):
        ''' Checking if file specified in parameter exists. '''
        if not os.path.isfile(file_to_check):
            raise Exception(file_to_check + " not found!")
        
class PasswordDAO(DAO):
    '''
    DAO class for getting user password
    '''
    def __init__(self, data_wrapper):
        ''' Constructor '''
        super(PasswordDAO, self).__init__()
        self.data_wrapper = data_wrapper

    def get_data(self):
        ''' Obtaining user password from script. '''
        if self.data_wrapper.username == None:
            raise Exception ("Username was not specified.")
        passwd_script = self.data_wrapper.passwd_script
        passwd = subprocess.Popen(passwd_script, \
                    stdout = subprocess.PIPE, shell = True).stdout.read()
                    
        self.map_data(passwd)
    
    def map_data(self, passwd):
        self.data_wrapper.passwd = passwd
        #self.data_wrapper.user_pwd = self.data_wrapper.username + ":" + passwd

class CERNSyscontrolTopDAO(DAO):
    def __init__(self, data_wrapper):
        ''' Constructor '''
        super(CERNSyscontrolTopDAO, self).__init__()
        self.data_wrapper = data_wrapper

    def get_data(self):
        ''' Obtaining syscontrol directory path '''
        syscontrol_top_script = self.data_wrapper.syscontrol_top_script
        bash_command = syscontrol_top_script + \
        self.data_wrapper.syscontrol_top_arguments

        # checking if script exists
        super(CERNSyscontrolTopDAO, self).check_file_exists(syscontrol_top_script)

        syscontrol_top = subprocess.Popen(bash_command, stdout = subprocess.PIPE, \
            shell = True).stdout.read().rstrip()
        self.map_data(syscontrol_top)
        
    def map_data(self, syscontrol_top):
        self.data_wrapper.syscontrol_top = syscontrol_top

class CERNPasswordDAO(DAO):
    '''
    DAO class for getting user password
    '''
    def __init__(self, data_wrapper):
        ''' Constructor '''
        super(CERNPasswordDAO, self).__init__()
        self.data_wrapper = data_wrapper

    def get_data(self):
        ''' Obtaining user password from `get_passwd` script. '''
        script = self.data_wrapper.syscontrol_top + self.data_wrapper.get_passwd_path
        bash_command = script + self.data_wrapper.get_passwd_arguments + \
        self.data_wrapper.domain_name

        # checking if get_passwd script exists
        super(CERNPasswordDAO, self).check_file_exists(script)

        passwd = subprocess.Popen(bash_command, stdout = subprocess.PIPE, shell = True).stdout.read()
        self.map_data(passwd)
    
    def map_data(self, passwd):
        #self.data_wrapper.passwd = passwd
        self.data_wrapper.user_pwd = (self.data_wrapper.CERN_username + ":" + passwd).strip()
        
class CERNwebtabDAO(DAO):
    '''
    DAO class for getting domain data
    '''

    def __init__(self, data_wrapper):
        ''' Constructor '''
        super(CERNwebtabDAO, self).__init__()
        self.data_wrapper = data_wrapper

    def get_data(self):
        ''' Obtaining data from `webtab` script. '''

        #checking if wlstab script exists
        self.data_wrapper.webtab_path = self.data_wrapper.syscontrol_top + \
            self.data_wrapper.webtab_path
        super(CERNwebtabDAO, self).check_file_exists(self.data_wrapper.webtab_path)

        bash_command = self.data_wrapper.webtab_path + " sc_entity=" + \
        self.data_wrapper.domain_name + self.data_wrapper.webtab_arguments
        
        tab_t = subprocess.Popen(bash_command, stdout = subprocess.PIPE, shell = True).stdout.read()
        data_source = []
        for line in tab_t.splitlines():
            arr = line.split()
            data_source.append(arr)
        self.map_data(data_source[0][0])

    def map_data(self, data_source):
        ''' Interpreting the data from `webtab` script '''
        self.data_wrapper.wls_dir = data_source

class CERNwlstabDAO(DAO):
    '''
    DAO class for getting domain data
    '''

    def __init__(self, data_wrapper):
        ''' Constructor '''
        super(CERNwlstabDAO, self).__init__()
        self.data_wrapper = data_wrapper

    def get_data(self):
        ''' Obtaining data from `wlstab` script. '''

        #checking if wlstab script exists
        self.data_wrapper.wlstab_path = self.data_wrapper.syscontrol_top + \
            self.data_wrapper.wlstab_path
        super(CERNwlstabDAO, self).check_file_exists(self.data_wrapper.wlstab_path)

        bash_command = self.data_wrapper.wlstab_path + " sc_entity=" + \
        self.data_wrapper.domain_name + self.data_wrapper.wlstab_arguments
        
        tab_t = subprocess.Popen(bash_command, stdout = subprocess.PIPE, shell = True).stdout.read()
        data_source = []
        for line in tab_t.splitlines():
            arr = line.split()
            data_source.append(arr)

        self.map_data(data_source)

    def map_data(self, data_source):
        ''' Interpreting the data from `wlstab` script - servers and clusters data. '''
        try:
            self.data_wrapper.domain_dir = data_source[0][5]
        except IndexError: 
            raise Exception("Problem with source data occured. Please check the entity name.")
        
        self.data_wrapper.clusters = dict()

        for server in data_source:
            if server[1] == self.data_wrapper.adminserver_name:
                adminserver_host = server[3]
                adminserver_port = server[4]
                self.data_wrapper.adminserver_url = \
                    "https://" + adminserver_host + ":" + adminserver_port
                continue
            cluster_name = server[2]
            cluster = self.data_wrapper.clusters.get(cluster_name)
            if cluster is None and cluster_name != "-":
                cluster = list()
                cluster.append(server[1])
                self.data_wrapper.clusters[server[2]] = cluster
            else:
                cluster.append(server[1])


