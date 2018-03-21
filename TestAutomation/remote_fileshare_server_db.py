#!/usr/bin/env python


from binascii import crc32
from optparse import OptionParser
import os, os.path, sys, json, pprint, datetime
import string, time
import adodbapi


 
from twisted.protocols import basic
from twisted.application import service, internet
from twisted.internet import reactor, protocol

from twisted.python import components
from twisted.internet.protocol import ServerFactory
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import FileSender
from twisted.internet.defer import Deferred
from twisted.spread import pb
from zope.interface import Interface, implements
#import remotequeue_client
#from analysistools import analysis





sep = os.sep

paths = '%s%sPerformance_Results%s' % (os.environ['HOMEDRIVE'], sep,sep)
 
pp = pprint.PrettyPrinter(indent=1)
 
class TransferCancelled(Exception):
    """ Exception for a user cancelling a transfer """
    pass
	
class FileIOProtocol(basic.LineReceiver):
    """ File Receiver """
 
    class Session(object):
        """ Session object, just a demo """
        def is_invalid(self):
            return False
 
        def is_stale(self):
            return False
 
    class Status(object):
        """ Status object.. just a demo """
        def update(self, **kargs):
            """ """
            print '-'*80
            pp.pprint(kargs)
 
    def __init__(self):
        """ """
        self.session = FileIOProtocol.Session()
        self.status = FileIOProtocol.Status()
        self.outfile = None
        self.remain = 0
        self.crc = 0
 
    def lineReceived(self, line):
        """ """
        print ' ~ lineReceived:\n\t', line
        self.instruction = json.loads(line)
        self.instruction.update(dict(client=self.transport.getPeer().host))
	self.file_name = self.instruction['original_file_path']
        self.size = self.instruction['file_size']
        self.original_fname = self.instruction.get('original_file_path',
                                                   'not given by client')
        print self.file_name
        print '-------'
        #
        # Never happens.. just a demo.
        if self.session.is_invalid():
            print 'FileIOProtocol:lineReceived Invalid session'
            self.transport.loseConnection()
            return
 
        # Never happens.. just a demo.
        if self.session.is_stale():
            print 'FileIOProtocol:lineReceived Stale session'
            self.transport.loseConnection()
            return
 
        # Create the upload directory if not already present
        #uploaddir = file_path
	uploaddir = paths
        print " * Using upload dir:",uploaddir
        if not os.path.isdir(uploaddir):
            os.makedirs(uploaddir)
	#print self.original_fname.keys()
	original_file = self.file_name.split("\\")[-1:][0]
        self.outfilename = os.path.join(uploaddir, original_file)
 
        print ' * Receiving into file@',self.outfilename
        try:
            self.outfile = open(self.outfilename,'wb')
        except Exception, value:
            print ' ! Unable to open file', self.outfilename, value
            self.transport.loseConnection()
            return
 
        self.remain = int(self.size)
        print ' & Entering raw mode.',self.outfile, self.remain
        self.setRawMode()
 
    def rawDataReceived(self, data):
        """ """
        if self.remain%10000==0:
            print '   & ',self.remain,'/',self.size
        self.remain -= len(data)
 
        self.crc = crc32(data, self.crc)
        self.outfile.write(data)
 
    def connectionMade(self):
        """ """
        basic.LineReceiver.connectionMade(self)
        print '\n + a connection was made'
        print ' * ',self.transport.getPeer()
 
    def connectionLost(self, reason):
        """ """
        basic.LineReceiver.connectionLost(self, reason)
        print ' - connectionLost'
        if self.outfile:
            self.outfile.close()
        # Problem uploading - tmpfile will be discarded
        if self.remain != 0:
            print str(self.remain) + ')!=0'
            remove_base = '--> removing tmpfile@'
            if self.remain<0:
                reason = ' .. file moved too much'
            if self.remain>0:
                reason = ' .. file moved too little'
            print remove_base + self.outfilename + reason
            os.remove(self.outfilename)
 
        # Success uploading - tmpfile will be saved to disk.
        else:
            print '\n--> finished saving upload@' + self.outfilename
            client = self.instruction.get('client', 'anonymous')
            self.status.update( crc           = self.crc,
                                file_size     = self.size,
                                client        = client,
                                new_file      = self.outfilename,
                                original_file = self.original_fname,
                                file_metadata = fileinfo(self.outfilename),
                                upload_time   = datetime.datetime.now() )
            
            
            
  
 
class FileIOFactory(ServerFactory):
    """ file receiver factory """
    protocol = FileIOProtocol
 
    def __init__(self, db, options={}):
        """ """
        self.db = db
        self.options = options
	
	
            
def fileinfo(fname):
    """ when "file" tool is available, return it's output on "fname" """
    #and \    os.popen('file "'+fname+'"').read().strip().split(':')[1]
    print os.popen('file "'+fname+'"').read().strip().split(':')
    return ( os.system('file 2> /dev/null')!=0 and \
             os.path.exists(fname) )

 

 
if __name__=='__main__':
    port = 1331
    fileio = FileIOFactory({})
    reactor.listenTCP(port, fileio)
    print 'Listening on port',port,'..'
    reactor.run()
 
   

	