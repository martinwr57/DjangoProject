#!/usr/bin/env python

import SimpleXMLRPCServer
import xmlrpclib
import sys, time, os, os.path
import datetime

from sqlalchemy import create_engine
from sqlalchemy import sql, schema, types, exc, pool
from sqlalchemy import Table, Integer, Sequence, Column, String, MetaData
from sqlalchemy.orm import sessionmaker




#engine = create_engine('mssql+pyodbc://@DATABASE\SQLEXPRESS/RADatabase')
engine = create_engine('mssql+pyodbc://@DATABASE\AUTOMATION/Automation')

connection = engine.connect()

metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
sep = os.sep

paths = '%s%shddlab%sFileShare%sPerformance_Results%s' % (sep,sep,sep,sep,sep)
dir_name = '%s%shddlab%sPerformance_Results%sMetrics_outputs%s' % (sep,sep, sep,sep,sep)  
	

NAME = os.environ['COMPUTERNAME']
DOMAIN = os.environ['USERDNSDOMAIN']
server_name = '.'.join((NAME, DOMAIN))
server = SimpleXMLRPCServer.SimpleXMLRPCServer((server_name,1332), logRequests=True, allow_none=True)
server.register_introspection_functions()
server.register_multicall_functions()
	
file_names = ["all-in-one.csv"]
#file_names = ["WD_WD3000BKFG-18P2V_299GB_2011-05-11-075838_results.csv"]
class runAnalysis:
	
    def __init__(self):
	self.filenames = []
	self.output_file = ''
		
    def sendFileGroup(self, group, var):
	"""the group list is passed in to run the analysis between similar products"""	
	self.filenames = group
	filename = group.split("\\")[-1:][0]	
	#perf_d2d.run(group, dir_name, var)
	analysis.run(group, dir_name, var)

	

    def setMetrics(self, output):
        self.output_file = output
	"""returns the file name of the new metrics file to be entered in the database
	along with the device info"""
	
	
    def getMetrics(self):
	"""returns the file name of the new metrics file to be entered in the database
	along with the device info"""
	return self.output_file	
	
    
    def make_newfile_name(self, var, mydata):	
	print 'nothing yet...'
	dir_name = '%s%shddlab%sPerformance_Results%sMetrics_outputs%s' % (sep,sep, sep,sep,sep)  
	
	new_data={}
	sn = mydata.keys()[0]
	new_data.update(mydata[sn])
	#data = var.split('_')
	input = {}
	model = new_data['ModelNumber']
	
	new_file= ''.join((dir_name, var))
	inq = Table('DELLInqData', metadata, autoload=True)
	result = Table('Result', metadata, autoload=True)
	s = inq.select(inq.columns.ProductID == model)
		

	rs = s.execute()
	if rs:
	    row = rs.fetchone()   
	    formfactor = float(row['FormFactorWidth']) * 0.001	    
	    rpm = row['MediumRotationRate']
	    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")    
	#    ppid = row['DellPPID']
	    input = {'RPM' : rpm, 'CodeName':new_data['CodeName'], 'Vendor': new_data['Manufacturer'], 'Firmware': new_data['Firmware'], 'Capacity':new_data['Capacity'], 'ModelNumber':model,
	    	     'SerialNumber':new_data['SerialNumber'], 'FormFactor':formfactor, 'Timestamp':timestamp, 'TestName': 'D2D Metrics', 'Reports':new_file}
	    #input = {'CodeName':new_data['CodeName'], 'Vendor': new_data['Manufacturer'], 'Firmware': new_data['Firmware'], 'Capacity':new_data['Capacity'], 'ModelNumber':model,
	    #	     'SerialNumber':new_data['SerialNumber'], 'Timestamp':timestamp, 'TestName': 'D2D Metrics', 'Reports':new_file}
	    i = result.insert()
	    i.execute(input)
	#   
server.register_instance(runAnalysis())

try:
    print 'Use Control-C to exit'
    print server_name

    server.serve_forever()
except KeyboardInterrupt:
    print 'Exiting'


"""if __name__=="__main__":
	server = SimpleXMLRPCServer.SimpleXMLRPCServer(("hddlab.hdd.lab",1332))
	
	print 'xmlrpc server running...'
	server.register_instance(runAnalysis())
	server.serve_forever()
	print 'xmlrpc server running...'"""""
