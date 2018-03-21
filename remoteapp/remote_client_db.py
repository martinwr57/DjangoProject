#!/usr/bin/env python


import binascii
from binascii import crc32
from optparse import OptionParser
import os, os.path, sys, json, pprint, datetime
import re

from subprocess import Popen, PIPE, STDOUT
import copy
import string, time, datetime
import thread
import threading
import adodbapi

from ctypes import *
import random

import wmi
import win32com.client
import win32api
import win32file
import win32event
import win32con

############ Twisted Python Network Framework imports ############
from twisted.protocols import basic
from twisted.application import service, internet
from twisted.internet import reactor, protocol, defer, threads
from twisted.internet.protocol import ServerFactory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import FileSender
from twisted.internet.defer import Deferred
from twisted.spread import pb, jelly
from twisted.enterprise import adbapi
from zope.interface import interface, implements

from twisted.cred import checkers, portal, credentials
from twisted.python import log
############ Twisted Python Network Framework imports ############

import xmlrpclib



model_map = { \
    "ST3500620SS" : "Seagate Moose SAS_DUP",
    "ST3750630SS" : "Seagate Moose SAS_DUP",
    "ST31000640SS" : "Seagate Moose SAS_DUP",
    "ST3146356SS" : "Seagate Hurricane_DUP",
    "ST3300656SS" : "Seagate Hurricane_DUP",
    "ST3450856SS" : "Seagate Hurricane_DUP",
    "ST3250310NS" : "Seagate Moose SATA_DUP",
    "ST3500320NS" : "Seagate Moose SATA_DUP",
    "ST3750330NS" : "Seagate Moose SATA_DUP",
    "ST31000340NS" : "Seagate Moose SATA_DUP",
    "ST3400755SS" : "Seagate Timberland NS_DUP",
    "MBA3073RC" : "Fujitsu Allegro 10LX_DUP",
    "MBA3147RC" : "Fujitsu Allegro 10LX_DUP",
    "MBA3300RC" : "Fujitsu Allegro 10LX_DUP",
    "WDCWD1602ABKS-1" : "WD Pinnacle (XL320 RE)",
    "WDCWD2502ABYS-1" : "WD Pinnacle (XL320 RE)",
    "WDCWD5002ABYS-1" : "WD Pinnacle (XL320 RE)",
    "WDCWD7502ABYS-1" : "WD Mars (XL333 RE)",
    "WDCWD1002FBYS-1" : "WD Mars (XL333 RE)",
    "MHZ2080BK" : "Fujitsu Aries (A160-ED)",
    "MHZ2160BK" : "Fujitsu Aries (A160-ED)",
    "MHZ2250BK" : "Fujitsu Aries (A160-ED)",
    "ST973452SS" : "Seagate Hornet_DUP",
    "ST9146852SS" : "Seagate Hornet_DUP",
    "ST9146752SS" : "Seagate Hornet_DUP, SED",
    "ST9146803SS" : "Seagate Firefly_DUP",
    "ST9300603SS" : "Seagate Firefly_DUP",
    "ST9300503SS" : "Seagate Firefly_DUP, SED",
    "ST9500430SS" : "Seagate Dragonfly_DUP",
    "ST9500431SS" : "Seagate Dragonfly_DUP, SED",
    "ST3300657SS" : "Seagate Eagle_DUP",
    "ST3450857SS" : "Seagate Eagle_DUP",
    "ST3600057SS" : "Seagate Eagle_DUP",
    "ST3450757SS" : "Seagate Eagle_DUP, SED",
    "ST3600957SS" : "Seagate Eagle_DUP, SED",
    "ST3600002SS" : "Seagate Eagle RP_DUP",
    "ST3500414SS" : "Seagate Muskie_DUP",
    "ST31000424SS" : "Seagate Muskie_DUP",
    "ST32000444SS" : "Seagate Muskie_DUP",
    "ST31000425SS" : "Seagate Muskie_DUP, SED",
    "ST32000445SS" : "Seagate Muskie_DUP, SED",
    "ST9500530NS" : "Seagate Dragonfly ES_DUP",
    "ST3500514NS" : "Seagate Muskie ES_DUP",
    "ST31000524NS" : "Seagate Muskie ES_DUP",
    "ST32000544NS" : "Seagate Muskie ES_DUP",
    "MBD2147RC" : "Fujitsu Allegro 11SE_DUP",
    "MBD2300RC" : "Fujitsu Allegro 11SE_DUP",
    "MBE2073RC" : "Fujitsu Allegro 11SX_DUP",
    "MBE2147RC" : "Fujitsu Allegro 11SX_DUP",
    "HUC103014CSS600" : "Hitachi Cobra C_DUP",
    "HUC103030CSS600" : "Hitachi Cobra C_DUP",
    "HUC151473CSS600" : "Hitachi King Cobra C_DUP",
    "HUC151414CSS600" : "Hitachi King Cobra C_DUP",
    "HUS156030VLS600" : "Hitachi Viper C_DUP",
    "HUS156045VLS600" : "Hitachi Viper C_DUP",
    "HUS156060VLS600" : "Hitachi Viper C_DUP",
    "WDCWD1460BKFG-1" : "WD Rigel (SL150)_DUP",
    "WDCWD3000BKFG-1" : "WD Rigel (SL150)_DUP",
    "WDCWD1460BKFG-1" : "WD Rigel (SL150) 6Gb_DUP",
    "WDCWD3000BKFG-1" : "WD Rigel (SL150) 6Gb_DUP",
    "WDCWD3000BKHG-1" : "WD Vega_DUP",
    "WDCWD6000BKHG-1" : "WD Vega_DUP",
    "WDCWD2000FYYG-1" : "WD Bach_DUP",
    "HE161HJ" : "Samsung F1R",
    "WDCWD2002FYPS-1" : "WD Sparta ES_DUP",
    "WDCWD2003FYYS-1" : "WD Mantis ES",
    "WDCWD1003FBYX-1" : "WD Vulcan_DUP_1TB",
    "WDCWD2503ABYX-1" : "WD Summit_DUP_250GB",
    "WDCWD5003ABYX-1" : "WD Summit_DUP_500GB",
    "HUA722020ALA330" : "Hitachi Jupiter K ES_DUP",
    "ST9600204SS" : "Seagate Firestorm_DUP",
    "ST9600104SS" : "Seagate Firestorm_DUP, SED",
    "MBF2300RC" : "Toshiba Allegro 12SE_DUP",
    "MBF2600RC" : "Toshiba Allegro 12SE_DUP",
    "HE253GJ" : "Samsung F3R ES",
    "HE502HJ" : "Samsung F3R ES",
    "HE103SJ" : "Samsung F3R ES",
    "HUC106030CSS600" : "Hitachi Cobra D_DUP",
    "HUC106060CSS600" : "Hitachi Cobra D_DUP",
    "ST936751SS" : "Seagate Maverick_non-DUP",
    "ST973451SS" : "Seagate Maverick_non-DUP",
    "WDCWD1000FYPS-1" : "WD Hulk (GP250RE2)",
    "HUS154530VLS300" : "Hitachi Viper B+_DUP",
    "HUS154545VLS300" : "Hitachi Viper B+_DUP",
    "HUS153073VLS300" : "Hitachi Viper B_DUP",
    "HUS153014VLS300" : "Hitachi Viper B_DUP",
    "HUS153030VLS300" : "Hitachi Viper B_DUP",
    "HUC101473CSS300" : "Hitachi Cobra B_DUP",
    "HUC101414CSS300" : "Hitachi Cobra B_DUP",
    "HUA721050KLA330" : "Hitachi Gemini K",
    "HUA721075KLA330" : "Hitachi Gemini K",
    "HUA721010KLA330" : "Hitachi Gemini K",
    "ST973452SS" : "Seagate Hornet_DUP",
    "ST9146852SS" : "Seagate Hornet_DUP",
    "ST9146803SS-H" : "Seagate Firefly_DUP",
    "ST9146803SS" : "Seagate Firefly_DUP",
    "ST9300603SS" : "Seagate Firefly_DUP",
    "ST9500430SS" : "Seagate Dragonfly_DUP",
    "ST3300657SS" : "Seagate Eagle_DUP",
    "ST3450857SS" : "Seagate Eagle_DUP",
    "ST3600057SS" : "Seagate Eagle_DUP",
    "ST3600002SS" : "Seagate Eagle RP_DUP",
    "MBD2147RC" : "Fujitsu Allegro 11SE_DUP",
    "MBD2147RC" : "Fujitsu Allegro 11SE_DUP",
    "MBD2300RC" : "Fujitsu Allegro 11SE_DUP",
    "MBE2073RC" : "Fujitsu Allegro 11SX_DUP",
    "MBE2147RC" : "Fujitsu Allegro 11SX_DUP",
    "HUC103014CSS600" : "Hitachi Cobra C_DUP",
    "HUC103030CSS600" : "Hitachi Cobra C_DUP",
    "WD5000YS-18MPB1" : "WD Zeus ES",
    "HDS725050KLA360" : "Hitachi Kurofune II",
    "MAX3036RC" : "Fujitsu Allegro 9LX",
    "MAX3073RC" : "Fujitsu Allegro 9LX",
    "MAX3147RC" : "Fujitsu Allegro 9LX",
    "HUS151436VLS300" : "Hitachi Viper A'",
    "HUS151473VLS300" : "Hitachi Viper A'",
    "HUS151414VLS300" : "Hitachi Viper A'",
    "MAY2036RC" : "Fujitsu Allegro 9SE+",
    "MAY2073RC" : "Fujitsu Allegro 9SE+",
    "ATLAS10K5-073SAS" : "Maxtor Genesis",
    "ATLAS10K5-147SAS" : "Maxtor Genesis",
    "ATLAS10K5-300SAS" : "Maxtor Genesis",
    "ATLAS15K2-036SAS" : "Maxtor Blackbird ",
    "ATLAS15K2-073SAS" : "Maxtor Blackbird ",
    "ATLAS15K2-147SAS" : "Maxtor Blackbird ",
    "ST336754SS" : "Seagate Cheetah 15K.4",
    "ST373454SS" : "Seagate Cheetah 15K.4",
    "ST3146854SS" : "Seagate Cheetah 15K.4",
    "WD800JD-75MSA3" : "WD Unicorn II",
    "WD1600JS-75NCB3" : "WD Hawk II",
    "WD2500JS-75NCB3" : "WD Hawk II",
    "ST380819AS" : "Seagate Puma II",
    "ST3160828AS" : "Seagate Puma II",
    "ST3808110AS" : "Seagate Tonka II",
    "ST3160812AS" : "Seagate Tonka II",
    "ST3250824AS" : "Seagate Tonka Plus",
    "ST936701SS" : "Seagate Savvio (10K.1)",
    "ST973401SS" : "Seagate Savvio (10K.1)",
    "MHV2040BS" : "Fujitsu Mercury 60-ED",
    "MHW2040BS" : "Fujitsu Mercury 80-ED",
    "MHW2080BS" : "Fujitsu Mercury 80-ED",
    "ST3250620NS" : "Seagate Galaxy ES",
    "ST3500630NS" : "Seagate Galaxy ES",
    "ST3750640NS" : "Seagate Galaxy ES",
    "WD1600YS-18SHB2" : "WD Hawk ES",
    "WD2500YS-18SHB2" : "WD Hawk ES",
    "ST373455SS" : "Seagate Timberland 15K non-DUP (Field only)",
    "ST3146855SS" : "Seagate Timberland 15K non-DUP (Field only)",
    "ST3300655SS" : "Seagate Timberland 15K non-DUP (Field only)",
    "ST373355SS" : "Seagate Timberland T10 non-DUP",
    "ST3146755SS" : "Seagate Timberland T10 non-DUP",
    "ST3300555SS" : "Seagate Timberland T10 non-DUP",
    "ST973402SS" : "Seagate Firebird non-DUP",
    "ST9146802SS" : "Seagate Firebird non-DUP",
    "MHW2080BK" : "Fujitsu Aries (A80-ED)",
    "MHW2120BK" : "Fujitsu Aries (A80-ED)",
    "WDCWD800AAJS-1" : "WD Unicorn ES",
    "WDCWD5001ABYS-1" : "WD Tornado (XL160M)",
    "ST373355SS" : "Seagate Timberland T10_DUP",
    "ST3146755SS" : "Seagate Timberland T10_DUP",
    "ST3300555SS" : "Seagate Timberland T10_DUP",
    "WD1601ABYS-18C0A0" : "WD Sequoia (XL160)",
    "HE160HJ" : "Samsung S166R",
    "ST973402SS" : "Seagate Firebird_DUP",
    "ST9146802SS" : "Seagate Firebird_DUP",
    "ST373455SS" : "Seagate Timberland 15K_DUP",
    "ST3146855SS" : "Seagate Timberland 15K_DUP",
    "ST3300655SS" : "Seagate Timberland 15K_DUP",
    "MBB2073RC" : "Fujitsu Allegro 10SE_DUP",
    "MBB2147RC" : "Fujitsu Allegro 10SE_DUP",
    "MBC2036RC" : "Fujitsu Allegro 10SX_DUP",
    "MBC2073RC" : "Fujitsu Allegro 10SX_DUP",
    "MCBQE25G5MPQ-0VAD3" : "Samsung RBX",
    "MCCOE50G5MPQ-0VAD3" : "Samsung RBX",
    "MCB4E50G5MXP-0VBD3" : "Samsung SS805",
    "MCCOE1HG5MXP-0VBD3" : "Samsung SS805",
    "LB150S" : "LB150S",
    "WDCWD6000BKHG-1" : "WD Vega_600GB",
    "HitachiHUA72202" : "Hitachi JupiterK",
    "ST9300605SS" : "Compass ST9300605SS ",
    "ST9900805SS" : "Compass ST9900805SS ",
    "ST91000640NS" : "Airwalker ST91000640NS ",


}


