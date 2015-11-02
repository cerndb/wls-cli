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
Created on Jun 19, 2015

@author: Konrad Kaczkowski
'''
import unittest
from Queue import Queue
from view import View
from model.data_storage import DataWrapper
import json
import tempfile

def get_output(file_path):
    file_to_open = open(file_path, 'r')
    output = json.loads(file_to_open.read())
    file_to_open.close()
    return output

def perform_test(file_path, view, data_mockup):
    output = get_output(file_path)
    data_mockup.view_result_to_parse = output
    return view.handle_output(data_mockup)

class ViewServersCase(unittest.TestCase):
    """
    Test case for server/cluster/domain View functions
    """

    def setUp(self):
        """Set up for every single test."""
        self.data_mockup.view_test_file = \
        tempfile.NamedTemporaryFile(mode = 'w', delete = True)
        
    def tearDown(self):
        """Clean up for every single test."""
        self.data_mockup.view_test_file.close()
        
    def test_status_server(self):
        status_code = perform_test('out/status_server_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
        
    def test_start_server(self):
        status_code = perform_test('out/start_server_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
        
        status_code = perform_test('out/start_server_failure.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 1)       
            
    def test_restart_server(self):
        status_code = perform_test('out/restart_server_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
            
    def test_suspend_server(self):
        status_code = perform_test('out/suspend_server_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
            
    def test_resume_server(self):
        status_code = perform_test('out/resume_server_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
    
    def test_stop_server(self):
        status_code = perform_test('out/stop_server_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
        
        status_code = perform_test('out/stop_server_failure.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 1)  
        
    @staticmethod
    def set_up():
        data_mockup = DataWrapper()
        data_mockup.view_operation_type = "REST"
        ViewServersCase.data_mockup = data_mockup
        ViewServersCase.view = View()       
        
class ViewShowCase(unittest.TestCase):
    """
    Test case for 'show' View functions
    """

    def setUp(self):
        """Set up for every single test."""
        self.data_mockup.view_test_file = \
        tempfile.NamedTemporaryFile(mode = 'w', delete = True)
        
    def tearDown(self):
        """Clean up for every single test."""
        self.data_mockup.view_test_file.close()
            
    def test_list_targets(self):
        status_code = perform_test('out/show_targets_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)     
            
    def test_list_libraries(self):
        status_code = perform_test('out/show_libraries_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)     
            
    def test_list_apps(self):
        status_code = perform_test('out/show_apps_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)     
    
    @staticmethod
    def set_up():
        """Set up for all tests - executed only once"""
        data_mockup = DataWrapper()
        data_mockup.view_operation_type = "REST"
        ViewShowCase.data_mockup = data_mockup
        ViewShowCase.view = View()    
 
 
class ViewAdminCase(unittest.TestCase):
    """
    Test case for 'admin_change' View functions
    """

    def setUp(self):
        """Set up for every single test."""
        self.data_mockup.view_test_file = \
        tempfile.NamedTemporaryFile(mode = 'w', delete = True)
        
    def tearDown(self):
        """Clean up for every single test."""
        self.data_mockup.view_test_file.close()
            
    def test_start_edit(self):
        status_code = perform_test('out/admin_start_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)     
            
    def test_cancel_edit(self):
        status_code = perform_test('out/admin_cancel_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)     
            
    def test_activate(self):
        status_code = perform_test('out/admin_activate_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
        
        status_code = perform_test('out/admin_activate_failure.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 1) 
                  
    @staticmethod
    def set_up():
        """Set up for all tests - executed only once"""
        data_mockup = DataWrapper()
        data_mockup.view_operation_type = "REST"
        ViewAdminCase.data_mockup = data_mockup
        ViewAdminCase.view = View()   
  
 
class ViewLogsCase(unittest.TestCase):
    """
    Test case for 'logs' View functions
    """

    def setUp(self):
        """Set up for every single test."""
        self.data_mockup.view_test_file = \
        tempfile.NamedTemporaryFile(mode = 'w', delete = True)
        
    def tearDown(self):
        """Clean up for every single test."""
        self.data_mockup.view_test_file.close()
            
    def test_httpaccesslog(self):
        status_code = perform_test('out/log_httpaccess_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)
            
    def test_datasourcelog(self):
        status_code = perform_test('out/log_datasource_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)
            
    def test_serverlog(self):
        status_code = perform_test('out/log_server_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)
            
    def test_domainlog(self):
        status_code = perform_test('out/log_domain_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)

        
    @staticmethod
    def set_up():
        """Set up for all tests - executed only once"""
        data_mockup = DataWrapper()
        data_mockup.view_operation_type = "REST"
        ViewLogsCase.data_mockup = data_mockup
        ViewLogsCase.view = View()    
        
class ViewAppsCase(unittest.TestCase):
    """
    Test case for apps View functions
    """

    def setUp(self):
        """Set up for every single test."""
        self.data_mockup.view_test_file = \
        tempfile.NamedTemporaryFile(mode = 'w', delete = True)
        
    def tearDown(self):
        """Clean up for every single test."""
        self.data_mockup.view_test_file.close()
            
    def test_start_app(self):
        status_code = perform_test('out/app_start_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
        
        status_code = perform_test('out/app_start_failure.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 1)
            
    def test_stop_app(self):
        status_code = perform_test('out/app_stop_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
        
        status_code = perform_test('out/app_stop_failure.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 1)
            
    def test_status_app(self):
        status_code = perform_test('out/app_status_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
            
    def test_redeploy_app(self):
        pass
            
    def test_update_app(self):
        status_code = perform_test('out/app_update_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
                      
    def test_deploy_app_local(self):
        status_code = perform_test('out/app_deploy_local_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
        
        status_code = perform_test('out/app_deploy_local_failure.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 1)
            
    def test_deploy_app_uploaded(self):
        status_code = perform_test('out/app_deploy_uploaded_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
        
        status_code = perform_test('out/app_deploy_uploaded_failure.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 1)
    
    def test_deploy_lib_local(self):
        status_code = perform_test('out/lib_deploy_local_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
        
        status_code = perform_test('out/lib_deploy_local_failure.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 1)
            
    def test_deploy_lib_uploaded(self):
        status_code = perform_test('out/lib_deploy_uploaded_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
        
        status_code = perform_test('out/lib_deploy_uploaded_failure.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 1)     
    
    def test_undeploy_app(self):
        status_code = perform_test('out/app_undeploy_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
        
        status_code = perform_test('out/app_undeploy_failure.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 1) 
            
    def test_undeploy_lib(self):
        status_code = perform_test('out/lib_undeploy_success.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 0)       
        
        status_code = perform_test('out/lib_undeploy_failure.out', \
                                   self.view, self.data_mockup)
        self.assertEqual(status_code, 1)      
        
    @staticmethod
    def set_up():
        """Set up for all tests - executed only once"""
        data_mockup = DataWrapper()
        data_mockup.view_operation_type = "REST"
        ViewAppsCase.data_mockup = data_mockup
        ViewAppsCase.view = View()   

        