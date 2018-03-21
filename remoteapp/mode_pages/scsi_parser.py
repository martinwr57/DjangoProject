#!/usr/bin/env python

import sys
import os, os.path, sys, json, pprint, datetime
import time
from ctypes import *
import binascii
from binascii import crc32
from optparse import OptionParser
import string, time


#**************FAST API IMPORTS***************************
import fast
#**********************************************************


sep = os.sep
cdpath = os.getcwd() + sep

path = '%s%sDownloads%sDELLINQ%s' % (os.environ['USERPROFILE'], sep,sep,sep)
dellinq_data={}
keys = ['Vender ID', 'Product ID', 'Firmware Revision Level', 'Product Serial Number', 'Target Device Name', 'Target Port Identifier 1',
            'Target Port Identifier 2', 'Form Factor Width', 'Form Factor Height', 'Device ID', 'Servo Code Level', 'PCBA Serial Number', 'PCBA Part Number',
            'Disk Media Vendor', 'Motor Serial Number', 'Flex Circuit Assembly Serial Number', 'Head Vendor', 'HDC Revision', 'Actuator Serial Number',
            'Head Disk Assembly', 'Year of Manufacture', 'Week of Manufacture', 'Day of Manufacture', 'Location of Manufacture', 'Dell PPID', 'Medium Rotation Rate', 'Diff', 'SED']

def initalize_dict():
    for k in keys:
        dellinq_data[k]='null'
    return dellinq_data


