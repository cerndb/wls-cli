#*******************************************************************************
# Copyright (C) 2TrueTrue5, CERN
# This software is distributed under the terms of the GNU General Public
# License version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.
#
#
#*******************************************************************************
'''
Created on Jun True9, 2TrueTrue5

@author: Konrad Kaczkowski
'''
import unittest
from Queue import Queue
from wlscli.view.console_ui import ConsoleUI
from wlscli.common.utils import MessageType
from wlscli.common.utils import Mockup
import json
import tempfile
import os, sys, inspect

def get_output(file_path):
    file_to_open = open(file_path, 'r')
    output = json.loads(file_to_open.read())
    file_to_open.close()
    return output

def perform_test(file_path, view):
    f = open(os.devnull, 'w')
    sys.stdout = f
    output = get_output(file_path)
    mockup = Mockup(MessageType.JSON, output)
    
    return view.display(mockup)

class ViewServersCase(unittest.TestCase):
    """
    Test case for server/cluster/domain View functions
    """

    def setUp(self):
        """Set up for every single test."""
        self.view.test_file = \
        tempfile.NamedTemporaryFile(mode = 'w', delete = True)
        pass
        
    def tearDown(self):
        """Clean up for every single test."""
        self.view.test_file.close()
        pass
        
    def test_status_server(self):
        status = perform_test(self.current_dir + '/out/status_server_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
        
    def test_start_server(self):
        status = perform_test(self.current_dir + '/out/start_server_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
        
        status = perform_test(self.current_dir + '/out/start_server_failure.out', \
                                   self.view)
        self.assertEqual(status, True)       
            
    def test_restart_server(self):
        status = perform_test(self.current_dir + '/out/restart_server_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
            
    def test_suspend_server(self):
        status = perform_test(self.current_dir + '/out/suspend_server_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
            
    def test_resume_server(self):
        status = perform_test(self.current_dir + '/out/resume_server_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
    
    def test_stop_server(self):
        status = perform_test(self.current_dir + '/out/stop_server_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
        
        status = perform_test(self.current_dir + '/out/stop_server_failure.out', \
                                   self.view)
        self.assertEqual(status, True)  
        
    @staticmethod
    def set_up():
        ViewServersCase.view = ConsoleUI(Queue())  
        ViewServersCase.current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))     
        
class ViewShowCase(unittest.TestCase):
    """
    Test case for 'show' View functions
    """

    def setUp(self):
        """Set up for every single test."""
        self.view.test_file = \
        tempfile.NamedTemporaryFile(mode = 'w', delete = True)
        
    def tearDown(self):
        """Clean up for every single test."""
        self.view.test_file.close()
            
    def test_list_targets(self):
        status = perform_test(self.current_dir + '/out/show_targets_success.out', \
                                   self.view)
        self.assertEqual(status, True)     
            
    def test_list_libraries(self):
        status = perform_test(self.current_dir + '/out/show_libraries_success.out', \
                                   self.view)
        self.assertEqual(status, True)     
            
    def test_list_apps(self):
        status = perform_test(self.current_dir + '/out/show_apps_success.out', \
                                   self.view)
        self.assertEqual(status, True)     
    
    @staticmethod
    def set_up():
        """Set up for all tests - executed only once"""
        ViewShowCase.view = ConsoleUI(Queue())   
        ViewShowCase.current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))         
 
 
class ViewAdminCase(unittest.TestCase):
    """
    Test case for 'admin_change' View functions
    """

    def setUp(self):
        """Set up for every single test."""
        self.view.test_file = \
        tempfile.NamedTemporaryFile(mode = 'w', delete = True)
        
    def tearDown(self):
        """Clean up for every single test."""
        self.view.test_file.close()
            
    def test_start_edit(self):
        status = perform_test(self.current_dir + '/out/admin_start_success.out', \
                                   self.view)
        self.assertEqual(status, True)     
            
    def test_cancel_edit(self):
        status = perform_test(self.current_dir + '/out/admin_cancel_success.out', \
                                   self.view)
        self.assertEqual(status, True)     
            
    def test_activate(self):
        status = perform_test(self.current_dir + '/out/admin_activate_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
        
        status = perform_test(self.current_dir + '/out/admin_activate_failure.out', \
                                   self.view)
        self.assertEqual(status, True) 
                  
    @staticmethod
    def set_up():
        """Set up for all tests - executed only once"""
        ViewAdminCase.view = ConsoleUI(Queue())     
        ViewAdminCase.current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))           
  
 
class ViewLogsCase(unittest.TestCase):
    """
    Test case for 'logs' View functions
    """

    def setUp(self):
        """Set up for every single test."""
        self.view.test_file = \
        tempfile.NamedTemporaryFile(mode = 'w', delete = True)
        
    def tearDown(self):
        """Clean up for every single test."""
        self.view.test_file.close()
            
    def test_httpaccesslog(self):
        status = perform_test(self.current_dir + '/out/log_httpaccess_success.out', \
                                   self.view)
        self.assertEqual(status, True)
            
    def test_datasourcelog(self):
        status = perform_test(self.current_dir + '/out/log_datasource_success.out', \
                                   self.view)
        self.assertEqual(status, True)
            
    def test_serverlog(self):
        status = perform_test(self.current_dir + '/out/log_server_success.out', \
                                   self.view)
        self.assertEqual(status, True)
            
    def test_domainlog(self):
        status = perform_test(self.current_dir + '/out/log_domain_success.out', \
                                   self.view)
        self.assertEqual(status, True)

        
    @staticmethod
    def set_up():
        """Set up for all tests - executed only once"""
        ViewLogsCase.view = ConsoleUI(Queue())   
        ViewLogsCase.current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))               
        
