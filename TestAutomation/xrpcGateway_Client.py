#!/usr/bin/env python

import SimpleXMLRPCServer
import xmlrpclib
import sys, time, os, os.path
import datetime
from remoteapp import remote_client_db, convertdata
sep = os.sep
NAME = os.environ['COMPUTERNAME']
DOMAIN = os.environ['USERDNSDOMAIN']
server_name = lower('.'.join(NAME, DOMAIN))
paths = '%s%shddlab%sPerformance_Results%s' % (sep,sep,sep,sep)


server = SimpleXMLRPCServer.SimpleXMLRPCServer((server_name,1332), logRequests=True, allow_none=True)
server.register_introspection_functions()
server.register_multicall_functions()
	
#file_names = ["XQV03JDA.csv", "XQV03L1A.csv", "XQV03LJA.csv", "XQV03LKA.csv", "XQV03PRA.csv", "XQV03R6A.csv"]
file_names = ["1 1.csv", "2 1.csv", "3 1.csv", "4 1.csv", "5 1.csv", "6 1.csv"]
class gateway_connect:
	
    def __init__(self):
	self.script_filenames = []	
	self.performance_Result_file = ''
		
    def run_performance_testing(self, group, metrics):
	"""the group list of iometer scripts are passed in to run the analysis between similar products"""
	self.script_filenames  = group
	#paths = '%s%shddlab%sPerformance_Results%s' % (sep,sep,sep,sep)
	analysis.run(file_names, paths, metrics)
	

    def setMetrics(self, output):
        self.output_file = output
	"""returns the file name of the new metrics file to be entered in the database
	along with the device info"""
	
	
    def getMetrics(self):
	"""returns the file name of the new metrics file to be entered in the database
	along with the device info"""
	return self.output_file	
	

server.register_instance(runAnalysis())

try:
    print 'Use Control-C to exit'
    server.serve_forever()
except KeyboardInterrupt:
    print 'Exiting'


"""if __name__=="__main__":
	server = SimpleXMLRPCServer.SimpleXMLRPCServer(("hddlab.hdd.lab",1332))
	
	print 'xmlrpc server running...'
	server.register_instance(runAnalysis())
	server.serve_forever()
	print 'xmlrpc server running...'"""""
