#!/usr/bin/env python

import SimpleXMLRPCServer
import xmlrpclib
import sys, time, os, os.path
import datetime
import shelve

sep = os.sep
paths = '%s%shddlab%sFileShare%sPerformance_Results%s' % (sep,sep,sep,sep,sep)
dir_name = '%s%shddlab%sPerformance_Results%sMetrics_outputs%s' % (sep,sep, sep,sep,sep)  
	

NAME = os.environ['COMPUTERNAME']
DOMAIN = os.environ['USERDNSDOMAIN']
server_name = '.'.join((NAME, DOMAIN))
server = SimpleXMLRPCServer.SimpleXMLRPCServer((server_name,1332), logRequests=True, allow_none=True)
server.register_introspection_functions()
server.register_multicall_functions()

class workingDatabase:
	
    def __init__(self):
	self.inq = shelve.open('Inquiry.db', flag='c', writeback=True) 
	self.checkin = shelve.open('CheckIn.db', flag='c', writeback=True)
	self.checkout = shelve.open('CheckOut.db', flag='c', writeback=True)
		
    def getInquiryData(self, data, sn):
	"""the group list is passed in to run the analysis between similar products"""
	output = self.inq[sn]
	self.closeConnect('inq')	

    def setInquiryData(self, data, sn):
	"""returns the file name of the new metrics file to be entered in the database
	along with the device info"""
	self.inq[sn] = data
	self.closeConnect('inq')	
	
    def getCheckInData(self, data,sn,mp):
	"""the group list is passed in to run the analysis between similar products"""		
	self.closeConnect('checkin')	

    def setCheckInData(self, data,sn,mp):
	"""returns the file name of the new metrics file to be entered in the database
	along with the device info"""
	key = sn + '_' + mp
	self.checkin[key] = data
	self.closeConnect('checkin')
	
	
    def getCheckOutData(self, data, sn, mp):
	"""the group list is passed in to run the analysis between similar products"""	
	self.closeConnect('checkout')

    def setCheckOutData(self, data, sn, mp):
	"""returns the file name of the new metrics file to be entered in the database
	along with the device info"""
	key = sn + '_' + mp
	self.checkout[key] = data
	self.closeConnect('checkout')
	
	
	
    def closeConnect(self, type):
	if type == 'inq':
	    self.inq.close()
	elif type == 'checkin':
	    self.checkin.close()
	elif type == 'checkout':
	    self.checkout.close()
	else:
	    print 'does not exist'
	
server.register_instance(workingDatabase())

try:
    print 'Use Control-C to exit'
    print server_name

    server.serve_forever()
except KeyboardInterrupt:
    print 'Exiting'
