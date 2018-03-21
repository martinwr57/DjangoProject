#!/usr/bin/env python

import sys
import os, os.path, sys, json, pprint
import re

from subprocess import Popen, PIPE, STDOUT
import copy
import string, time, datetime
import thread
import threading
import remote_client_db

from ctypes import *
import random

import wmi
import win32com.client
import win32api
import win32file
import win32event
import win32con
sep = os.sep




real_time = time.strftime('%Y/%m/%d %I:%M:%S%p',time.localtime())

sep = os.sep
paths = '%s%shddlab%sFileShare%sPerformance_Results%s' % (sep,sep,sep,sep,sep)
dir_name = '%s%shddlab%sFileShare%sPerformance_Results%sMetrics_outputs%s' % (sep,sep, sep,sep,sep,sep)
dirname2 = '%s%s%s%shddlab%s%sFileShare%s%sPerformance_Results%s%s' % (sep,sep, sep,sep,sep,sep,sep,sep,sep,sep)
cdpath = os.getcwd() + sep


class iom:

    def io_m(scripts, output, data):

	#import pythoncom
	#pythoncom.CoInitialize()
	c = wmi.WMI()
	drives={}
	for disk in c.Win32_DiskDrive():
		
	    if 'H700' not in disk.Model.split(' '):
		location = disk.DeviceID.replace("\\\\.\\",'')
		phy = list(location)
		loc = ''.join((phy[:-1])) + ':' + str(phy[-1:][0])
		drives[str(loc)] = str(disk.SerialNumber)
	cmd = 'Iometer.exe /c' + ' "' + scripts[0] + '" /r '+  output
	#os.system(cmd)
	p = Popen(cmd, stdout = None, stderr = None)
	ret = p.wait()    
	f = open(output, 'r')
	s = f.readlines()
	f.close()
	
	ff = open(output, 'w')   
	for line in s:
	    for PD in drives.keys():
		if PD in line:
		    #replaces 'windows' drive name and location with serial number
		    line = line.replace(PD, drives[PD])
	    ff.writelines(line)
	ff.close()
	
	#f = open(output, 'r')
	#ss = f.read()
	#data['Raw'] = repr(ss)
	#rev_id = time.time(data['Timestamp'])
	#data['rev_id'] = rev_id + '_' + data['ModelNumber']
	#f.close()
	thread.start_new_thread(remote_client_db.data_entry, (data, 'thread_data', 20))
	
#	if ret:            
#            return ret
#        time.sleep(2)
#	if ret == 0:
#	    print 'its done'
#	    analyze = paths + output
#	#    thread.start_new_thread(remote_client_db.data_entry, (sender, 'thread_data', 20))
#	    thread.start_new_thread(remote_client_db.running, (analyze, report,"thread-2", 10)) 

	return     
    
