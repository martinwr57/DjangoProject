#!/usr/bin/env python



__author__ = "Willie Martin"
__version__ = "$Revision: 1.5 $"


import SimpleXMLRPCServer
import xmlrpclib
import sys, time, os, os.path
import datetime


import re
import subprocess
import string
import thread
import threading

from ctypes import *
import random

import wmi
import win32com.client
import win32api
import win32file
import win32event
import win32con

import remote_client_db
#import scsipassthru_fastinterface
sep = os.sep
NAME = os.environ['COMPUTERNAME']
DOMAIN = os.environ['USERDNSDOMAIN']
server_name = '.'.join((NAME, DOMAIN))
print server_name

paths = '%s%shddlab%sFileShare%sPerformance_Results%s' % (sep,sep,sep,sep, sep)

cdpath = os.getcwd() + sep
server = SimpleXMLRPCServer.SimpleXMLRPCServer((server_name,1332), logRequests=True, allow_none=True)
server.register_introspection_functions()
server.register_multicall_functions()



	
class gateway_connect:
    """Contains XML RPC Server Gateway methods for Test System Client Intefacing.

    """
	
    def __init__(self):
	self.script_filenames = []	
	self.performance_Result_file = ''
		
#    def run_performance_testing(self, group,postproc):
#	"""the group list of iometer scripts are passed in to run the analysis between similar products"""
#	#if postproc:
#	#    remote_client_db.check_in('PT')
#	#remote_client_db.check_in('Checkin')
#	remote_client_db.run_performance(group)
	
    
    def run_performance_multi(self, group,postproc,threadn, sleeptime):
	"""Passes information to Client to do performance testing
        Uses diskpart script to put disk drives online and initializes them before performance testing
	This ensures that the disks are free for metadata and RAID information thus allowing IOMeter to properly test. 
        @type  remote_client_db: Twisted Client
        @param group: Group of IOMeter scripts passed in from Dashboard
        @param postproc: place holder of post processing options
        @param threadn: thread name       
        @param sleeptime: time set to kill thread
        """
	#if postproc:
	#    remote_client_db.check_in('PT')
	#remote_client_db.check_in('Checkin')
	cmd = "diskpart /s c:\\python26\\Lib\\site-packages\\remoteapp\\disk_initial.txt > disk_initial_log.txt"
	os.system(cmd)
	remote_client_db.run_performance(group)
	time.sleep(sleeptime)     
	
		
    def run_verification_testing(self, group, metrics):
	"""the group list of iometer scripts are passed in to run the analysis between similar products"""
	self.script_filenames  = group
	#paths = '%s%shddlab%sPerformance_Results%s' % (sep,sep,sep,sep)
	analysis.run(file_names, paths, metrics)
	

    def drive_inquiry(self, test_type ):
	"""Runs FAST API code to SCSI Commands to retrieve the 0xDC (Dell Inquiry Page)
       
        @type  remote_client_db: Twisted Client
	@type  filetrans: Twisted Client function to transfer SCSI output files
	@type  check_in: Twisted Client function to transfer data to server for entry into database
        @param threadn: thread name       
        @param sleeptime: time set to kill thread
        """
	self.inq=[]
	
	cmd ='scsipassthru_fastinterface.py'
	var = os.system(cmd)
	

    def drive_mode_pages(self, test_type ):
	"""Runs FAST API code to SCSI Commands to retrieve the 0xDC (Dell Inquiry Page)
       
        @type  remote_client_db: Twisted Client
	@type  filetrans: Twisted Client function to transfer SCSI output files
	@type  check_in: Twisted Client function to transfer data to server for entry into database
        @param threadn: thread name       
        @param sleeptime: time set to kill thread
        """
	self.inq=[]
	
	cmd ='getsupportedmodepages.py ' + test_type
	var = os.system(cmd)
	return var
	
	
    def system_query(self):
	"""Runs FAST API code to query Test System for configuration and Drives in use      
        
        """
	cmd ='system_check_report.py'
	os.system(cmd)


    def system_check(self):
	remote_client_db.check_systems('SystemCheck')
	"""returns the file name of the new metrics file to be entered in the database
	along with the device info"""
	



server.register_instance(gateway_connect())

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
