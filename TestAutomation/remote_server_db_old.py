#!/usr/bin/env python


__author__ = "Willie Martin"
__version__ = "$Revision: 1.5 $"

import binascii
from binascii import crc32
from optparse import OptionParser
import os, os.path, sys, json, pprint, datetime
import string, time, datetime
from datetime import datetime
import adodbapi

#from AutoPerfAnalysis3 import analysis
from AutoPerfAnalysis import perf_d2d
import shelve

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

from twisted.enterprise import adbapi

import wmi

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

paths = '%s%sResults%s' % (os.environ['USERPROFILE'], sep,sep)
paths = '%s%shddlab%sFileShare%sPerformance_Results%s' % (sep,sep,sep,sep,sep)
dir_name = '%s%shddlab%sFileShare%sPerformance_Results%sMetrics_outputs%s' % (sep,sep, sep,sep,sep, sep)  

 
pp = pprint.PrettyPrinter(indent=1)    
            
            
keys = ['VenderID', 'ProductID', 'FirmwareRevisionLevel', 'ProductSerialNumber', 'TargetDeviceName', 'TargetPortIdentifier1',
            'TargetPortIdentifier2', 'FormFactorWidth', 'FormFactorHeight', 'DeviceID', 'ServoCodeLevel', 'PCBASerialNumber', 'PCBAPartNumber',
            'DiskMediaVendor', 'MotorSerialNumber', 'FlexCircuitAssemblySerialNumber', 'HeadVendor', 'HDCRevision', 'ActuatorSerialNumber',
            'HeadDiskAssembly', 'YearofManufacture', 'WeekofManufacture', 'DayofManufacture', 'LocationofManufacture', 'DellPPID', 'MediumRotationRate', 'Diff', 'SED']