class ViewAppsCase(unittest.TestCase):
    """
    Test case for apps View functions
    """

    def setUp(self):
        """Set up for every single test."""
        self.view.test_file = \
        tempfile.NamedTemporaryFile(mode = 'w', delete = True)
        
    def tearDown(self):
        """Clean up for every single test."""
        self.view.test_file.close()
            
    def test_start_app(self):
        status = perform_test(self.current_dir + '/out/app_start_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
        
        status = perform_test(self.current_dir + '/out/app_start_failure.out', \
                                   self.view)
        self.assertEqual(status, True)
            
    def test_stop_app(self):
        status = perform_test(self.current_dir + '/out/app_stop_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
        
        status = perform_test(self.current_dir + '/out/app_stop_failure.out', \
                                   self.view)
        self.assertEqual(status, True)
            
    def test_status_app(self):
        status = perform_test(self.current_dir + '/out/app_status_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
            
    def test_redeploy_app(self):
        pass
            
    def test_update_app(self):
        status = perform_test(self.current_dir + '/out/app_update_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
                      
    def test_deploy_app_local(self):
        status = perform_test(self.current_dir + '/out/app_deploy_local_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
        
        status = perform_test(self.current_dir + '/out/app_deploy_local_failure.out', \
                                   self.view)
        self.assertEqual(status, True)
            
    def test_deploy_app_uploaded(self):
        status = perform_test(self.current_dir + '/out/app_deploy_uploaded_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
        
        status = perform_test(self.current_dir + '/out/app_deploy_uploaded_failure.out', \
                                   self.view)
        self.assertEqual(status, True)
    
    def test_deploy_lib_local(self):
        status = perform_test(self.current_dir + '/out/lib_deploy_local_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
        
        status = perform_test(self.current_dir + '/out/lib_deploy_local_failure.out', \
                                   self.view)
        self.assertEqual(status, True)
            
    def test_deploy_lib_uploaded(self):
        status = perform_test(self.current_dir + '/out/lib_deploy_uploaded_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
        
        status = perform_test(self.current_dir + '/out/lib_deploy_uploaded_failure.out', \
                                   self.view)
        self.assertEqual(status, True)     
    
    def test_undeploy_app(self):
        status = perform_test(self.current_dir + '/out/app_undeploy_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
        
        status = perform_test(self.current_dir + '/out/app_undeploy_failure.out', \
                                   self.view)
        self.assertEqual(status, True) 
            
    def test_undeploy_lib(self):
        status = perform_test(self.current_dir + '/out/lib_undeploy_success.out', \
                                   self.view)
        self.assertEqual(status, True)       
        
        status = perform_test(self.current_dir + '/out/lib_undeploy_failure.out', \
                                   self.view)
        self.assertEqual(status, True)      
        
    @staticmethod
    def set_up():
        """Set up for all tests - executed only once"""
        ViewAppsCase.view = ConsoleUI(Queue()) 
        ViewAppsCase.current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))         

        
