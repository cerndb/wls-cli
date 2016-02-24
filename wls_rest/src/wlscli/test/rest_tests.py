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
from mocks import WebLogicMock
from mocks import ApplicationMock
import unittest
from threading import Thread
import inspect, os
     
def perform_test(command, weblogic_mock, app):
    # start weblogic dummy server in a thread
    server_thread = Thread(target = weblogic_mock.handle_request)
    server_thread.start()     
    try:
        app.run(command.split())
    except SystemExit: return 1
    server_thread.join(timeout = 5)
    return app.get_output()

class RESTServersCase(unittest.TestCase):
    """
    Test case for REST server/cluster/domain functions
    """

    def setUp(self):
        """Set up for every single test."""
        self.weblogic_mock.start()
        
    def tearDown(self):
        """Clean up for every single test."""
        self.weblogic_mock.stop()  
        
    def test_start_server(self):
        # start weblogic dummy server in a thread
        command = "Main.py --start server --test --netrc --target" + \
                     " devITDBIMS01_A_1 --url https://"+self.host + ":" + str(self.port)     
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)  
            
    def test_restart_server(self):
        # start weblogic dummy server in a thread
        command = "Main.py --restart server --test --netrc --target" + \
                     " devITDBIMS01_A_1 --url https://"+self.host + ":" + str(self.port)      
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200) 
            
    def test_suspend_server(self):
        # start weblogic dummy server in a thread
        command = "Main.py --suspend server --test --netrc --target" + \
                     " devITDBIMS01_A_1 --url https://"+self.host + ":" + str(self.port)      
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)  
            
    def test_resume_server(self):
        # start weblogic dummy server in a thread
        command = "Main.py --resume server --test --netrc --target" + \
                     " devITDBIMS01_A_1 " + "--url https://"+self.host + ":" + str(self.port)       
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)   
            
    def test_stop_server(self):
        command = "Main.py --stop server --test --netrc --target" + \
                     " devITDBIMS01_A_1 --url https://"+self.host + ":" + str(self.port)     
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200) 
         
    def test_status_server(self):
        command = "Main.py --status server --netrc --test --target" + \
                     " AdminServer --url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)  
              
    @staticmethod
    def set_up():
        """Set up for all tests - executed only once"""
        RESTServersCase.host = 'localhost'
        RESTServersCase.port = 5008
        RESTServersCase.app = ApplicationMock()
        RESTServersCase.weblogic_mock = WebLogicMock(RESTServersCase.host, RESTServersCase.port)
        
class RESTShowCase(unittest.TestCase):
    """
    Test case for REST 'show' functions
    """

    def setUp(self):
        """Set up for every single test."""
        self.weblogic_mock.start()
        
    def tearDown(self):
        """Clean up for every single test."""
        self.weblogic_mock.stop()  
            
    def test_show_targets(self):
        command = "Main.py --show targets --netrc" + \
                     " --test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)  
            
    def test_show_libraries(self):
        command = "Main.py --show libs --netrc" + \
                     " --test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)  
            
            
    def test_show_apps(self):
        command = "Main.py --show apps --netrc" + \
                     " --test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)  
        
    def test_show_wrong_command(self):
        command = "Main.py --show abc --netrc" + \
                     " --test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)
        try:
            result = result[1]
            for response in result:
                self.assertEqual(int(result[response]), 400)  
                
        except TypeError: self.assertEqual(result, 1)  
    
    @staticmethod
    def set_up():
        """Set up for all tests - executed only once"""
        RESTShowCase.host = 'localhost'
        RESTShowCase.port = 5001
        RESTShowCase.app = ApplicationMock()
        RESTShowCase.weblogic_mock = WebLogicMock(RESTShowCase.host, RESTShowCase.port)
 
class RESTAdminCase(unittest.TestCase):
    """
    Test case for 'admin_change' REST functions
    """

    def setUp(self):
        """Set up for every single test."""
        self.weblogic_mock.start()
        
    def tearDown(self):
        """Clean up for every single test."""
        self.weblogic_mock.stop()  
            
    def test_start_edit(self):
        command = "Main.py --admin_change start --netrc" + \
                     " --test " + "--url https://"+self.host + ":" + str(self.port)     
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)  
            
    def test_cancel_edit(self):
        command = "Main.py --admin_change cancel --netrc" + \
                     " --test " + "--url https://"+self.host + ":" + str(self.port)    
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)  
            
    def test_activate(self):
        command = "Main.py --admin_change activate --netrc" + \
                     " --test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)  
            
    def test_wrong_command(self):
        command = "Main.py --admin_change abc --netrc" + \
                     " --test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)
        try:
            result = result[1]
            for response in result:
                self.assertEqual(int(result[response]), 400)  
                
        except TypeError: self.assertEqual(result, 1)
            
                  
    @staticmethod
    def set_up():
        """Set up for all tests - executed only once"""
        RESTAdminCase.host = 'localhost'
        RESTAdminCase.port = 5002
        RESTAdminCase.app = ApplicationMock()
        RESTAdminCase.weblogic_mock = WebLogicMock(RESTAdminCase.host, RESTAdminCase.port)
 