code_name= { 'Vendor':'SEAGATE','SerialNumber':"ST3500620SS", 'MarketName' : "Seagate Moose SAS_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3750630SS", 'MarketName' : "Seagate Moose SAS_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST31000640SS" , 'MarketName' : "Seagate Moose SAS_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3146356SS" , 'MarketName' : "Seagate Hurricane_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3300656SS" , 'MarketName' : "Seagate Hurricane_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3450856SS" , 'MarketName' : "Seagate Hurricane_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3250310NS" , 'MarketName' : "Seagate Moose SATA_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3500320NS" , 'MarketName' : "Seagate Moose SATA_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3750330NS" , 'MarketName' : "Seagate Moose SATA_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST31000340NS" , 'MarketName' : "Seagate Moose SATA_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3400755SS" , 'MarketName' : "Seagate Timberland NS_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBA3073RC" , 'MarketName' : "Fujitsu Allegro 10LX_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBA3147RC" , 'MarketName' : "Fujitsu Allegro 10LX_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBA3300RC" , 'MarketName' : "Fujitsu Allegro 10LX_DUP",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD1602ABKS-1" , 'MarketName' : "WD Pinnacle (XL320 RE)",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD2502ABYS-1" , 'MarketName' : "WD Pinnacle (XL320 RE)",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD5002ABYS-1" , 'MarketName' : "WD Pinnacle (XL320 RE)",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD7502ABYS-1" , 'MarketName' : "WD Mars (XL333 RE)",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD1002FBYS-1" , 'MarketName' : "WD Mars (XL333 RE)",
    'Vendor':'FUJITSU','SerialNumber':"MHZ2080BK" , 'MarketName' : "Fujitsu Aries (A160-ED)",
    'Vendor':'FUJITSU','SerialNumber':"MHZ2160BK" , 'MarketName' : "Fujitsu Aries (A160-ED)",
    'Vendor':'FUJITSU','SerialNumber':"MHZ2250BK" , 'MarketName' : "Fujitsu Aries (A160-ED)",
    'Vendor':'SEAGATE','SerialNumber':"ST973452SS" , 'MarketName' : "Seagate Hornet_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST9146852SS" , 'MarketName' : "Seagate Hornet_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST9146752SS" , 'MarketName' : "Seagate Hornet_DUP, SED",
    'Vendor':'SEAGATE','SerialNumber':"ST9146803SS" , 'MarketName' : "Seagate Firefly_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST9300603SS" , 'MarketName' : "Seagate Firefly_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST9300503SS" , 'MarketName' : "Seagate Firefly_DUP, SED",
    'Vendor':'SEAGATE','SerialNumber':"ST9500430SS" , 'MarketName' : "Seagate Dragonfly_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST9500431SS" , 'MarketName' : "Seagate Dragonfly_DUP, SED",
    'Vendor':'SEAGATE','SerialNumber':"ST3300657SS" , 'MarketName' : "Seagate Eagle_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3450857SS" , 'MarketName' : "Seagate Eagle_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3600057SS" , 'MarketName' : "Seagate Eagle_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3450757SS" , 'MarketName' : "Seagate Eagle_DUP, SED",
    'Vendor':'SEAGATE','SerialNumber':"ST3600957SS" , 'MarketName' : "Seagate Eagle_DUP, SED",
    'Vendor':'SEAGATE','SerialNumber':"ST3600002SS" , 'MarketName' : "Seagate Eagle RP_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3500414SS" , 'MarketName' : "Seagate Muskie_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST31000424SS" , 'MarketName' : "Seagate Muskie_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST32000444SS" , 'MarketName' : "Seagate Muskie_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST31000425SS" , 'MarketName' : "Seagate Muskie_DUP, SED",
    'Vendor':'SEAGATE','SerialNumber':"ST32000445SS" , 'MarketName' : "Seagate Muskie_DUP, SED",
    'Vendor':'SEAGATE','SerialNumber':"ST9500530NS" , 'MarketName' : "Seagate Dragonfly ES_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3500514NS" , 'MarketName' : "Seagate Muskie ES_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST31000524NS" , 'MarketName' : "Seagate Muskie ES_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST32000544NS" , 'MarketName' : "Seagate Muskie ES_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBD2147RC" , 'MarketName' : "Fujitsu Allegro 11SE_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBD2300RC" , 'MarketName' : "Fujitsu Allegro 11SE_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBE2073RC" , 'MarketName' : "Fujitsu Allegro 11SX_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBE2147RC" , 'MarketName' : "Fujitsu Allegro 11SX_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUC103014CSS600" , 'MarketName' : "Hitachi Cobra C_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUC103030CSS600" , 'MarketName' : "Hitachi Cobra C_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUC151473CSS600" , 'MarketName' : "Hitachi King Cobra C_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUC151414CSS600" , 'MarketName' : "Hitachi King Cobra C_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUS156030VLS600" , 'MarketName' : "Hitachi Viper C_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUS156045VLS600" , 'MarketName' : "Hitachi Viper C_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUS156060VLS600" , 'MarketName' : "Hitachi Viper C_DUP",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD1460BKFG-1" , 'MarketName' : "WD Rigel (SL150)_DUP",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD3000BKFG-1" , 'MarketName' : "WD Rigel (SL150)_DUP",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD1460BKFG-1" , 'MarketName' : "WD Rigel (SL150) 6Gb_DUP",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD3000BKFG-1" , 'MarketName' : "WD Rigel (SL150) 6Gb_DUP",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD3000BKHG-1" , 'MarketName' : "WD Vega_DUP",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD6000BKHG-1" , 'MarketName' : "WD Vega_DUP",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD2000FYYG-1" , 'MarketName' : "WD Bach_DUP",
    'Vendor':'SAMSUNG','SerialNumber':"HE161HJ" , 'MarketName' : "Samsung F1R",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD2002FYPS-1" , 'MarketName' : "WD Sparta ES_DUP",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD2003FYYS-1" , 'MarketName' : "WD Mantis ES",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD1003FBYX-1" , 'MarketName' : "WD Vulcan_DUP_1TB",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD2503ABYX-1" , 'MarketName' : "WD Summit_DUP_250GB",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD5003ABYX-1" , 'MarketName' : "WD Summit_DUP_500GB",
    'Vendor':'HITACHI','SerialNumber':"HUA722020ALA330" , 'MarketName' : "Hitachi Jupiter K ES_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST9600204SS" , 'MarketName' : "Seagate Firestorm_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST9600104SS" , 'MarketName' : "Seagate Firestorm_DUP, SED",
    'Vendor':'TOSHIBA','SerialNumber':"MBF2300RC" , 'MarketName' : "Toshiba Allegro 12SE_DUP",
    'Vendor':'TOSHIBA','SerialNumber':"MBF2600RC" , 'MarketName' : "Toshiba Allegro 12SE_DUP",
    'Vendor':'SAMSUNG','SerialNumber':"HE253GJ" , 'MarketName' : "Samsung F3R ES",
    'Vendor':'SAMSUNG','SerialNumber':"HE502HJ" , 'MarketName' : "Samsung F3R ES",
    'Vendor':'SAMSUNG','SerialNumber':"HE103SJ" , 'MarketName' : "Samsung F3R ES",
    'Vendor':'HITACHI','SerialNumber':"HUC106030CSS600" , 'MarketName' : "Hitachi Cobra D_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUC106060CSS600" , 'MarketName' : "Hitachi Cobra D_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST936751SS" , 'MarketName' : "Seagate Maverick_non-DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST973451SS" , 'MarketName' : "Seagate Maverick_non-DUP",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD1000FYPS-1" , 'MarketName' : "WD Hulk (GP250RE2)",
    'Vendor':'HITACHI','SerialNumber':"HUS154530VLS300" , 'MarketName' : "Hitachi Viper B+_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUS154545VLS300" , 'MarketName' : "Hitachi Viper B+_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUS153073VLS300" , 'MarketName' : "Hitachi Viper B_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUS153014VLS300" , 'MarketName' : "Hitachi Viper B_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUS153030VLS300" , 'MarketName' : "Hitachi Viper B_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUC101473CSS300" , 'MarketName' : "Hitachi Cobra B_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUC101414CSS300" , 'MarketName' : "Hitachi Cobra B_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUA721050KLA330" , 'MarketName' : "Hitachi Gemini K",
    'Vendor':'HITACHI','SerialNumber':"HUA721075KLA330" , 'MarketName' : "Hitachi Gemini K",
    'Vendor':'HITACHI','SerialNumber':"HUA721010KLA330" , 'MarketName' : "Hitachi Gemini K",
    'Vendor':'SEAGATE','SerialNumber':"ST973452SS" , 'MarketName' : "Seagate Hornet_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST9146852SS" , 'MarketName' : "Seagate Hornet_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST9146803SS-H" , 'MarketName' : "Seagate Firefly_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST9146803SS" , 'MarketName' : "Seagate Firefly_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST9300603SS" , 'MarketName' : "Seagate Firefly_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST9500430SS" , 'MarketName' : "Seagate Dragonfly_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3300657SS" , 'MarketName' : "Seagate Eagle_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3450857SS" , 'MarketName' : "Seagate Eagle_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3600057SS" , 'MarketName' : "Seagate Eagle_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3600002SS" , 'MarketName' : "Seagate Eagle RP_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBD2147RC" , 'MarketName' : "Fujitsu Allegro 11SE_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBD2147RC" , 'MarketName' : "Fujitsu Allegro 11SE_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBD2300RC" , 'MarketName' : "Fujitsu Allegro 11SE_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBE2073RC" , 'MarketName' : "Fujitsu Allegro 11SX_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBE2147RC" , 'MarketName' : "Fujitsu Allegro 11SX_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUC103014CSS600" , 'MarketName' : "Hitachi Cobra C_DUP",
    'Vendor':'HITACHI','SerialNumber':"HUC103030CSS600" , 'MarketName' : "Hitachi Cobra C_DUP",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WD5000YS-18MPB1" , 'MarketName' : "WD Zeus ES",
    'Vendor':'HITACHI','SerialNumber':"HDS725050KLA360" , 'MarketName' : "Hitachi Kurofune II",
    'Vendor':'FUJITSU','SerialNumber':"MAX3036RC" , 'MarketName' : "Fujitsu Allegro 9LX",
    'Vendor':'FUJITSU','SerialNumber':"MAX3073RC" , 'MarketName' : "Fujitsu Allegro 9LX",
    'Vendor':'FUJITSU','SerialNumber':"MAX3147RC" , 'MarketName' : "Fujitsu Allegro 9LX",
    'Vendor':'HITACHI','SerialNumber':"HUS151436VLS300" , 'MarketName' : "Hitachi Viper A'",
    'Vendor':'HITACHI','SerialNumber':"HUS151473VLS300" , 'MarketName' : "Hitachi Viper A'",
    'Vendor':'HITACHI','SerialNumber':"HUS151414VLS300" , 'MarketName' : "Hitachi Viper A'",
    'Vendor':'FUJITSU','SerialNumber':"MAY2036RC" , 'MarketName' : "Fujitsu Allegro 9SE+",
    'Vendor':'FUJITSU','SerialNumber':"MAY2073RC" , 'MarketName' : "Fujitsu Allegro 9SE+",
    'Vendor':'MAXTOR','SerialNumber':"ATLAS10K5-073SAS" , 'MarketName' : "Maxtor Genesis",
    'Vendor':'MAXTOR','SerialNumber':"ATLAS10K5-147SAS" , 'MarketName' : "Maxtor Genesis",
    'Vendor':'MAXTOR','SerialNumber':"ATLAS10K5-300SAS" , 'MarketName' : "Maxtor Genesis",
    'Vendor':'MAXTOR','SerialNumber':"ATLAS15K2-036SAS" , 'MarketName' : "Maxtor Blackbird ",
    'Vendor':'MAXTOR','SerialNumber':"ATLAS15K2-073SAS" , 'MarketName' : "Maxtor Blackbird ",
    'Vendor':'MAXTOR','SerialNumber':"ATLAS15K2-147SAS" , 'MarketName' : "Maxtor Blackbird ",
    'Vendor':'SEAGATE','SerialNumber':"ST336754SS" , 'MarketName' : "Seagate Cheetah 15K.4",
    'Vendor':'SEAGATE','SerialNumber':"ST373454SS" , 'MarketName' : "Seagate Cheetah 15K.4",
    'Vendor':'SEAGATE','SerialNumber':"ST3146854SS" , 'MarketName' : "Seagate Cheetah 15K.4",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WD800JD-75MSA3" , 'MarketName' : "WD Unicorn II",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WD1600JS-75NCB3" , 'MarketName' : "WD Hawk II",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WD2500JS-75NCB3" , 'MarketName' : "WD Hawk II",
    'Vendor':'SEAGATE','SerialNumber':"ST380819AS" , 'MarketName' : "Seagate Puma II",
    'Vendor':'SEAGATE','SerialNumber':"ST3160828AS" , 'MarketName' : "Seagate Puma II",
    'Vendor':'SEAGATE','SerialNumber':"ST3808110AS" , 'MarketName' : "Seagate Tonka II",
    'Vendor':'SEAGATE','SerialNumber':"ST3160812AS" , 'MarketName' : "Seagate Tonka II",
    'Vendor':'SEAGATE','SerialNumber':"ST3250824AS" , 'MarketName' : "Seagate Tonka Plus",
    'Vendor':'SEAGATE','SerialNumber':"ST936701SS" , 'MarketName' : "Seagate Savvio (10K.1)",
    'Vendor':'SEAGATE','SerialNumber':"ST973401SS" , 'MarketName' : "Seagate Savvio (10K.1)",
    'Vendor':'FUJITSU','SerialNumber':"MHV2040BS" , 'MarketName' : "Fujitsu Mercury 60-ED",
    'Vendor':'FUJITSU','SerialNumber':"MHW2040BS" , 'MarketName' : "Fujitsu Mercury 80-ED",
    'Vendor':'FUJITSU','SerialNumber':"MHW2080BS" , 'MarketName' : "Fujitsu Mercury 80-ED",
    'Vendor':'SEAGATE','SerialNumber':"ST3250620NS" , 'MarketName' : "Seagate Galaxy ES",
    'Vendor':'SEAGATE','SerialNumber':"ST3500630NS" , 'MarketName' : "Seagate Galaxy ES",
    'Vendor':'SEAGATE','SerialNumber':"ST3750640NS" , 'MarketName' : "Seagate Galaxy ES",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WD1600YS-18SHB2" , 'MarketName' : "WD Hawk ES",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WD2500YS-18SHB2" , 'MarketName' : "WD Hawk ES",
    'Vendor':'SEAGATE','SerialNumber':"ST373455SS" , 'MarketName' : "Seagate Timberland 15K non-DUP (Field only)",
    'Vendor':'SEAGATE','SerialNumber':"ST3146855SS" , 'MarketName' : "Seagate Timberland 15K non-DUP (Field only)",
    'Vendor':'SEAGATE','SerialNumber':"ST3300655SS" , 'MarketName' : "Seagate Timberland 15K non-DUP (Field only)",
    'Vendor':'SEAGATE','SerialNumber':"ST373355SS" , 'MarketName' : "Seagate Timberland T10 non-DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3146755SS" , 'MarketName' : "Seagate Timberland T10 non-DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3300555SS" , 'MarketName' : "Seagate Timberland T10 non-DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST973402SS" , 'MarketName' : "Seagate Firebird non-DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST9146802SS" , 'MarketName' : "Seagate Firebird non-DUP",
    'Vendor':'FUJITSU','SerialNumber':"MHW2080BK" , 'MarketName' : "Fujitsu Aries (A80-ED)",
    'Vendor':'FUJITSU','SerialNumber':"MHW2120BK" , 'MarketName' : "Fujitsu Aries (A80-ED)",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD800AAJS-1" , 'MarketName' : "WD Unicorn ES",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD5001ABYS-1" , 'MarketName' : "WD Tornado (XL160M)",
    'Vendor':'SEAGATE','SerialNumber':"ST373355SS" , 'MarketName' : "Seagate Timberland T10_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3146755SS" , 'MarketName' : "Seagate Timberland T10_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3300555SS" , 'MarketName' : "Seagate Timberland T10_DUP",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WD1601ABYS-18C0A0" , 'MarketName' : "WD Sequoia (XL160)",
    'Vendor':'SAMSUNG','SerialNumber':"HE160HJ" , 'MarketName' : "Samsung S166R",
    'Vendor':'SEAGATE','SerialNumber':"ST973402SS" , 'MarketName' : "Seagate Firebird_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST9146802SS" , 'MarketName' : "Seagate Firebird_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST373455SS" , 'MarketName' : "Seagate Timberland 15K_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3146855SS" , 'MarketName' : "Seagate Timberland 15K_DUP",
    'Vendor':'SEAGATE','SerialNumber':"ST3300655SS" , 'MarketName' : "Seagate Timberland 15K_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBB2073RC" , 'MarketName' : "Fujitsu Allegro 10SE_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBB2147RC" , 'MarketName' : "Fujitsu Allegro 10SE_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBC2036RC" , 'MarketName' : "Fujitsu Allegro 10SX_DUP",
    'Vendor':'FUJITSU','SerialNumber':"MBC2073RC" , 'MarketName' : "Fujitsu Allegro 10SX_DUP",
    'Vendor':'SAMSUNG','SerialNumber':"MCBQE25G5MPQ-0VAD3" , 'MarketName' : "Samsung RBX",
    'Vendor':'SAMSUNG','SerialNumber':"MCCOE50G5MPQ-0VAD3" , 'MarketName' : "Samsung RBX",
    'Vendor':'SAMSUNG','SerialNumber':"MCB4E50G5MXP-0VBD3" , 'MarketName' : "Samsung SS805",
    'Vendor':'SAMSUNG','SerialNumber':"MCCOE1HG5MXP-0VBD3" , 'MarketName' : "Samsung SS805",
    'Vendor':'PLIANT','SerialNumber':"LB150S" , 'MarketName' : "LB150S",
    'Vendor':'WESTERN DIGITAL','SerialNumber':"WDCWD6000BKHG-1" , 'MarketName' : "WD Vega_600GB",
    'Vendor':'HITACHI','SerialNumber':"HitachiHUA72202" , 'MarketName' : "Hitachi JupiterK",
    'Vendor':'SEAGATE','SerialNumber':"ST9300605SS" , 'MarketName' : "Compass ST9300605SS ",
    'Vendor':'SEAGATE','SerialNumber':"ST9900805SS" , 'MarketName' : "Compass ST9900805SS ",
    'Vendor':'SEAGATE','SerialNumber':"ST91000640NS" , 'MarketName' : "Airwalker ST91000640NS "}


