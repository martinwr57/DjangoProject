#!/usr/bin/env python

import os, os.path, sys
import win32com.client
import win32api
from xml.etree.ElementTree import *
import codecs
import shutil
import zipfile
import shelve


# Setup fast logger
import fast
from fast.os_validation.windows_validator import WMIDateStringToDate, writeHTML
from fast import log
from fast.test_library.hdd import performance

INFO = log.INFO
CRIT = log.CRIT
WARN = log.WARN

import string, time
from twisted.spread import pb

real_time = time.strftime('%Y/%m/%d %I:%M:%S%p',time.localtime())

sep = os.sep

paths = '%s%sTestData%s' % (os.environ['USERPROFILE'], sep,sep)
pathd = '%s%sDownloads%s' % (os.environ['USERPROFILE'], sep,sep)
#output_dir = os.path.join(os.getcwd(), fast.log_dir, 'os_validation')
output_dir = pathd

strComputer = "."
displayList = ["DeviceName",
                   "DeviceID",
                   "DriverDate",
                   "DriverName",
                   "DriverProviderName",
                   "DriverVersion",
                   "FriendlyName",
                   "InfName",
                   "InstallDate",
                   "Manufacturer",
                   "Name",
                   "Started",
                   "StartMode",
                   "Status"
                   ]
propList = ["DeviceName",
                   "DeviceID",
                   "DriverName",
                   "DriverProviderName",
                   "DriverVersion",
                   "FriendlyName",
                   "InfName",
                   "Manufacturer",
                   "Name",
                   "Started",
                   "StartMode",
                   "Status"
                   ]

class MasterPool(pb.Cacheable):
    def __init__(self, ducks):
        self.observers = []
        self.ducks = ducks
	
    def count(self):
        print "I have device data" % self.ducks.keys()
    def addData(self, duck):
        self.ducks.append(duck)
        for o in self.observers: o.callRemote('addData', duck)
    def removeData(self, duck):
        self.ducks.remove(duck)
        for o in self.observers: o.callRemote('removeData', duck)
    def getStateToCacheAndObserveFor(self, perspective, observer):
        self.observers.append(observer)
        # you should ignore pb.Cacheable-specific state, like self.observers
        return self.ducks # in this case, just a list of ducks
    def stoppedObserving(self, perspective, observer):
        self.observers.remove(observer)

class SlavePool(pb.RemoteCache):
    # This is a cache of a remote MasterDuckPond
    def count(self):
        return len(self.cacheducks)
    def getData(self):
        return self.cacheducks
    def setCopyableState(self, state):
        print " cache - sitting, er, setting ducks"
        self.cacheducks = state
    def observe_addData(self, newDuck):
        print " cache - addData"
        self.cacheducks.append(newDuck)
    def observe_removeData(self, deadDuck):
        print " cache - removeData"
        self.cacheducks.remove(deadDuck)
	
    def getFilename(self):
        self.name=''
	self.mydata = None
	self.dataQueue={}
	db = shelve.open('hdd', 'c')
	filelist = os.listdir(paths)
	
	for file_path in filelist:
	    
	    data_path = paths + file_path 
	    date = os.path.getmtime(data_path)		
	    f = open(data_path, 'r') 
	    self.name = f.name.split("\\")[-1:][0] 
	    s = f.read()
	    self.dataQueue[self.name] = {'Date': date, 'Data':s} #Adds file to queue	
	    db[self.name] = {'Date': date, 'Data':s} #Adds file to queue
	    self.mydata = s
	    f.close()
	#return self.dataQueue
	return db
    
    def getDriverList(self):
	
	ret = 0
	filename = "%s\\drivers" %(output_dir)
	objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
	objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
	colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_PnPSignedDriver")
	if len(colItems) == 0:
	    ret = 1
	driver_root = Element("InstalledDrivers")
	for objItem in colItems:
	    driver_node = SubElement(driver_root, "Driver")
	    for s in propList:
		res = objItem.__getattr__(s)
		if res!= None:
		    property_node = SubElement(driver_node, s)
		    self.assign(property_node, res)

	    if objItem.DriverDate != None:
		property_node = SubElement(driver_node, "DriverDate")
		self.assign(property_node, WMIDateStringToDate(objItem.DriverDate))


	    if objItem.InstallDate != None:
		property_node = SubElement(driver_node, "InstallDate")
		self.assign(property_node, WMIDateStringToDate(objItem.InstallDate))

	#writeXMLTree(filename, driver_root)
	writeHTML(filename, driver_root, "System Drivers", "Driver", displayList)
	return ret
    
    def assign(self, node,obj):
	try:
	    node.text = str(obj)
	except:
	    node.text = " "

    
class analysis(self):
    
    def __init__(self, value):
	self.group_analysis = value
	print 'I have the answer'
	self.set_value(value)
	
	
    def set_value(value):
	group = performance.group_analysis()
	group(value)
	
    
	
    



pb.setUnjellyableForClass(MasterPool, SlavePool)