class RESTLogsCase(unittest.TestCase):
    """
    Test case for REST 'logs' functions
    """

    def setUp(self):
        """Set up for every single test."""
        self.weblogic_mock.start()
        
    def tearDown(self):
        """Clean up for every single test."""
        self.weblogic_mock.stop()  
            
    def test_httpaccesslog(self):
        command = "Main.py --logs httpaccess --netrc --target" + \
                     " devITDBIMS01_A_1 --test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)
            
    def test_datasourcelog(self):
        command = "Main.py --logs datasource --netrc --target" + \
                     " devITDBIMS01_A_1 --test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)
            
    def test_serverlog(self):
        command = "Main.py --logs server --netrc --target" + \
                     " devITDBIMS01_A_1 --test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)
            
    def test_serverlog_wrong_target(self):
        command = "Main.py --logs server --netrc --target" + \
                     " ABC --test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 400)
            
    def test_domainlog(self):
        command = "Main.py --logs domain --netrc --test " + \
                     "--url https://"+self.host + ":" + str(self.port)  
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)
            
    def test_wrong_logs(self):
        command = "Main.py --logs abc --netrc" + \
                     " --test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)
        try:
            result = result[1]
            for response in result:
                self.assertEqual(int(result[response]), 400)  
                
        except TypeError: self.assertEqual(result, 1)

    @staticmethod
    def set_up():
        """Set up for all tests - executed only once"""
        RESTLogsCase.host = 'localhost'
        RESTLogsCase.port = 5003
        RESTLogsCase.app = ApplicationMock()
        RESTLogsCase.weblogic_mock = WebLogicMock(RESTLogsCase.host, RESTLogsCase.port)        
        
class RESTAppsCase(unittest.TestCase):
    """
    Test case for REST apps functions
    """

    def setUp(self):
        """Set up for every single test."""
        self.weblogic_mock.start()
        
    def tearDown(self):
        """Clean up for every single test."""
        self.weblogic_mock.stop()
             
            
    def test_start_app(self):
        command = "Main.py --start app --netrc --appname" + \
                     " myapp --test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)
            
    def test_stop_app(self):
        command = "Main.py --stop app --netrc --appname" + \
                     " myapp --test " + "--url https://"+self.host + ":" + str(self.port)    
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)
            
    def test_stop_app_wrong_target(self):
        command = "Main.py --stop app --netrc --appname" + \
                     " ABC --test " + "--url https://"+self.host + ":" + str(self.port)    
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 400)
            
    def test_status_app(self):
        command = "Main.py --status app --netrc --appname" + \
                     " myapp --test " + "--url https://"+self.host + ":" + str(self.port)     
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)
            
    def test_redeploy_local_app(self):
        command = "Main.py --redeploy --netrc --appname" + \
                     " myapp --file " + self.current_dir + \
                     "/war/j2eeapplication-2.0.1-SNAPSHOT.war " + \
        "--test " + "--url https://"+self.host + ":" + str(self.port)   
        
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)
            
    def test_redeploy_uploaded_app(self):
        command = "Main.py --redeploy --netrc --appname" + \
                     " myapp --adminfs --test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)
            
    def test_redeploy_local_lib(self):
        command = "Main.py --redeploy --netrc --libname" + \
                     " mylib --file " + self.current_dir + \
                     "/war/j2eeapplication-2.0.1-SNAPSHOT.war " + \
        "--test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)
            
    def test_redeploy_uploaded_lib(self):
        command = "Main.py --redeploy --netrc --libname" + \
                     " mylib --adminfs --test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)
            
    def test_update_app(self):
        command = "Main.py --update --netrc --appname" + \
                     " myapp --test " + "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)
            
    def test_deploy_app_local(self):
        command = "Main.py --deploy --netrc --targets " + \
        "AdminServer --file " + self.current_dir + \
        "/war/j2eeapplication-2.0.1-SNAPSHOT.war " + \
        "--appname myapp --test " + \
                    "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)  
            
    def test_deploy_app_local_wrong_filepath(self):
        command = "Main.py --deploy --netrc --targets " + \
        "AdminServer --file /home/kkaczkow/abc/" + \
        "j2eeapplication-2.0.1-SNAPSHOT.war " + \
        "--appname myapp --test " + \
                    "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)
        try:
            result = result[1]
            for response in result:
                self.assertEqual(int(result[response]), 400)  
                
        except TypeError: self.assertEqual(result, 1)
            
    def test_deploy_app_uploaded(self):
        command = "Main.py --deploy --netrc --adminfs --targets " + \
        "AdminServer --file " + self.current_dir + \
        "/war/j2eeapplication-2.0.1-SNAPSHOT.war " + \
        "--appname myapp --test " + \
                    "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200) 
            
    def test_deploy_lib_local(self):
        command = "Main.py --deploy --netrc --targets " + \
        "AdminServer --file " + self.current_dir + \
        "/war/j2eeapplication-2.0.1-SNAPSHOT.war " + \
        "--libname mylib --test " + \
                    "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)      
    
    def test_deploy_lib_uploaded(self):
        command = "Main.py --deploy --netrc --adminfs --targets " + \
        "AdminServer --file " + self.current_dir + \
        "/war/j2eeapplication-2.0.1-SNAPSHOT.war " + \
        "--libname mylib --test " + \
                    "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)  
            
    def test_undeploy_app(self):
        pass
        command = "Main.py --undeploy --netrc " + \
        "--appname myapp --test " + \
                    "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200) 
            
    def test_undeploy_app_wrong_target(self):
        pass
        command = "Main.py --undeploy --netrc " + \
        "--appname ABC --test " + \
                    "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 400) 
            
    def test_undeploy_lib(self):
        pass
        command = "Main.py --undeploy --netrc " + \
        "--libname mylib --test " + \
                    "--url https://"+self.host + ":" + str(self.port)
        result = perform_test(command, self.weblogic_mock, self.app)[1]
        for response in result:
            self.assertEqual(int(result[response]), 200)     
 
    @staticmethod
    def set_up():
        """Set up for all tests - executed only once"""
        RESTAppsCase.host = 'localhost'
        RESTAppsCase.port = 5004
        RESTAppsCase.app = ApplicationMock()
        RESTAppsCase.weblogic_mock = WebLogicMock(RESTAppsCase.host, RESTAppsCase.port)
        RESTAppsCase.current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

        