#class MessageLogger:
#    """
#    An independent logger class (because separation of application
#    and protocol logic is a good thing).
#    """
#    def __init__(self, file):
#        self.file = file

#    def log(self, message):
#        """Write a message to the file."""
#        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
#        self.file.write('%s %s\n' % (timestamp, message))
#        self.file.flush()

#    def close(self):
#        self.file.close()

	    

class Receiver(pb.Root):
    """Contains Twisted Server methods for transferring Test System Client data.

    """
	
    
    
    def __init__(self):
	self.clients = []
	self.fpath=''
	self.outfile= None
	self.dataQueue={}
	self.drives = None
	self.device_data ={}
	 
	
        #self.logger = MessageLogger(open('log\server_logger.txt', "a"))
        #self.logger.log("Server is awake now at %s" % time.asctime(time.localtime(time.time())) )	
	#self.logger.close()
	
    
	
    def remote_shutdown(self):
        reactor.stop()      
        
	    
#    def remote_addDeviceData(self, data): No longer being used
#	
#	if self.device_data:
#	    drive_info = self.device_data
#	else:
#	    drive_info = data
#	
#	drive = Table('Device', metadata, autoload=True)
#	info ={}
#	s = drive.select((drive.columns.ModelNumber != drive_info['ModelNumber']) & (drive.columns.SerialNumber != drive_info['SerialNumber']) )
#	#s = drive.select(drive.columns.SerialNumber == drive_info['SerialNumber'])
#
#	val = connection.execute(s)
#	if val.rowcount == 0:
#	    for d in drive.columns:
#		col = str(d).split('.')[1]
#		if col in drive_info.keys():		
#		    info[col]=drive_info[col]	
#		if col == 'Shipping':		
#		    info[col]=0    
#		if col == 'SupportDUP':		
#		    info[col]=0
#	    try:
#		i = drive.insert()
#		i.execute(info)
#	    except Exception:
#		print 'Entry not made'
#		pass
#	else:
#	    driverev = Table('DeviceRev', metadata, autoload=True)
#	    info.clear()
#	    s = driverev.select((driverev.columns.ModelNumber == drive_info['ModelNumber']) & (driverev.columns.FWRev != drive_info['Firmware']))
#
#	    #s = driverev.select(driverev.columns.FWRev != drive_info['Firmware'])
#	    val = connection.execute(s)
#	    if val.rowcount:
#		try: 
#		    info = {'ModelNumber':drive_info['ModelNumber'], 'FWRev':drive_info['Firmware']}
#		    i = driverev.insert()
#		    i.execute(info)
#		except Exception:
#		    print 'Entry not made'
#		    pass
#	
#	
#	return 
	
    	
    def remote_addDeviceData_batch(self, data):		
	"""Passes device information to SQL Server Database       
        @type  remote_server_db: Twisted Server
        @param data: data is a dictionary containing keys and values that correspond to the db scheme for device
        @param device: device db table instance
        @param devicerev: devicerev db table instance
        """
	drive = Table('Device', metadata, autoload=True)
	driverev = Table('DeviceRev', metadata, autoload=True)
	for k in data.keys():
	    drive_info = data[k]
	   
	    info ={}
	    s = drive.select((drive.columns.ModelNumber != drive_info['ModelNumber']) & (drive.columns.SerialNumber != drive_info['SerialNumber']) )
	    val = connection.execute(s)
	    if val.rowcount==0:
		for d in drive.columns:
		    col = str(d).split('.')[1]
		    if col in drive_info.keys():		
			info[col]=str(drive_info[col])		    
			    
		    if col == 'Shipping':		
			info[col]=0    
		    if col == 'SupportDUP':		
			info[col]=0
		try:
		    i = drive.insert()
		    i.execute(info)
		    
		    #self.logger.log("[Data Entry  Successful] at %s" % time.asctime(time.localtime(time.time())) )	
		    #self.logger.log("Drive information has been entered into the database")
		    #self.logger.log("Dataset: %s" % drive_info )
		except Exception:
		    #self.logger.log("[Data Entry  Was Not Made] at %s" % time.asctime(time.localtime(time.time())) )	
		    #self.logger.log("Drive information already in the database")

		    pass
	    else:
		info.clear()
		s = driverev.select((driverev.columns.ModelNumber == str(drive_info['ModelNumber'])) & (driverev.columns.FWRev != str(drive_info['Firmware'])))	
		val = connection.execute(s)
		if val.rowcount:
		    try: 
			info = {'ModelNumber':str(drive_info['ModelNumber']), 'FWRev':str(drive_info['Firmware'])}
			i = driverev.insert()
			i.execute(info)
		    except Exception:
			#self.logger.log("[Data Entry  Was Not Made] at %s" % time.asctime(time.localtime(time.time())) )	
			#self.logger.log("Information already in the database")
			pass
		
	    
	 

	#self.logger.close()
	
   