def main():
    check_in={}
    data = initalize_dict()
    #print data.keys()
    hex_keys = {}
    inquiry = []
    #filelist = os.listdir(path)
    filelist = os.listdir(os.getcwd())

    #filelist = filter(lambda x: not os.path.isdir(x), filelist)
    #newest = max(filelist, key=lambda x: os.stat(x).st_mtime)
    #print newest
    #real_date = time.strftime('%Y/%m/%d %I:%M:%S%p', time.localtime(date))	
    for file_path in filelist:
	data = file_path.split('_')
        ending = file_path.split('.')[-1:][0]
	
        if ending == 'txt':
            
            date = os.path.getmtime(file_path)		
            f = open(file_path, 'r') 
            s = f.readlines()
            for i in s:
                b = i.split(':')
                byte = b[0].replace('0x','')
                byte = int(byte, 16)
                value = b[1].split('  ')[1]
                hex_keys[byte] = value
                inquiry.extend(value.split(' '))
            f.close()
	    
	    
	if '0x00.txt' in data:
	    VSM={}
	    value =''.join(('0x', inquiry[6]))
	    val = int(value, 16)
	    VSM['UEAR'] = val
	    print 'VSM', VSM
	    
	if '0x01.txt' in data:
	    RWER={}
	    RW = {7:'AWRE',6:'ARRE',5:'TB',4:'RC',3:'EER',2:'PER',1:'DTE',0:'DCR'}
	    RTL = ''.join((inquiry[14],inquiry[15]))
	    RWER['RTL'] = RTL
	    #print inquiry 
	    value =''.join(('0x', inquiry[6]))
	    val = int(value, 16)
	    try:
	       val = int(value, 16)
	       out = bin(val)
	       out = out.split('0b')
	       op = out[1]
	       bin_list = list(op)	            
	       bin_list.reverse()
	       for x in range(0,8):
		    RWER[RW[x]] = bin_list[x]	       
	       #print RWER
	    except:
		pass
	    print 'RWER', RWER
	    
	if '0x07.txt' in data:
	    VERM={}
	    ERM = {7:'AWRE',6:'ARRE',5:'TB',4:'RC',3:'EER',2:'PER',1:'DTE',0:'DCR'}
	    RTL = ''.join((inquiry[14],inquiry[15]))
	    VERM['VRTL'] = RTL
	    value =''.join(('0x', inquiry[6]))
	    val = int(value, 16)
	    try:
	       val = int(value, 16)
	       if not val:
		    for x in range(0,4):
			 try:			    
			    VERM[ERM[x]] = '0'
			 except:
			    pass
	       else:
		    out = bin(val)
		    out = out.split('0b')
		    op = out[1]
		    bin_list = list(op)	            
		    bin_list.reverse()
		    for x in range(0,8):
			 VERM[ERM[x]] = bin_list[x]	       
	    except:
		pass
	    print 'VERM', VERM
	if '0x08.txt' in data:
	    CACHE={}
	    CP = {7:'IC',6:'ABPF',5:'CAP',4:'DISC',3:'SIZE',2:'WCE',1:'MF',0:'RCD'}
	    value =''.join(('0x', inquiry[6]))
	    val = int(value, 16)
	    try:
	       val = int(value, 16)
	       if not val:
		    for x in range(0,8):
			 try:			    
			    CACHE[CP[x]] = '0'
			 except:
			    pass
	       else:
		    out = bin(val)
		    out = out.split('0b')
		    op = out[1]
		    bin_list = list(op)	            
		    bin_list.reverse()
		    for x in range(0,8):
			 CACHE[CP[x]] = bin_list[x]	       
	    except:
		pass
	    print 'CACHE', CACHE
	if '0x0A.txt' in data:
	    CMP={}
	    CM = {2:'D_SENSE',1:'GLTSD',0:'RLEC'}
	    value =''.join(('0x', inquiry[6]))
	    try:
	        
	       val = int(value, 16)
	       if not val:
		    for x in range(0,3):
			 try:			    
			    CMP[CM[x]] = '0'
			 except:
			    pass
	       else:
		    out = bin(val)
		    out = out.split('0b')
		    op = out[1]
		    bin_list = list(op)	            
		    bin_list.reverse()
		    for x in range(0,8):
			 CMP[CM[x]] = bin_list[x]	       
		    
	    except:
		pass
	    print 'CMP', CMP	
	if '0x18.txt' in data:
	    PSLUM={}
	    SLU = {4:'TLR'}
	    value =''.join(('0x', inquiry[6]))
	    try:  
	       val = int(value, 16)
	       if not val:
		    PSLUM['TLR'] = '0'	    
		
	       else:
		    out = bin(val)
		    out = out.split('0b')
		    op = out[1]
		    
		    bin_list = list(op)
		    while len(bin_list) <= 7:			
			op = '0' + op
			bin_list = list(op)
	            
		    bin_list.reverse()
		    for x in range(0,8):
			try:
			    PSLUM[SLU[x]] = bin_list[x]
			except:
			    pass
		    
	    
	    except:
		pass
	    print 'PSLUM', PSLUM
	    
	if '0x19.txt' in data:
	    PSPMP={}
	    PM = {6:'CAWT', 5:'BAE',4:'RLM'}
	    NLT = ''.join((inquiry[8],inquiry[9]))
	    IRT = ''.join((inquiry[10],inquiry[11]))
	    PSPMP['NLT'] = NLT
	    PSPMP['IRT'] = IRT
	    value =''.join(('0x', inquiry[6]))
	    val = int(value, 16)
	    print inquiry
	    try:
	       val = int(value, 16)
	       if not val:
		    for x in range(0,4):
			 try:			    
			    PSPMP[PM[x]] = '0'
			 except:
			    pass
	       else:
		    out = bin(val)
		    out = out.split('0b')
		    op = out[1]
		    bin_list = list(op)
		    while len(bin_list) <= 7:			
			op = '0' + op
			bin_list = list(op)
	
		    bin_list.reverse()
		    for x in range(0,8):
			try:
			    PSPMP[PM[x]] = bin_list[x]	 
			except:
			    pass
	    except:
		pass
	    print 'PSPMP', PSPMP
	    
	if '0x1C.txt' in data:
	    IECP={}
	    IEC = {7:'PERF',6:'RESERVED2',5:'EBF',4:'EWASC',3:'DEXCPT',2:'TEST',1:'RESERVED1',0:'LOGERR'}
	    IT = ''.join((inquiry[8],inquiry[11]))
	    RC = ''.join((inquiry[12],inquiry[15]))
	    IECP['IT'] = IT
	    IECP['RC'] = RC
	    value =''.join(('0x', inquiry[6]))
	    val = int(value, 16)
	    print inquiry
	    try:
	       val = int(value, 16)
	       if not val:
		    for x in range(0,4):
			 try:			    
			    IECP[IEC[x]] = '0'
			 except:
			    pass
	       else:
		    out = bin(val)
		    out = out.split('0b')
		    op = out[1]
		    bin_list = list(op)
		    while len(bin_list) <= 7:			
			op = '0' + op
			bin_list = list(op)
	
		    bin_list.reverse()
		    for x in range(0,8):
			 IECP[IEC[x]] = bin_list[x]	       
	    except:
		pass
	    print 'IECP', IECP
       
       
        inquiry=[]        
    print check_in
    
    

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()