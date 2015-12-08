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
import datetime

class ResultParser(object):
    '''
    Parent class investigating if executed operation was successful or not
    '''

    def __init__(self):
        ''' Constructor '''
    
    def parse(self, result):
        ''' parse interface '''
        raise NotImplementedError('subclasses must override execute()!')
        
    def check_status(self, output):
        ''' return 0 if communicate was successful, return 1 if not '''
        try:
            if "FAILURE" in output or "already" in output or "failed" in output or\
            "such" in output or "not" in output or \
	        "FAILURE" in output["messages"][0]["severity"]:
                return 1
        except (KeyError, TypeError, IndexError): pass
        return 0
        
        
class RESTParser(ResultParser):
    '''
    Result parser class for REST operations
    '''

    def __init__(self):
        ''' Constructor '''
        super(RESTParser, self).__init__()
        
    def parse(self, mockup):
        ''' parse json output'''
        
        try:
            self.print_result(mockup)
        except TypeError:
            print "Exception during json result parsing"
            return
        
        #return super(RESTParser, self).check_status(json_result)
    
    def print_result(self, mockup):
        # if user wants parsed output
        
        json_result = mockup.message
        raw = mockup.raw
        long_print = mockup.long_print
        servlets = mockup.servlets
        
        if not raw:
            self.print_parsed_json(json_result, long_print, servlets)
                   
        # user wants to print default json output
        else:
            self.print_default_json(json_result)
        
    def print_parsed_json(self, json_result, long, servlets):
        ''' parse json tree and print output'''
        # start/stop/restart/edit/activatge commands
        if json_result.has_key("messages"):
            self.print_message(json_result)
                    
        # logs
        elif json_result.has_key("items") and len(json_result["items"]) > 0 and \
        json_result["items"][0].has_key("recordId"):
            self.print_logs(json_result)
                
        # status (server/cluster/domain)
        elif json_result.has_key("item") and \
        len(filter(lambda x: "/management/wls/latest/servers/id" in \
                    x["uri"], json_result["links"])) > 0 :
            self.print_status(json_result, long)
                    
        # an app
        elif json_result.has_key("item") and \
        len(filter(lambda x: "/management/wls/latest/deployments/application" in \
                    x["uri"], json_result["links"])) > 0 :
            self.print_app(json_result, long, servlets)
            
        # show: apps / libraries
        elif json_result.has_key("items") and len(json_result["items"]) > 0 and \
        (len(filter(lambda x: "/management/wls/latest/deployments/application" in \
                    x["uri"], json_result["links"])) > 0 or 
        len(filter(lambda x: "/management/wls/latest/deployments/library" in \
                    x["uri"], json_result["links"])) > 0) :
            self.print_show_deployments(json_result, long, servlets)
            
        # show jobs
        elif len(filter(lambda x: "/management/wls/latest/jobs" in \
                    x["uri"], json_result["links"])) > 0:
            self.print_jobs(json_result, long, servlets)
                     
        # show: targets
        elif json_result.has_key("items") and (len(json_result["items"]) > 0 and \
        json_result["items"][0].has_key("type")):
            self.print_show_targets(json_result, servlets)
                        
        elif json_result.has_key("items") and len(json_result["items"]) == 0:
            print "Empty list."
        #print
        
    def print_message(self, json_result):
        ''' printing message and its status '''
        for x in json_result["messages"]:
            print "%s : %s" % (x["message"], x["severity"])
        try:
            for error in json_result["item"]["targets"][0]["errors"]:
                print "ERROR: "
                print str(error)
        except (KeyError, TypeError): pass
            
    def print_jobs(self, json_result, long, servlets):
        if (long == True):
            parameters_to_omit = ["name"]
        
        else:
            parameters_to_omit = ["name", "beginTime", "endTime", 
                                  "status", "id", 
                                  "type"]
        #parameters_to_omit = ["name"]
        if not servlets: parameters_to_omit.append("servlets")
        for x in json_result["items"]:
            print "\n%s" % x["name"]
            if long or servlets:
                self.print_dictionary(x, 1, parameters_to_omit)
                continue
            self.print_dictionary_short(x, 1, parameters_to_omit)
            
    def print_logs(self, json_result):
        ''' printing 'logs' operation '''
        for x in json_result["items"]:
            print "\n recordId: " + x["recordId"] + ":"
            parameters_to_omit = ["recordId"]
            self.print_dictionary(x, 1, parameters_to_omit)
    
    def print_show_deployments(self, json_result, long, servlets):
        ''' printing 'show' operation '''
        if (long == True):
            parameters_to_omit = ["name"]
        
        else:
            parameters_to_omit = ["name", "planPath", "sessionsOpenedTotalCount", 
                                  "ejbs", "openSessionsCurrentCount", "applicationType", 
                                  "displayName", "type", "deploymentPath",
                                  "implVersion", "specVersion", "urls"]
        #parameters_to_omit = ["name"]
        if not servlets: parameters_to_omit.append("servlets")
        for x in json_result["items"]:
            print "\n%s" % x["name"]
            if long or servlets:
                self.print_dictionary(x, 1, parameters_to_omit)
                continue
            self.print_dictionary_short(x, 1, parameters_to_omit)
            
    def print_show_targets(self, json_result, servlets):
        ''' printing 'show' operation '''
        parameters_to_omit = ["name"]
        if not servlets: parameters_to_omit.append("servlets")
        for x in json_result["items"]:
            print "\n%s" % x["name"]
            self.print_dictionary(x, 1, parameters_to_omit)
            
    def print_status(self, json_result, long):
        ''' printing 'status' (servers, clusters, domain) operation '''
        if (long == True):
            print "\n%s\n -state: %s" % (json_result["item"]["name"], json_result["item"]["state"])
            #self.print_additional_parameters(json_result["item"]);
            parameters_to_omit = ["name", "state"]
            self.print_dictionary(json_result["item"], 1, parameters_to_omit)
        elif json_result["item"].has_key("state"):
            print "%s\n -state: %s" % (json_result["item"]["name"], json_result["item"]["state"])
            try:
                print " -health: %s\n" % json_result["item"]["health"]
            except KeyError:
                print " -health: shutdown\n"
                
    def print_app(self, json_result, long, servlets):
        ''' printing 'status app' operation '''
        print json_result["item"]["name"] + ":"
        if (long == True):
            parameters_to_omit = ["name"]
        
        else:
            parameters_to_omit = ["name", "planPath", "sessionsOpenedTotalCount", 
                                  "ejbs", "openSessionsCurrentCount", "applicationType", 
                                  "displayName", "type", "deploymentPath",
                                  "implVersion", "specVersion", "urls"]

        if not servlets: parameters_to_omit.append("servlets")
        if long or servlets:
            self.print_dictionary(json_result["item"], 1, parameters_to_omit)
            return
        self.print_dictionary_short(json_result["item"], 1, parameters_to_omit)
                        
                
    def print_dictionary(self, dict_to_print, i = 1, parameters_to_omit = []):
        ''' printing dictionary recursively '''
        for key, value in dict_to_print.iteritems():
            if isinstance(value, dict):
                print (' ' * i) + "-{0}:".format(key)
                self.print_dictionary(value, i + 3)
                
            elif isinstance(value, list):
                if key in parameters_to_omit:
                    continue
                print (' ' * i) + "-{0}:".format(key)
                self.print_list(value, i + 3)
            else:
                if not key in parameters_to_omit:
                    if "beginTime" in key or "endTime" in key:
                        value = datetime.datetime.fromtimestamp(
                            int(str(value)[:-3])).strftime('%Y-%m-%d %H:%M:%S')
                    print (' ' * i) + "-{0} : {1}".format(key, value)
                
    def print_list(self, list_to_print, i = 1):
        ''' printing list recursively '''
        for value in list_to_print:
            if isinstance(value, dict):
                self.print_dictionary(value, i + 3)
                if len(list_to_print) > 1: print
            elif isinstance(value, list):
                self.print_list(list_to_print, i + 3)
            else:
                print (' ' * i) + "-{0}".format(value)
        
        
    def print_dictionary_short(self, dict_to_print, i = 1, parameters_to_omit = []):
        ''' printing dictionary recursively '''
        for key, value in dict_to_print.iteritems():
            if isinstance(value, dict):
                print (' ' * i) + "-{0}:".format(key),
                self.print_dictionary_short(value, i + 3)
                
            elif isinstance(value, list):
                if key in parameters_to_omit:
                    continue
                print (' ' * i) + "-{0}:".format(key),
                self.print_list_short(value, i + 3)
            else:
                if not key in parameters_to_omit:
                    if i == 1:
                        print (' ' * i) + "-{0} : {1}".format(key, value)
                    else:
                        print "{{{0} : {1}}}".format(key, value)
                
    def print_list_short(self, list_to_print, i = 1):
        ''' printing list recursively '''
        for i in range(0, len(list_to_print)):
            print list_to_print[i],
            if i != len(list_to_print)-1: print ",",
        print
        
    def print_default_json(self, json_result):
        ''' printing not parsed json '''
        print json_result
        
class NMParser(ResultParser):
    '''
    Result parser class for Node Manager operations
    '''
        
    def parse(self, nm_result, is_get_domain_data_op):
        ''' Prints output and returns result code '''
        print nm_result.rstrip() + "."
        
        return super(NMParser, self).check_status(nm_result)
        