#    def remote_addResultData(self, data): No longer being used	
#	drive_info = data		
#	info ={}	
#	result = Table('Result', metadata, autoload=True)	
#	info.clear()
#	for d in result.columns:
#	    col = str(d).split('.')[1]
#	    if col in drive_info.keys():
#		info[col]=drive_info[col]
#	   
#	try:
#	    i = result.insert()
#	    i.execute(info)
#	except Exception:
#	    print 'Entry not made'
#	    pass
#	
#	return 
    def remote_PostAnalysis(self, data):
	"""Passes device information to SQL Server Database       
        @type  remote_server_db: Twisted Server
        @param data: data is a dictionary containing keys and values that correspond to the db scheme for device
        @param device: device db table instance
        @param devicerev: devicerev db table instance
        """
	#filename = data[0].split("\\")[-1:][0]	
	#perf_d2d.run(group, dir_name, var)
	#analysis.run(data[0], dir_name, data[1])
	print data[1]
	perf_d2d.run(data[0], dir_name, data[1])
   
    def remote_addResultData_batch(self, data):		
	"""Passes device information to SQL Server Database       
        @type  remote_server_db: Twisted Server
        @param data: data is a dictionary containing keys and values that correspond to the db scheme for device
        @param device: device db table instance
        @param devicerev: devicerev db table instance
        """
	result = Table('Result', metadata, autoload=True)
	drive = Table('Device', metadata, autoload=True)
	metrics={}
	input={}
	info ={}
	drive_info = data
	f = open(drive_info['RawData'], 'r')
	rawd = f.read()
	f.close()
	info['Raw'] = repr(rawd)
	for d in result.columns:
	    col = str(d).split('.')[1]
	    if col in drive_info.keys():
		if col == 'Manufacturer':
		    info['Vendor'] = str(drive_info['Manufacturer']).strip()
		else:
		    info[col]=str(drive_info[col]).strip()
		    
		if col == 'Timestamp':
		    info[col] = time.strftime("%Y-%m-%d %H:%M:%S")
	
	dD = drive.select(drive.columns.ModelNumber == str(drive_info['ModelNumber']).strip())
	
	val = dD.execute()
	if val.rowcount == -1:
	    row = val.fetchone()
	    input = {'Timestamp':time.strftime("%Y-%m-%d %H:%M:%S"), 'RPM':row['RPM'],'Firmware':row['Firmware'],'FormFactor':row['FormFactor'], 'Capacity':str(row['Capacity']).strip(), 'PPID':row['DellPPID'] , 'MemoryType':str(row['MemoryType']).strip(), 'Vendor': str(row['Manufacturer']).strip() }
	    new_info = info.update(input)
	    try:
		#-------Create metrics analysis dictionary for data entry--
		m = metrics.update(info)
		del metrics['RawData']
		del info['Reports']
		metrics['TestName'] = 'D2D Metrics'
		#----------------------------------------------------------
		i = result.insert()	  
		i.execute(info)
		i.execute(metrics) #Enter metrics analysis data
		#self.logger.log("[Entry Made] at %s" % time.asctime(time.localtime(time.time())) )	

	    except Exception:
		#self.logger.log("[Data Entry  Was Not Made] at %s" % time.asctime(time.localtime(time.time())) )	
		#self.logger.log("Drive data not present to update data")
		pass

	
	else:
	    try:
		#-------Create metrics analysis dictionary for data entry--
		m = metrics.update(info)
		del metrics['RawData']
		del info['Reports']
		metrics['TestName'] = 'D2D Metrics'
		#----------------------------------------------------------
		i = result.insert()	  
		i.execute(info)	    
		#self.logger.log("[Entry Made without inquiry data] at %s" % time.asctime(time.localtime(time.time())) )	
		#self.logger.log("Drives have not been loaded correctly")
	    except:	    
		#self.logger.log("[Entry Not Made] at %s" % time.asctime(time.localtime(time.time())) )	
		pass
        
