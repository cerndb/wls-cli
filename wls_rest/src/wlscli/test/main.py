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
Created on Aug 12, 2015

@author: Konrad Kaczkowski
'''
import rest_tests
import view_tests
import unittest
from mocks import WebLogicMock
from mocks import ApplicationMock
''' 
This script is used for performing all tests.
'''
def set_up_rest_class(test_class):
    test_class.host = host
    test_class.port = port
    test_class.app = app
    test_class.weblogic_mock = weblogic_mock
    
def test_classes_list(classes_to_run_list):
    for test_class in classes_to_run_list:
        test_class.set_up()
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)
        
if __name__ == '__main__':
    host = 'localhost'
    port = 5000
    app = ApplicationMock()
    weblogic_mock = WebLogicMock(host, port)
    
    rest_classes_to_run = [rest_tests.RESTServersCase, rest_tests.RESTShowCase, \
                           rest_tests.RESTAdminCase, rest_tests.RESTLogsCase, \
                           rest_tests.RESTAppsCase]
    view_classes_to_run = [view_tests.ViewServersCase, view_tests.ViewShowCase, \
                           view_tests.ViewAdminCase, view_tests.ViewLogsCase, \
                           view_tests.ViewAppsCase]

    loader = unittest.TestLoader()
    suites_list = []
    test_classes_list(view_classes_to_run)
    test_classes_list(rest_classes_to_run)

    big_suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)