real_time = time.strftime('%Y/%m/%d %I:%M:%S%p',time.localtime())

sep = os.sep
paths = '%s%shddlab%sFileShare%sPerformance_Results%s' % (sep,sep,sep,sep,sep)
dir_name = '%s%shddlab%sFileShare%sPerformance_Results%sMetrics_outputs%s' % (sep,sep, sep,sep,sep,sep)
dirname2 = '%s%s%s%shddlab%s%sFileShare%s%sPerformance_Results%s%s' % (sep,sep, sep,sep,sep,sep,sep,sep,sep,sep)
cdpath = os.getcwd() + sep

strComputer = "."


class MessageLogger:
    """
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    """
    def __init__(self, file):
        self.file = file

    def log(self, message):
        """Write a message to the file."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()


class Sender:
    """Sender Class, Twisted Client used transmit information and python objects across the network.
	
    """
	
    def __init__(self, type, data, analysis):
	self.data = data
	self.analysis = analysis
	self.device= ''
	self.dellinq_file = ''
	self.test_type = type
	
	
        self.logger = MessageLogger(open('log\client_logger.txt', "a"))
        self.logger.log("Client is awake now at %s" % time.asctime(time.localtime(time.time())) )	
	self.logger.close()


    def phase6(self, dummy):
        reactor.stop()
	
    
    def ok(self, response):
	self.logger = MessageLogger(open('log\client_logger.txt', "a"))
	self.logger.log("[Transfer successful  %s] at %s" %
                         response, time.asctime(time.localtime(time.time())) )
	
	self.logger.close()
	reactor.stop()
	return 

    def notOk(self, failure):
	self.logger = MessageLogger(open('log\client_logger.txt', "a"))
        if failure.type == jelly.InsecureJelly:
	    self.logger.log("InsecureJelly")
        else:
	    self.logger.log("transmission error: Reactor threads" )
	    self.logger.log(failure)
	self.logger.close()
	reactor.stop()
        return 

    def add_devicedata(self, remote):
	data = self.data
	#closing = self.obj
	d = remote.callRemote("addDeviceData", data)	
	#d.addCallback(self.ok).addErrback(self.notOk)	
	d.addCallback(self.ok)
		
    def add_testdata(self, remote):
	data = self.data
        d = remote.callRemote("addTestData", data)	
	#d.addCallback(self.ok).addErrback(self.notOk)	
	d.addCallback(self.ok)
	
	
    def add_resultdata(self, remote):
	data = self.data
        d = remote.callRemote("addResultData", data)
	#d.addCallback(self.ok).addErrback(self.notOk)	
	d.addCallback(self.ok)	

    def add_devicedata_batch(self, remote):
	data = self.data
	self.remote = remote
	d = remote.callRemote("addDeviceData_batch", data)		
	#d.addCallback(self.ok)			
	
    def add_testdata_batch(self, remote):	
	data = self.data
	d = self.remote.callRemote("addTestData_batch", data)		
	#d.addCallback(self.ok)		
	#d.addCallback(self.ok).addErrback(self.notOk)	
	
	
    def add_resultdata_batch(self, remote):
	data = self.data
	self.remote = remote
        d = remote.callRemote("addResultData_batch", data)		
	#d.addCallback(self.ok)
	#d.addCallback(self.ok).addErrback(self.notOk)
	
    def add_runanalysis(self, remote):
	data = self.analysis
	#print data
        d = self.remote.callRemote("PostAnalysis", data)		
	#d.addCallback(self.ok)
	#d.addCallback(self.ok).addErrback(self.notOk)
	
    def add_inquiry(self, remote):
	data = self.data
        d = remote.callRemote("LoadDellInqData", data)
	d.addCallback(self.ok).addErrback(self.notOk)
	#d.addCallback(self.add_systemdata)
	#d.addCallback(self.ok)

    def add_modepages(self, remote):
	data = self.data
        d = remote.callRemote("LoadModePages", data)
	d.addCallback(self.ok).addErrback(self.notOk)
	#d.addCallback(self.add_systemdata)
	#d.addCallback(self.ok)
	
   
    
    def add_systemdata(self, remote):
	data = self.data
	output = self.add_get_sys_info()
	ctrl_listing = self.get_sys_ctrl_list()
	
	dns = output[0] + '.hdd.lab'
	server = {'SystemName': output[0], 'ModelName': output[1], 'Controller': ctrl_listing, 'NetworkID':dns, 'OS':'Windows Server 2008'}
	d = remote.callRemote("addServerData", server)	
	d.addCallback(self.ok).addErrback(self.notOk)	
	

    def add_get_sys_info(self):
	"""Returns the hostname, model name, and service tag of the SUT."""
	if sys.platform[:3] == 'win':
	    sys_name = os.environ['COMPUTERNAME']
	    try:
		import wmi
		w = wmi.WMI()
		

		bios_query_data = w.Win32_BIOS.query()[0]            
		service_tag =  bios_query_data.SerialNumber.replace(' ', '')

		system_query_data = w.Win32_ComputerSystem.query()[0]
		model_name = system_query_data.Model.replace(' ', '')
		
	    except Exception, e:
		#logger(WARN, "Failed to get system info:  %s" % e)
		service_tag = "unknown"
		model_name = "unknown"

	else:
	    sys_name = os.environ['HOSTNAME']
	    try:
		from subprocess import Popen, PIPE
                
		cmd = 'dmidecode -s system-serial-number'
		p = Popen(cmd, shell = True, stdout = PIPE)
		retcode = p.wait()
		output = p.stdout.read()
		service_tag = output.replace(' ', '').strip()
            
		cmd = 'dmidecode -s system-product-name'
		p = Popen(cmd, shell = True, stdout = PIPE)
		retcode = p.wait()
		output = p.stdout.read()
		model_name = output.replace(' ', '').strip()
	    except Exception, e:
		#logger(WARN, "Failed to get system info:  %s" % e)
		service_tag = "unknown"
		model_name = "unknown"

	return sys_name, model_name, service_tag
  

class FileIOClient(basic.LineReceiver):
    """ file sender """
 
    def __init__(self, path, controller):
        """ """
        self.path = path
        self.controller = controller
 
        self.infile = open(self.path, 'rb')
        self.insize = os.stat(self.path).st_size
 
        self.result = None
        self.completed = False
 
        self.controller.file_sent = 0
        self.controller.file_size = self.insize
 
    def _monitor(self, data):
        """ """
        self.controller.file_sent += len(data)
        self.controller.total_sent += len(data)
 
        # Check with controller to see if we've been cancelled and abort
        # if so.
        if self.controller.cancel:
            print 'FileIOClient._monitor Cancelling'
 
            # Need to unregister the producer with the transport or it will
            # wait for it to finish before breaking the connection
            self.transport.unregisterProducer()
            self.transport.loseConnection()
 
            # Indicate a user cancelled result
            self.result = TransferCancelled('User cancelled transfer')
 
        return data
 
    def cbTransferCompleted(self, lastsent):
        """ """
        self.completed = True
        self.logger.log("[transmission completed at %s]" %
                        time.asctime(time.localtime(time.time())))

        self.transport.loseConnection()
	
 
    def connectionMade(self):
        """ """
        self.logger = MessageLogger(open('log\client_logger.txt', "a"))
        self.logger.log("[connected at %s]" %
                        time.asctime(time.localtime(time.time())))

        instruction = dict(file_size=self.insize,
                           original_file_path=self.path)
        instruction = json.dumps(instruction)
        self.transport.write(instruction+'\r\n')
        sender = FileSender()
        sender.CHUNK_SIZE = 2 ** 16
        d = sender.beginFileTransfer(self.infile, self.transport,
                                     self._monitor)
        d.addCallback(self.cbTransferCompleted)
 
    def connectionLost(self, reason):
        """
            NOTE: reason is a twisted.python.failure.Failure instance
        """
        self.logger.log("[Connection losted and client disconnected at %s]" %
                        time.asctime(time.localtime(time.time())))

        from twisted.internet.error import ConnectionDone
        basic.LineReceiver.connectionLost(self, reason)
        print ' - connectionLost\n  * ', reason.getErrorMessage()
        print ' * finished with',self.path
        self.logger.log(reason.getErrorMessage())
        self.logger.log("[finished with %s ]" % self.path)
        self.infile.close()
        if self.completed:
            self.controller.completed.callback(self.result)
	    self.logger.log(self.result)

        else:
            self.controller.completed.errback(reason)
	    self.logger.log(reason)

	
	#if reactor.running:
	#    print 'its running, now stop it'
	self.logger.close()
	reactor.stop()
	return
 
class FileIOClientFactory(ClientFactory):
#class FileIOClientFactory(ReconnectingClientFactory):

    """ file sender factory """
    protocol = FileIOClient
 
    def __init__(self, path, controller):
        """ """
        self.path = path
        self.controller = controller
 
    def clientConnectionFailed(self, connector, reason):
        """ """
        ClientFactory.clientConnectionFailed(self, connector, reason)
        self.controller.completed.errback(reason)
 
    def buildProtocol(self, addr):
        """ """
        print ' + building protocol'
        p = self.protocol(self.path, self.controller)
        p.factory = self
        return p
 
 
def transmitOne(path, address='hddlab.hdd.lab', port=1331):
    """ helper for file transmission """
    controller = type('test',(object,),{'cancel':False, 'total_sent':0,'completed':Deferred()})
    f = FileIOClientFactory(path, controller)
    reactor.connectTCP(address, port, f)
    return controller.completed
 
 
def build_parser():
    """ builds the command line parser """
    parser = OptionParser()
    portHelp = 'Which port to use. (default "1234")'
    addressHelp = 'Which address to use. (default "localhost")'
    serverHelp = "Use server"
    clientHelp = "Use client"
    parser.add_option("--port", dest="port", default='1234', help=portHelp, metavar="PORT")
    parser.add_option("--address", dest="address", default='127.0.0.1', help=addressHelp, metavar="ADDRESS")
    parser.add_option("--server",action="store_true",default=False, dest="use_server",help=serverHelp)
    parser.add_option("--client",action="store_true",default=False, dest="use_client",help=clientHelp)
    return parser
 
def avatar():
    #lego = CachingRealm.
    closeshop = closeShop()
    sender = Sender('data', closeshop, 'no_file')
    factory = pb.PBClientFactory()
    reactor.connectTCP("dashboard.hdd.lab", 1331, factory)
    def1 = factory.login(credentials.UsernamePassword("user1", "pass1"))
    def1.addCallback(connected)
    #def1.addCallback(connectedAgain)

    #deferred = factory.getRootObject()
    #deffed.addCallback(connected)
    #deferred.addCallback(sender.phase360)
    reactor.run()

def connected(remote):
    print "got remote ref:", remote
    print "asking it to ignore pool"
    remote.callRemote("ignorePool")

    
def connectedAgain(perspective):
    print "got perspective ref:", perspective
    print "asking it to foo(12)"
    #perspective.callRemote("foo", 12)

def running(file_path, var, name, sleeptime):
    #transmitOne(file_path, port=1331,address='hddlab.hdd.lab')
    print 'Dialing on port...'
    print '..................................'
    server = xmlrpclib.ServerProxy("http://dashboard.hdd.lab:1332", allow_none=True)
    server.sendFileGroup(file_path, var)
    time.sleep(sleeptime)    
    #reactor.run()


def filetrans(file_path,type,teatime):
    transmitOne(file_path, port=1331,address='hddlab.hdd.lab')
    time.sleep(teatime)
    reactor.run()    

    
def check_in(test_type, data, name, sleeptime):
    sender = Sender(test_type, data, analysis=None)
    print '........got data..............'
    factory = pb.PBClientFactory()
    reactor.connectTCP("dashboard.hdd.lab", 1331, factory)
    deferred = factory.getRootObject()
    deferred.addCallback(sender.add_inquiry)
    time.sleep(sleeptime) 
    reactor.run()
    
def checkin(test_type, data):
    sender = Sender(test_type, data, analysis=None)
    print '........got data..............'
    factory = pb.PBClientFactory()
    reactor.connectTCP("dashboard.hdd.lab", 1331, factory)
    deferred = factory.getRootObject()
    deferred.addCallback(sender.add_inquiry)
    reactor.run()
      
def mode_pages(test_type, data):
    data = [data, test_type]
    sender = Sender(test_type, data, analysis=None)
    print '........got data..............'
    factory = pb.PBClientFactory()
    reactor.connectTCP("Dashboard.hdd.lab", 1331, factory)
    deferred = factory.getRootObject()
    deferred.addCallback(sender.add_modepages)
    reactor.run()
    
        

def check_systems(test_type):
    sender = Sender(test_type, 'data')
    factory = pb.PBClientFactory()
    reactor.connectTCP("Dashboard.hdd.lab", 1331, factory)
    deferred = factory.getRootObject()
    deferred.addCallback(sender.add_systemdata)  
    reactor.run()
      
def run_performance(scripts):
    factory = pb.PBClientFactory()
    reactor.connectTCP("dashboard.hdd.lab", 1331, factory)
    deferred = factory.getRootObject()
    data = data_builder('Performance', scripts)
    device =  data[0]
    output = data[1] #the csv output file for IOMeter Performance Testing
    report = data[2] #the output file name for Metrics Analysis Tool
    output_file = paths + output   

    analyze = paths + output

    analysis_data = [analyze, report]
    sender = Sender('Performance', device, analysis_data)    

    ret = iometer_thread(scripts, output_file)
    if ret:
    	return ret
    if ret == 0:
	thread.start_new_thread(data_entry, (device, analysis_data, "thread-1", 100)) 
	#thread.start_new_thread(running, (analyze, report,"thread-2", 10)) 
    reactor.run()
    
def iometer_thread(scripts,output):
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
    return ret
    #time.sleep(naptime)
    

def data_entry(device, analysis_data, name, sleeptime):
    factory = pb.PBClientFactory()
    reactor.connectTCP("dashboard.hdd.lab", 1331, factory)
    deferred = factory.getRootObject()
    #ff = open(output, 'r')
    #device['Raw'] = [repr(ff)]
    #sender = Sender('Performance', device)
    sender = Sender('Performance', device, analysis_data)

    #ff.close()
    deferred.addCallback(sender.add_resultdata_batch)
    deferred.addCallback(sender.add_testdata_batch)
    deferred.addCallback(sender.add_runanalysis)
    time.sleep(sleeptime)
    reactor.run()
    


def data_builder(test, scripts):
    import os
    serial=[]
    drives = []
    NAME = os.environ['COMPUTERNAME']

    c = wmi.WMI()
    for disk in c.Win32_DiskDrive():
	
	if 'H700' not in disk.Model.split(' '):
	    serial.append(disk.SerialNumber)
	    drives.append(disk)
    disk = drives[0]
    location = disk.DeviceID.replace("\\\\.\\",'')
    size = int(disk.Size)
    if size > 10**12:
	size_str = str(size / 10**12) + "TB"
    else:
	size_str = str(size / 10**9) + "GB"
    if disk.MediaType == 'Fixed hard drive media':
	media = 'HDD'
    else:
	media = 'SSD'
		
    if disk.InterfaceType == 'SCSI':
	pd_type = 'SAS'
    else:
	pd_type = 'SATA'
		
    fw_version = disk.FirmwareRevision
    vendor = disk.Model.split(' ')[0]
    model = disk.Model.split(' ')[1]
    hdd_name = model_map.get(model)
    if hdd_name is None:
	hdd_name = model
    hdd_name = re.sub("\s+", "_", hdd_name)
    pd_type = disk.InterfaceType
    speed = disk.Capabilities[0]
    date = time.strftime("%Y-%m-%d-%H%M%S")
    sys_name = disk.SystemName		
		
    script = scripts[0].split("\\")[-1:][0]
    output = NAME + '_' + vendor + '_' + model + '_' + size_str + '_' + date     
    report = NAME + '_' + vendor + '_' + model + '_' + size_str + '_' + date + '.xlsx'
    output = output + '_results.csv'    
    rawdata = paths + output
    reports = dir_name + report
	    
    data = {'MemoryType': media, 'CodeName':hdd_name, 'Manufacturer':vendor, 'InterfaceType': pd_type, 'WindowsLocation':location,
	'InterfaceSpeed': speed,'Capacity':size_str,'System':sys_name,'RawData':rawdata,'Reports':reports, 'Script':script,'Controller': 'PERC-H200A',
	'ModelNumber':model,'SerialNumber':serial,'Firmware':fw_version, 'Timestamp':date, 'TestName': test}
    return data, output, reports