#    def remote_addTestData(self, data): No longer being used	
#	
#	test = Table('Test', metadata, autoload=True)	
#	drive_info = data
#		
#	info ={}
#    	s = test.select((test.columns.TestName == drive_info['TestName']) & (test.columns.Script == drive_info['Script'])  ) 
#	val = connection.execute(s)
#	if val.rowcount:
#	    
#	    testrev = Table('TestRev', metadata, autoload=True)    
#	    info.clear()        
#	    for d in testrev.columns:
#		col = str(d).split('.')[1]
#		if col in drive_info.keys():
#		    info[col]=drive_info[col]
#	    try:		    
#		i = testrev.insert()
#		i.execute(info)
#	    except Exception:
#		print 'Entry not made'
#		pass
#	    	   
#	else:
#	    info.clear()        
#	    for d in test.columns:
#		col = str(d).split('.')[1]
#		if col in drive_info.keys():        
#		    info[col]=drive_info[col]
#	    try:	    
#		i = test.insert()
#		i.execute(info)
#	    except Exception:
#		print 'Entry not made'
#		pass
#	
#	
#	
#	return 
#	
    
    
    def remote_addTestData_batch(self, data):		
	"""Passes device information to SQL Server Database       
        @type  remote_server_db: Twisted Server
        @param data: data is a dictionary containing keys and values that correspond to the db scheme for device
        @param device: device db table instance
        @param devicerev: devicerev db table instance
        """
	test = Table('Test', metadata, autoload=True)
	testrev = Table('TestRev', metadata, autoload=True)    
	drive_info = data
	info={}

    	s = test.select((test.columns.TestName == str(drive_info['TestName'])) & (test.columns.Script == str(drive_info['Script']))  ) 
	val = connection.execute(s)
	if val.rowcount==0:
	    
	    info.clear()        
	    for d in testrev.columns:
		col = str(d).split('.')[1]
		if col in drive_info.keys():
		    info[col]=str(drive_info[col])
		    
	    try:	    
		i = test.insert()
		i.execute(info)
		#self.logger.log("[Entry Made] at %s" % time.asctime(time.localtime(time.time())) )
	    except Exception:
		#self.logger.log("[Data Entry  Was Not Made] at %s" % time.asctime(time.localtime(time.time())) )	
		#self.logger.log("Drive information already in the database")
		pass
	    try:		    
		i = testrev.insert()
		i.execute(info)
		#self.logger.log("[Entry Made] at %s" % time.asctime(time.localtime(time.time())) )
	    except Exception:
		#self.logger.log("[Data Entry  Was Not Made] at %s" % time.asctime(time.localtime(time.time())) )	
		#self.logger.log("Drive information already in the database")
		pass
	else:
	    info.clear()        
	    for d in test.columns:
		col = str(d).split('.')[1]
		if col in drive_info.keys():        
		    info[col]=str(drive_info[col])
	    try:	    
		i = test.insert()
		i.execute(info)
		self.logger.log("[Entry Made] at %s" % time.asctime(time.localtime(time.time())) )
	    except Exception:
		#self.logger.log("[Data Entry  Was Not Made] at %s" % time.asctime(time.localtime(time.time())) )	
		#self.logger.log("Drive information already in the database")
		pass
	
	
	
    def remote_addInquiryData(self, data):	
	"""Passes device information to SQL Server Database       
        @type  remote_server_db: Twisted Server
        @param data: data is a dictionary containing keys and values that correspond to the db scheme for device
        @param device: device db table instance
        @param devicerev: devicerev db table instance
        """	
	inquiry_info = data
	inq = Table('DELLInqData', metadata, autoload=True)
	driverev = Table('DeviceRev', metadata, autoload=True)
	drive = Table('Device', metadata, autoload=True)

	info ={}
	s = inq.select(inq.columns.ProductSerialNumber == inquiry_info['ProductSerialNumber'])
	val = connection.execute(s)
	if val.rowcount == 0:
	    for d in inq.columns:
		col = str(d).split('.')[1]
		if col in inquiry_info.keys():		
		    info[col]=str(inquiry_info[col]).strip()
	    try:
		i = inq.insert()
		i.execute(info)
		#self.logger.log("[Entry Made] at %s" % time.asctime(time.localtime(time.time())) )
	    except Exception:
		print 'Entry not made'
		#self.logger.log("[Data Entry  Was Not Made] at %s" % time.asctime(time.localtime(time.time())) )	
		#self.logger.log("Drive information already in the database")
		pass
	#update section
		    
	input = {'FormFactor':inquiry_info['FormFactorWidth'], 'Height':inquiry_info['FormFactorHeight'], 'RPM':inquiry_info['MediumRotationRate']
		    , 'DellPPID':inquiry_info['DellPPID'] }
	
	d = drive.select(drive.columns.SerialNumber == inquiry_info['ProductSerialNumber'])
	val = d.execute()
	if val.rowcount == -1:
	    ss = drive.update(whereclause=((drive.columns.SerialNumber == inquiry_info['ProductSerialNumber'])), values=input )
	    ss.execute()
	

	return
    
    
	
    def remote_addModeData(self, data):	
	"""Passes device information to SQL Server Database       
        @type  remote_server_db: Twisted Server
        @param data: data is a dictionary containing keys and values that correspond to the db scheme for device
        @param device: device db table instance
        @param devicerev: devicerev db table instance
        """	
	inquiry_info = data
	inq = Table('DELLInqData', metadata, autoload=True)
	driverev = Table('DeviceRev', metadata, autoload=True)
	drive = Table('Device', metadata, autoload=True)

	info ={}
	s = inq.select(inq.columns.ProductSerialNumber == inquiry_info['ProductSerialNumber'])
	val = connection.execute(s)
	if val.rowcount == 0:
	    for d in inq.columns:
		col = str(d).split('.')[1]
		if col in inquiry_info.keys():		
		    info[col]=str(inquiry_info[col]).strip()
	    try:
		i = inq.insert()
		i.execute(info)
		#self.logger.log("[Entry Made] at %s" % time.asctime(time.localtime(time.time())) )
	    except Exception:
		#self.logger.log("[Data Entry  Was Not Made] at %s" % time.asctime(time.localtime(time.time())) )	
		#self.logger.log("Drive information already in the database")
		pass
    
    def remote_addServerData(self, data):	
	"""Passes device information to SQL Server Database       
        @type  remote_server_db: Twisted Server
        @param data: data is a dictionary containing keys and values that correspond to the db scheme for device
        @param device: device db table instance
        @param devicerev: devicerev db table instance
	
	Note: have not been put into use yet in the automatic registering on Servers
        """	
	system_info = data
	system = Table('Systems', metadata, autoload=True)
	info ={}
	s = system.select(system.columns.SystemName == system_info['SystemName'])
	val = connection.execute(s)
	if val.rowcount == 0:
	    for d in system.columns:
		col = str(d).split('.')[1]
		if col in system_info.keys():		
		    info[col]=system_info[col]
	    try:
		i = system.insert()
		i.execute(info)
		#self.logger.log("[Entry Made] at %s" % time.asctime(time.localtime(time.time())) )
	    except Exception:
		#self.logger.log("[Data Entry  Was Not Made] at %s" % time.asctime(time.localtime(time.time())) )	
		#self.logger.log("Drive information already in the database")
		pass
	
	return 
	
	
	
    
    def remote_LoadDellInqData(self, dell_files):	
	"""Passes device information to SQL Server Database       
        @type  remote_server_db: Twisted Server
        @param data: data is a dictionary containing keys and values that correspond to the db scheme for device
        @param device: device db table instance
        @param devicerev: devicerev db table instance
        """
	data={}
	self.check_in={}
	hex_keys = {}
	inquiry = []
	#filelist = os.listdir(paths)
	for d in dell_files.keys():
	#    dd = ''.join((paths,d))
	#    
	#    f = open(dd, 'r')
	#    s = f.readlines()
	#    for i in s:
	#	b = i.split(':')
	#	byte = b[0].replace('0x','')
	#	byte = int(byte, 16)
	#	value = b[1].split('  ')[1]
	#	hex_keys[byte] = value
	#	inquiry.extend(value.split(' '))
	#    f.close()	
	    inquiry = dell_files[d]	
	    
	    values = ''
	    #Get Vender ID
	    for x in range(4,12):                
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['VenderID'] = out.strip()  
	    #Get Product ID
	    values = ''
	    for x in range(12,27):                
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['ProductID'] = out.strip()
	    #Get Firmware Revision Level
	    values = ''
	    for x in range(28,32):                
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['FirmwareRevisionLevel'] = out.strip()
	    #Get 'Product Serial Number'
	    values = ''
	    for x in range(32,51):               
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['ProductSerialNumber'] = out.strip()
	    #Get 'Target Device Name'
	    values = ''
	    for x in range(52,60):                
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    #out = binascii.b2a_hqx(''.join(values.split( )))
	    data['TargetDeviceName'] = out.strip()
	    #Get 'Target Port Identifier 1'
	    values = ''
	    for x in range(60,68):                
		values = values + inquiry[x]
	    #out = binascii.unhexlify(''.join(values.split( )))
	    out = binascii.b2a_hqx(''.join(values.split( )))
	    data['TargetPortIdentifier1'] = out.strip()
	    #Get 'Target Port Identifier 2'
	    values = ''
	    for x in range(68,76):                 
		values = values + inquiry[x]
	    #out = binascii.unhexlify(''.join(values.split( )))
	    out = binascii.b2a_hqx(''.join(values.split( )))
	    data['TargetPortIdentifier2'] = out.strip()   
	    #Get 'Form Factor Width'
	    values = ''            
	    for x in range(76,80):                
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    try: 
		data['FormFactorWidth'] = int(out.strip()) * 0.001
	    except:
		print out
		data['FormFactorWidth'] = 0.0
		pass
	    #Get 'Form Factor Height'
	    values = ''
	    for x in range(80,85):               
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    try:
		data['FormFactorHeight'] = int(out.strip()) * 0.01
	    except:
		print out
		data['FormFactorHeight'] = 0.0
		pass
	    #Get 'Device ID'
	    values = ''
	    for x in range(84,92):               
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['DeviceID'] = out.strip()   
	    #Get 'Servo Code Level'
	    values = ''
	    for x in range(92,99):               
		#print inquiry[x]
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['ServoCodeLevel'] = out.strip()  
	    #Get 'PCBA Serial Number'
	    values = '' 
	    for x in range(100,116):               
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['PCBASerialNumber'] = out.strip() 
	    #Get 'PCBA Part Number'
	    values = ''
	    for x in range(117,131):               
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['PCBAPartNumber'] = out.strip() 
	    #Get 'Disk Media Vendor'
	    values = ''
	    for x in range(132,147):               
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['DiskMediaVendor'] = out.strip() 
	    #Get 'Motor Serial Number'
	    values = ''
	    for x in range(148,163):                
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['MotorSerialNumber'] = out.strip()
	    #Get 'Flex Circuit Assembly Serial Number'
	    values = ''
	    for x in range(164,180):               
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['FlexCircuitAssemblySerialNumber'] = out.strip() 
	    #Get 'Head Vendor'
	    values = ''
	    for x in range(180,196):               
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['HeadVendor'] = out.strip() 
	    #Get 'HDC Revision'
	    values = ''
	    for x in range(196,211):               
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['HDCRevision'] = out.strip() 
	    #Get 'Actuator Serial Number'
	    values = ''
	    for x in range(212,227):               
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['ActuatorSerialNumber'] = out.strip() 
	    #Get 'Head Disk Assembly'
	    values = ''
	    for x in range(228,244):               
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['HeadDiskAssembly'] = out.strip() 
	    #Get 'Year of Manufacture'
	    values = ''
	    for x in range(244,248):               
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['YearofManufacture'] = out.strip() 
	    #Get 'Week of Manufacture'
	    values = ''
	    for x in range(247,249):                
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['WeekofManufacture'] = out.strip()
	    #Get 'Day of Manufacture'
	    values = ''
	    for x in range(250,252):               
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['DayofManufacture'] = out.strip() 
	    #Get 'Location of Manufacture'
	    values = ''
	    for x in range(251,260):                
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['LocationofManufacture'] = out.strip()
	    #Get 'Dell PPID'
	    values = ''
	    for x in range(261,284):               
		values = values + inquiry[x]
	    out = binascii.unhexlify(''.join(values.split( )))
	    data['DellPPID'] = out.strip()
	    #Get 'Medium Rotation Rate'
	    values = ''
	    for x in range(284,286):               
		values = values + inquiry[x]            
	    out = int(values, 16)
	    data['MediumRotationRate'] = out
	    self.check_in[data['ProductSerialNumber']] = data
	    inquiry=[]
	    
	    self.remote_addInquiryData(data)
		
		
	   
    def remote_LoadModePages(self, drive):	
	"""Passes device information to SQL Server Database       
        @type  remote_server_db: Twisted Server
        @param data: data is a dictionary containing keys and values that correspond to the db scheme for device
        @param device: device db table instance
        @param devicerev: devicerev db table instance
        """
	self.checkin = shelve.open('CheckIn.db', flag='c', writeback=True)
	self.checkout = shelve.open('CheckOut.db', flag='c', writeback=True)
	dell_files = drive[0]
	type = drive[1]
	hex_keys = {}
	inquiry = []
	#filelist = os.listdir(path)
	for d in dell_files.keys():
	    inquiry = dell_files[d]
	    
		    
		
	    if '0x00' in d:
		VSM={}
		value =''.join(('0x', inquiry[6]))
		val = int(value, 16)
		VSM['UEAR'] = val
		#print 'VSM', VSM
		if type == 'CheckIn':
		    self.checkin[d] = VSM  #add the writing to the shelf db 
		elif type == 'CheckOut':
		    self.checkout[d] = VSM  #add the writing to the shelf db 
		
		
	    if '0x01' in d:
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
		#print 'RWER', RWER
		if type == 'CheckIn':
		    self.checkin[d] = RWER  #add the writing to the shelf db 
		elif type == 'CheckOut':
		    self.checkout[d] = RWER  #add the writing to the shelf db 
		
		
	    if '0x07' in d:
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
		#print 'VERM', VERM
		if type == 'CheckIn':
		    self.checkin[d] = VERM  #add the writing to the shelf db 
		elif type == 'CheckOut':
		    self.checkout[d] = VERM  #add the writing to the shelf db 
		
		
	    if '0x08' in d:
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
		#print 'CACHE', CACHE
		if type == 'CheckIn':
		    self.checkin[d] = CACHE  #add the writing to the shelf db 
		elif type == 'CheckOut':
		    self.checkout[d] = CACHE  #add the writing to the shelf db 
		
		
	    if '0x0A' in d:
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
		#print 'CMP', CMP	
		if type == 'CheckIn':
		    self.checkin[d] = CMP  #add the writing to the shelf db 
		elif type == 'CheckOut':
		    self.checkout[d] = CMP  #add the writing to the shelf db 
		
		
	    if '0x18' in d:
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
		#print 'PSLUM', PSLUM
		if type == 'CheckIn':
		    self.checkin[d] = PSLUM  #add the writing to the shelf db 
		elif type == 'CheckOut':
		    self.checkout[d] = PSLUM  #add the writing to the shelf db 
		
		
	    if '0x19' in d:
		PSPMP={}
		PM = {6:'CAWT', 5:'BAE',4:'RLM'}
		NLT = ''.join((inquiry[8],inquiry[9]))
		IRT = ''.join((inquiry[10],inquiry[11]))
		PSPMP['NLT'] = NLT
		PSPMP['IRT'] = IRT
		value =''.join(('0x', inquiry[6]))
		val = int(value, 16)
		#print inquiry
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
		#print 'PSPMP', PSPMP
		if type == 'CheckIn':
		    self.checkin[d] = PSPMP  #add the writing to the shelf db 
		elif type == 'CheckOut':
		    self.checkout[d] = PSPMP  #add the writing to the shelf db 
		
		
	    if '0x1C' in d:
		IECP={}
		IEC = {7:'PERF',6:'RESERVED2',5:'EBF',4:'EWASC',3:'DEXCPT',2:'TEST',1:'RESERVED1',0:'LOGERR'}
		IT = ''.join((inquiry[8],inquiry[11]))
		RC = ''.join((inquiry[12],inquiry[15]))
		IECP['IT'] = IT
		IECP['RC'] = RC
		value =''.join(('0x', inquiry[6]))
		val = int(value, 16)
		#print inquiry
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
		#print 'IECP', IECP
		if type == 'CheckIn':
		    self.checkin[d] = IECP  #add the writing to the shelf db 
		elif type == 'CheckOut':
		    self.checkout[d] = IECP  #add the writing to the shelf db 
		
	    
       
            inquiry=[]
	if type == 'CheckOut':
	    for k in self.checkout.keys():
		out = dict_diff(self.checkin, self.checkout)
		print 'drive mode page', k
		if out:
		    print 'Failed'
		else:
		    print 'Passed'
		#print dir(out)
		
	    
		#out2 = dict_diff(self.checkin[k], self.checkout[k])
		#print out2
	self.checkin.close()
	self.checkout.close()
	
	
def dict_diff(first, second):
    """ Return a dict of keys that differ with another config object.  If a value is
        not found in one fo the configs, it will be represented by KEYNOTFOUND.
        @param first:   Fist dictionary to diff.
        @param second:  Second dicationary to diff.
        @return diff:   Dict of Key => (first.val, second.val)
    """
    diff = {}
    sd1 = set(first)
    sd2 = set(second)
    #Keys missing in the second dict
    for key in sd1.difference(sd2):
        diff[key] = KEYNOTFOUNDIN2
    #Keys missing in the first dict
    for key in sd2.difference(sd1):
        diff[key] = KEYNOTFOUNDIN1
    #Check for differences
    for key in sd1.intersection(sd2):
        if first[key] != second[key]:
            diff[key] = (first[key], second[key])    
    return diff	
	

    
reactor.listenTCP(1331, pb.PBServerFactory(Receiver()))
print 'Server is running and waiting.....'
#reactor.listenTCP(8007, pb.PBServerFactory(Receiver()))
reactor.run()