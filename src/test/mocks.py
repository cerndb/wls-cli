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
Created on Jun 23, 2015

@author: Konrad Kaczkowski
'''
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import sys
sys.path.append('..')
from controller import Controller
from model import Model
import urlparse
import socket
import ssl
import json
from Queue import Queue
from model.data_storage import DataWrapper
from model.data_access import DataGetter

class WebLogicMock(object):
    
    def __init__(self, host, port):
        ''' Constructor '''
        try:
            WebLogicDummyHandler.set_up()
            self.server = WebLogicDummyHTTPServer((host, port), WebLogicDummyHandler)
            self.server.socket = ssl.wrap_socket \
            (self.server.socket, \
             certfile="/ORA/dbs01/syscontrol/projects/wls/scripts/rest/cerndb-infra-wls_rest/cert/server.crt", \
             keyfile="/ORA/dbs01/syscontrol/projects/wls/scripts/rest/cerndb-infra-wls_rest/cert/server.key", \
             server_side = True)

        except socket.error as exception:
            print "ERROR: " + str(exception)
            sys.exit(1)
            
    def stop(self):
        self.server.run = False
        
    def start(self):
        self.server.run = True
        
    def handle_request(self):
        self.server.serve() 
        
            
class WebLogicDummyHTTPServer(HTTPServer):
    
    @property
    def run(self): return self.__run
    @run.setter
    def run(self, value): self.__run = value

    def server_bind(self):
        HTTPServer.server_bind(self)
        self.socket.settimeout(1)

    def get_request(self):
        while self.run:
            try:
                sock, addr = self.socket.accept()
                sock.settimeout(None)
                return (sock, addr)
            except socket.timeout: pass

    def serve(self):
        while self.run:
            try:
                self.handle_request()
            except Exception: pass

class WebLogicDummyHandler(BaseHTTPRequestHandler):
    
    @staticmethod
    def set_up():
        """Set up for all tests - executed only once"""
        entity_name = "wls_itdbims01_dev"
        data_getter = DataGetter()
        WebLogicDummyHandler.data_wrapper = DataWrapper()
        WebLogicDummyHandler.data_wrapper.entity_name = entity_name
        #data_getter.fill_data_wrapper(WebLogicDummyHandler.data_wrapper)

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path).path
        if(self.parse_GET(parsed_path) == 0):
            self.request.sendall(json.dumps({'return':'200'}))
        else:
            self.request.sendall(json.dumps({'return':'400'}))

        self.end_headers()
        return
    
    def do_DELETE(self):
        parsed_path = urlparse.urlparse(self.path).path
        if(self.parse_DELETE(parsed_path) == 0):
            self.request.sendall(json.dumps({'return':'200'}))
        else:
            self.request.sendall(json.dumps({'return':'400'}))
        self.end_headers()
        return

    def do_POST(self):
        parsed_path = urlparse.urlparse(self.path).path
        if(self.parse_POST(parsed_path) == 0):
            self.request.sendall(json.dumps({'return':'200'}))
        else:
            self.request.sendall(json.dumps({'return':'400'}))
        self.end_headers()
        return

    def create_POST_urls_to_check(self):
        urls_to_check = list()
        urls_to_check.append("/management/wls/latest/changeManager/startEdit")
        urls_to_check.append("/management/wls/latest/changeManager/cancelEdit")
        urls_to_check.append("/management/wls/latest/changeManager/activate")
        urls_to_check.append("/management/wls/latest/deployments/application")
        urls_to_check.append("/management/wls/latest/deployments/library")
        #for cluster in self.data_wrapper.clusters:
        #    for server in self.data_wrapper.clusters[cluster]:    
        urls_to_check.append("/management/wls/latest/servers/id/devITDBIMS01_A_1/start")
        urls_to_check.append("/management/wls/latest/servers/id/devITDBIMS01_A_1/shutdown")
        urls_to_check.append("/management/wls/latest/servers/id/devITDBIMS01_A_1/restart")
        urls_to_check.append("/management/wls/latest/servers/id/devITDBIMS01_A_1/suspend")
        urls_to_check.append("/management/wls/latest/servers/id/devITDBIMS01_A_1/resume")
        urls_to_check.append("/management/wls/" +\
                             "latest/deployments/application/id/myapp/start")
        urls_to_check.append("/management/wls/" +\
                             "latest/deployments/application/id/myapp/stop")
        urls_to_check.append("/management/wls/" +\
                             "latest/deployments/application/id/myapp/redeploy")
        urls_to_check.append("/management/wls/" +\
                             "latest/deployments/application/id/myapp/update")
        urls_to_check.append("/management/wls/" +\
                             "latest/deployments/library/id/mylib/redeploy")
        return urls_to_check
    
    def create_DELETE_urls_to_check(self):
        urls_to_check = list()
        urls_to_check.append("/management/wls/latest/deployments/library/id/mylib")
        urls_to_check.append("/management/wls/latest/deployments/application/id/myapp")
        return urls_to_check

    def create_GET_urls_to_check(self):
        urls_to_check = list()
        urls_to_check.append("/management/wls/latest/servers/id/AdminServer")
        urls_to_check.append("/management/wls/latest/targets")
        urls_to_check.append("/management/wls/latest/deployments/library")
        urls_to_check.append("/management/wls/latest/deployments/application")
        #for cluster in self.data_wrapper.clusters:
        #    for server in self.data_wrapper.clusters[cluster]:    
        urls_to_check.append("/management/wls/latest/servers/id/devITDBIMS01_A_1")
        urls_to_check.append("/management/wls/" +\
                             "latest/deployments/application/id/myapp")
        return urls_to_check

    def parse_GET(self, parsed_path):
        urlsToCheck = self.create_GET_urls_to_check()
        if any(url in parsed_path for url in urlsToCheck):
            return 0
        return 1
    
    def parse_DELETE(self, parsed_path):
        urlsToCheck = self.create_DELETE_urls_to_check()
        if any(url in parsed_path for url in urlsToCheck):
            return 0
        return 1

    def parse_POST(self, parsed_path):
        urlsToCheck = self.create_POST_urls_to_check()
        if any(url in parsed_path for url in urlsToCheck):
            return 0
        return 1
    
class ViewMock(object):
    def __init__(self, queue, arguments):
        ''' Constructor '''
        queue.put(arguments[1:])
        self.output = list()
        
    def handle_output(self, data_mockup, is_get_domain_data_op):
        ''' handle_output '''
        self.output.append(data_mockup.view_result_to_parse)
        return 0
        
    def get_output(self):
        return self.output
    
    def print_error(self, exception):
        print "ERROR: " + str(exception.message)
        return 1
    
    def logger_print(self, message, status_code = -1, mode = "INFO"):
        pass


class ApplicationMock(object):
   
    def run(self, request):
        queue = Queue()
        # input parameters are redirected to the view
        self.view = ViewMock(queue, request)
        model = Model()
        controller = Controller(model, self.view, queue)
        controller.run()
        
    def get_output(self):
        return self.view.get_output()