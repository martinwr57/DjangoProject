#!/usr/bin/env python


from binascii import crc32
from optparse import OptionParser
import os, os.path, sys, json, pprint, datetime
import string, time, datetime
import adodbapi
from AutoPerfAnalysis2 import analysis

 
from twisted.protocols import basic
from twisted.application import service, internet
from twisted.internet import reactor, protocol

#LOGGING
from twisted.python import log

from twisted.python import components
from twisted.internet.protocol import ServerFactory
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import FileSender
from twisted.internet.defer import Deferred
from twisted.spread import pb
from zope.interface import interface, implements
from twisted.cred import checkers, portal

#import remotequeue_client
from twisted.enterprise import adbapi

from sqlalchemy import create_engine
from sqlalchemy import sql, schema, types, exc, pool
from sqlalchemy import Table, Integer, Sequence, Column, String, MetaData
from sqlalchemy.orm import sessionmaker



engine = create_engine('mssql+pyodbc://@DATABASE\SQLEXPRESS/RADatabase')

connection = engine.connect()

metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)

sep = os.sep

paths = '%s%sResults%s' % (os.environ['USERPROFILE'], sep,sep)
 
pp = pprint.PrettyPrinter(indent=1)    
            
            




class Receiver(pb.Root):
    
    greetings = 0
    connections = 0
    
    def __init__(self, name):
        self.name = name
	self.clients = []
	self.fpath=''
	self.outfile= None
	self.dataQueue={}
	self.drives = None

    def connect(self):
        self.connections += 1
    def disconnect(self):
        self.connections -= 1
    def attached(self, mind):
        self.clients.append(mind)
        print "attached to", mind
    def detached(self, mind):
        self.clients.remove(mind)
        print "detached from", mind
    def update(self, message):
        for c in self.clients:
            c.callRemote("update", message)

    def perspective_greet(self):
        self.greetings += 1
        return "<%d>hello %s" % (self.greetings, self.name)	
    
    def perspective_foo(self, arg):
        print "I am", self.name, "perspective_foo(",arg,") called on", self
	
    def remote_ignorePool(self):
        # stop watching the pool
        print "dropping pool"
        # gc causes __del__ causes 'decache' msg causes stoppedObserving
        self.pool = None
	
    def remote_shutdown(self):
        reactor.stop()
        
        
    def remote_create_table(self):  
	
	metadata = MetaData()
	Table('devicepages', metadata,
	    Column('id', Integer,
		Sequence('blah',100,10), primary_key=True),
	    Column('name', String(20))
	    ).create(engine)

    def remote_addMetricsResults(self, data, metrics):
	""""
	Call the analysis run function
	Then connect to the results table and enter metrics data
	"""
	print metrics
	info = {}
	drive_info = data
	result = Table('Result', metadata, autoload=True)	
	info.clear()
	for d in result.columns:
	    col = str(d).split('.')[1]
	    
	    if col in drive_info.keys():
		info[col]=drive_info[col]	
	i = result.insert()
	i.execute(info)
	print 'device....Metrics...Results added', drive_info['SerialNumber']
    
        print 'done'
	#closeshop.callRemote("closeup")"""
	
	
    def remote_addDeviceData(self, data):	
	#print 'nothing yet...'
	
	drive_info = data
		
	drive = Table('Device', metadata, autoload=True)
	info ={}
	#s = drive.select((drive.columns.ModelNumber != drive_info['ModelNumber']) & (drive.columns.SerialNumber != drive_info['SerialNumber']) )
	s = drive.select(drive.columns.SerialNumber == drive_info['SerialNumber'])

	val = connection.execute(s)
	if val.rowcount == 0:
	    for d in drive.columns:
		col = str(d).split('.')[1]
		if col in drive_info.keys():		
		    info[col]=drive_info[col]	
		if col == 'Shipping':		
		    info[col]=0    
		if col == 'SupportDUP':		
		    info[col]=0
	    try:
		i = drive.insert()
		i.execute(info)
		#print 'device....'
	    except Exception:
		print 'Entry not made'
		pass
	else:
	    driverev = Table('DeviceRev', metadata, autoload=True)
	    info.clear()
	    s = driverev.select((driverev.columns.ModelNumber == drive_info['ModelNumber']) & (driverev.columns.FWRev != drive_info['Firmware']))

	    #s = driverev.select(driverev.columns.FWRev != drive_info['Firmware'])
	    val = connection.execute(s)
	    if val.rowcount:
		try: 
		    info = {'ModelNumber':drive_info['ModelNumber'], 'FWRev':drive_info['Firmware']}
		    i = driverev.insert()
		    i.execute(info)
		    #print 'device.... revision'
		except Exception:
		    print 'Entry not made'
		    pass
	
	
	return 
	
   
    def remote_addResultData(self, data):	
	#print 'nothing yet...'
	
	drive_info = data
		
	info ={}
	
	result = Table('Result', metadata, autoload=True)	
	info.clear()
	for d in result.columns:
	    col = str(d).split('.')[1]
	    if col in drive_info.keys():
		info[col]=drive_info[col]
	   
	try:
	    i = result.insert()
	    i.execute(info)
	except Exception:
	    print 'Entry not made'
	    pass
	#print 'device....Test...Results', drive_info['ModelNumber']
	#print 'done'
	#closeshop.callRemote("closeup")
	
	
	return 
   
    def remote_addTestData(self, data):	
	print 'nothing yet...'
	
	test = Table('Test', metadata, autoload=True)
	
	drive_info = data
		
	info ={}
    	s = test.select((test.columns.TestName == drive_info['TestName']) & (test.columns.Script == drive_info['Script'])  ) 
	val = connection.execute(s)
	if val.rowcount:
	    
	    testrev = Table('TestRev', metadata, autoload=True)    
	    info.clear()        
	    for d in testrev.columns:
		col = str(d).split('.')[1]
		if col in drive_info.keys():
		    info[col]=drive_info[col]
	    try:		    
		i = testrev.insert()
		i.execute(info)
	    except Exception:
		print 'Entry not made'
		pass
	    #print 'Test....Revision'
	    
	   
	else:
	    info.clear()        
	    for d in test.columns:
		col = str(d).split('.')[1]
		if col in drive_info.keys():        
		    info[col]=drive_info[col]
	    try:	    
		i = test.insert()
		i.execute(info)
	    except Exception:
		print 'Entry not made'
		pass
	    #print 'Test....'
	
	
	#closeshop.callRemote("closeup")
	
	return 
	
	
	
    def remote_checkTables(self, pool):	
	print 'nothing yet...'
	drive_info = pool
	drive = Table('Device', metadata, autoload=True)
	print drive_info
	
	i = drive.insert()
	i.execute(drive_info)
	print 'done'
	
	
    def remote_checkDrives(self, pool):	
	print 'nothing yet...'

class CachingRealm:
    implements(portal.IRealm)

    def __init__(self, max=10):
        self.avatars = {}
        self.max = max

    def requestAvatar(self, avatarId, mind, *interfaces):
	assert pb.IPerspective in interfaces
        if pb.IPerspective not in interfaces: raise NotImplementedError
        if avatarId in self.avatars:
            p = self.avatars[avatarId]
	    p.attached(mind)

        else:
            p = self.avatars[avatarId] = Receiver(avatarId)
	    p.attached(mind)
        if p.connections >= self.max:
            raise ValueError("too many connections")
        p.connect()
        return pb.IPerspective, p, p.disconnect, lambda a=p:a.detached(mind)

	
#application = service.Application("copy_receiver")
p = portal.Portal(CachingRealm())
c = checkers.InMemoryUsernamePasswordDatabaseDontUse(user1="pass1",
                                                     user2="pass2")
p.registerChecker(c)
#reactor.listenTCP(1331, pb.PBServerFactory(Receiver()))
reactor.listenTCP(1331, pb.PBServerFactory(p))
print 'Server is running and waiting.....'
#reactor.listenTCP(8007, pb.PBServerFactory(Receiver()))
reactor.run()