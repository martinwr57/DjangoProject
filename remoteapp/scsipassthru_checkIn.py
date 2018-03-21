#!/usr/bin/env python
"""This is a GUI to support FAST a peripheral communication software"""
__author__ = "Bob Clausen"
__date__ = "2009-10-10"
__version__ = '1.0'

import os
import sys
import time
from ctypes import *
import re
import threading, thread
#from remote_client_db import transmitOne
#**************FAST API IMPORTS***************************
import fast
import fast.defs as defs
import fast.scsi.scsi as scsi
import fast.scsi.scsi_defs as sd
#**********************************************************

#************** MY IMPORTS *********************************
#import convertdata

#**********************************************************


#*********************GLOBAL DEFINES*************************
#DBUG = fast.log.DBUG
#INFO = fast.log.INFO
#WARN = fast.log.WARN
#CRIT = fast.log.CRIT

LOG_PREFIX = "BIG_BIRD"
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

# setup logging for output file and console
#fast.log.init(appver=__version__, logsvr = "file:%s" % "test.log", console=True)
#fast.log.write(DBUG, "fastinterface Version = %s" % __version__, LOG_PREFIX)

#*********** Load Inventory ***********************************
inventory = fast.Inventory()

def returnvpddata(pd, vpdcode):
        
        #Message Dialog Box
        
        scsi_params = scsi.SCSI_PARAMS()
        scsi_params.op_code = sd.SCSI_INQUIRY
        scsi_params.page_code = vpdcode
        ret, scsi_pt = pd.create_scsi_passthru(scsi_params)
        if ret:
            return "Failed to create scsipassthru"
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = False)
        if ret:
            return "Failed to send scispassthru"
        else:
            return scsi_pt

def returnparsevpddata(vpddata):
    
    return_data = ""
    
    peripheralqual = (vpddata.data[0] and 0xf0)
    peripheralqual >> 4
    peripheraltype = (vpddata.data[0] and 0x0f)
    pagecode = vpddata.data[01]
    return_data = "VPD DATA for page %02X\r\n" % pagecode
    #return_data += "PERIPHERALQUALIFIER: %02x\r\n" % peripheralqual
    #return_data += "PERIPHERAL DEVICE TYPE: %02x\r\n" % peripheraltype
    #***** Parse vpd page 80
    if(pagecode == 0x00):
        return_data += "Supported VPD pages VPD Page\r\n"
        pagelength = vpddata.data[3]
        return_data += "PAGE CODE: %02x\r\n" % pagecode
        return_data += "PAGE LENGTH: %02x\r\n" % vpddata.data[3]
        datalength = vpddata.data[3]
        supportedvpdpages = ""
        dataindex = 4
        while(dataindex < datalength + 4):
            supportedvpdpages += "%02x " % vpddata.data[dataindex]
            dataindex += 1
        
        return_data += "Supported VPD page list: %s\r\n" % supportedvpdpages
        
    if(pagecode >= 0x01 and pagecode <= 0x7f):
        return_data += "ASCII Information VPD Page\r\n"
        return_data += "PAGE CODE: %02x\r\n" % vpddata.data[1]
        pagelength = vpddata.data[3]
        return_data += "PAGE LENGTH: %02x\r\n" % vpddata.data[3]
        asciilength = vpddata.data[4]
        return_data += "ASCII LENGTH: %02x\r\n" % vpddata.data[4]
        dataindex = 5
        return_data += "ASCII Information\r\n"
        while(dataindex < asciilength):
            if ((vpddata.data[dataindex] >= 0x20) and (vpddata.data[dataindex] < 0x7F)):
                return_data += ("%c" % vpddata.data[dataindex])
            else:
                return_data += "."  # eliminate non-printable characters            
            #return_data_row += ("%02X " % vpddata.data[dataindex])
                
            dataindex += 1
        return_data += "\r\n"
        return_data += "Vendor Specific Information\r\n"
        while(dataindex < pagelength):
            return_data += ("%02X " % vpddata.data[dataindex])            
            dataindex += 1
        return_data += "\r\n"
            
    #***** Parse vpd page 80
    if(pagecode == 0x80):
        return_data += "Unit Serial Number VPD Page\r\n"
        serialnumber = ""
        pagelength = vpddata.data[3]
        return_data += "PAGE CODE: %02x\r\n" % pagecode
        return_data += "PAGE LENGTH: %02x\r\n" % vpddata.data[3]

        serialnumberbuf = vpddata.data[4:vpddata.data_length]

        pdserialnumber = convertBufToChar(serialnumberbuf)                    
        
        return_data += "PRODUCT SERIAL NUMBER: %s\r\n" % pdserialnumber
        

    if(pagecode == 0x81 or pagecode == 0x82):
        # This page is obsolete
        return_data += "This page is OBSOLETE\r\n"
    #***** Parse vpd page 83
    if(pagecode == 0x83):
        return_data += "Device Identification VPD Page\r\n"
        dataindex = 4
        pagelength = ((vpddata.data[2] << 8) | vpddata.data[3])
        return_data += "PAGE CODE: %02x\r\n" % vpddata.data[1]
        return_data += "PAGE LENGTH: %04x\r\n" % pagelength
        identcount = 1
        while(dataindex < pagelength):
            protocolidentifier = (vpddata.data[dataindex] & 0xf0)
            protocolidentifier = protocolidentifier >> 4
            codeset = vpddata.data[dataindex] & 0x0f
            dataindex += 1
            pivbit = (vpddata.data[dataindex] & 0x80) >> 7
            associationnibble = (vpddata.data[dataindex] & 0x30) >> 4
            
            return_data += "********** Identification Descriptor %d ******************\r\n" % identcount
            return_data += "DATAINDEX %d\r\n" % dataindex
            return_data += "PROTOCOL IDENTIFIER: %02x\r\n" % protocolidentifier
            if(associationnibble != 1 | associationnibble != 2 | pivbit == 0):
                return_data += "PROTOCOL IDENTIFIER: RESERVE"
            elif(protocolidentifier == 0):
                return_data += "PROTOCOL IDENTIFIER: Fibre Channel FCP-2"
            elif(protocolidentifier == 1):
                return_data += "PROTOCOL IDENTIFIER: Parallel SCSI SPI-5"
            elif(protocolidentifier == 2):
                return_data += "PROTOCOL IDENTIFIER: SSA SSA-S3P"
            elif(protocolidentifier == 3):
                return_data += "PROTOCOL IDENTIFIER: IEEE 1394 SBP-3"
            elif(protocolidentifier == 4):
                return_data += "PROTOCOL IDENTIFIER: SCSI Remote Direct Memory Access Protocol SRP"
            elif(protocolidentifier == 5):
                return_data += "PROTOCOL IDENTIFIER: Internet SCSI (iSCSI) iSCSI"
            elif(protocolidentifier == 6):
                return_data += "PROTOCOL IDENTIFIER: SAS Serial SCSI Protocol SAS"
            elif(protocolidentifier == 7):
                return_data += "PROTOCOL IDENTIFIER: Automation/Drive Interface Transport Protocol ADT"
            elif(protocolidentifier == 8):
                return_data += "PROTOCOL IDENTIFIER: AT Attachment Interface (ATA/ATAPI) ATA/ATAPI-7"
            elif(protocolidentifier >= 9 and protocolidentifier <= 0x0e):
                return_data += "PROTOCOL IDENTIFIER: Reserved"
            elif(protocolidentifier == 0xf):
                return_data += "PROTOCOL IDENTIFIER: No specific protocol"
            return_data += "\r\n"
            
            
            return_data += "CODE SET: %02x\r\n" % codeset
            if(codeset == 0):
                return_data += "CODE SET: Reserved"
            elif(codeset == 1):
                return_data += "CODE SET: The IDENTIFIER field shall contain binary values."
            elif(codeset == 2):
                return_data += "CODE SET: The IDENTIFIER field shall contain ASCII printable characters\r\n"
                return_data += "(i.e., code values 20h through 7Eh)"
            elif(codeset == 3):
                return_data += "CODE SET: The IDENTIFIER field shall contain ISO/IEC 10646-1 (UTF-8) codes"
            elif(codeset >= 4 and codeset <= 0xf):
                return_data += "CODE SET: Reserved"
            return_data += "\r\n"
        
            return_data += "PIV: %d\r\n" % pivbit
            return_data += "ASSOCIATION: %x\r\n" % associationnibble
            if(associationnibble == 0):
                return_data += "ASSOCIATION: The IDENTIFIER field is associated with the addressed logical unit."
            if(associationnibble == 1):
                return_data += "ASSOCIATION: The IDENTIFIER field is associated with the target port that received the request."
            if(associationnibble == 2):
                return_data += "ASSOCIATION: The IDENTIFIER field is associated with the SCSI target device that contains the addressed logical unit."
            if(associationnibble == 3):
                return_data += "ASSOCIATION: Reserved"
            return_data += "\r\n"   
            
            identifiertype = vpddata.data[dataindex] & 0x0f
            return_data += "IDENTIFIER TYPE: %02x\r\n" % identifiertype
            if(identifiertype == 0):
                return_data += "IDENTIFIER TYPE: Vendor specific"
            if(identifiertype == 1):
                return_data += "IDENTIFIER TYPE: T10 vendor ID based."
            if(identifiertype == 2):
                return_data += "IDENTIFIER TYPE: EUI-64 based"
            if(identifiertype == 3):
                return_data += "IDENTIFIER TYPE: NAA"
            if(identifiertype == 4):
                return_data += "IDENTIFIER TYPE: Relative target port identifier"
            if(identifiertype == 5):
                return_data += "IDENTIFIER TYPE: Target port group."
            if(identifiertype == 6):
                return_data += "IDENTIFIER TYPE:Logical unit group"
            if(identifiertype == 7):
                return_data += "IDENTIFIER TYPE: MD5 logical unit identifier"
            if(identifiertype == 8):
                return_data += "IDENTIFIER TYPE: SCSI name string"
            if(identifiertype >= 9 and identifiertype <= 0xf):
                return_data += "IDENTIFIER TYPE: Reserved"
            return_data += "\r\n"
            dataindex += 2
            identifierlength = vpddata.data[dataindex]
            return_data += "IDENTIFIER LENGTH: %02x\r\n" % identifierlength
            dataindex += 1
            if(identifiertype == 0):
                return_data += "IDENTIFIER FIELD IS VENDOR SPECIFIC\r\n"
            if(identifiertype == 1):
                identindex = 0
                gett10vendor = ""
                return_data += "IDENTIFIER FIELD is T10 Vendor ID based\r\n"
                gett10vendor = vpddata.data[dataindex: 8]
                return_data += "IDENTIFIER FIELD: %s\r\n" % gett10vendor
                return_data += "IDENTIFIER FIELD is T10 Vendor ID based\r\n"
                gett10vendor = vpddata.data[dataindex: 8]
                    
                return_data += "IDENTIFIER FIELD: %s\r\n" % gett10vendor
                
            if(identifiertype == 3):
                naafield = (vpddata.data[dataindex] & 0xf0 ) >> 4
                return_data += "NAA: %02x\r\n" % naafield
                if(naafield == 2):
                    return_data += "NAA: IEEE Extended\r\n"
                if(naafield == 5):
                    return_data += "NAA: IEEE Registered\r\n"
                    ieecoid = "%01x%02x%02x%01x" % ((vpddata.data[dataindex] & 0x0f ), \
                                vpddata.data[dataindex + 1],  vpddata.data[dataindex + 2], \
                                (vpddata.data[dataindex + 3] & 0xf0))
                    
                    return_data += "IEEE COMPANY_ID: %s\r\n" % ieecoid
                    dataindex += 3
                    maxloop = dataindex + 4
                    vendorspecificidentifier = ""
                    while(dataindex <= maxloop):
                        if(vendorspecificidentifier == ""):
                            vendorspecificidentifier += "%01x" % (vpddata.data[dataindex] & 0x0f)
                        else:
                            vendorspecificidentifier += "%02x" % vpddata.data[dataindex]
                        dataindex += 1
                    
                    return_data += "VENDOR SPECIFIC IDENTIFIER: %s\r\n" % vendorspecificidentifier
                    
                if(naafield == 6):
                    return_data += "NAA: IEEE Registered Extended"
                if(naafield == 3 or naafield == 4 or naafield >= 7 and naafield <= 0xf):
                    return_data += "NAA: Reserved"
            if(identifiertype == 4):
                #first two bytes obsolete
                dataindex +=2
                relativetargetportid = ""
                relativetargetportid += "%02x%02x" % (vpddata.data[dataindex], vpddata.data[dataindex + 1])
                return_data += "RELATIVE TARGET PORT IDENTIFIER: %s " % relativetargetportid
                if(int(relativetargetportid, 16) == 0):
                    return_data += "Reserved"
                if(int(relativetargetportid, 16) == 1):
                    return_data += "Relative port 1, historically known as port A"
                if(int(relativetargetportid, 16) == 2):
                    return_data += "Relative port 2, historically known as port B"
                if(int(relativetargetportid, 16) >= 3 and int(relativetargetportid, 16) <= 0xffff):
                    return_data += "Relative port %x" % int(relativetargetportid, 16)
                dataindex += 2
                return_data += "\r\n"
            if(identifiertype == 8):
                indexcount = dataindex + identifierlength
                namestring = ""
                while(dataindex < indexcount-1):
                    if ((vpddata.data[dataindex] >= 0x20) and (vpddata.data[dataindex] < 0x7F)):
                        namestring += ("%c" % vpddata.data[dataindex])
                    else:
                        namestring += "."  # eliminate non-printable characters            
                    dataindex += 1
                return_data += "SCSI NAME STRING %s\r\n" % namestring
            return_data += "DATAINDEX %d\r\n" % dataindex
            identcount += 1
    
    # vpd page 86
    if(pagecode == 0x86):
        dataindex = 1
        return_data += "Extended INQUIRY Data VPD Page\r\n"
        return_data += "PAGE CODE: %02x\r\n" % vpddata.data[dataindex]
        dataindex = 3
        pagelength = vpddata.data[dataindex]
        return_data += "PAGE LENGTH: %02x\r\n" % pagelength
        dataindex = 4
        rtobit = (vpddata.data[dataindex] & 0x8) >> 3
        return_data += "RTO: %01x\r\n" % rtobit
        if(rtobit == 0):
            return_data += "Logical unit does not support application client ownership of the LOGICAL BLOCK REFERENCE TAG field\r\n"
        if(rtobit == 1):
            return_data += "Logical unit supports application client ownership of the LOGICAL BLOCK REFERENCE TAG field\r\n"
        grdchkbit = (vpddata.data[dataindex] & 0x4) >> 2
        return_data += "GRD_CHK: %01x\r\n" % grdchkbit
        if(grdchkbit == 0):
            return_data += "Device server does not check the LOGICAL BLOCK GUARD field\r\n"
        if(grdchkbit == 1):
            return_data += "Device server checks the LOGICAL BLOCK GUARD field\r\n"
        appchkbit = (vpddata.data[dataindex] & 0x2) >> 1
        return_data += "APP_CHK: %01x\r\n" % appchkbit
        if(appchkbit == 0):
            return_data += "Device server does not check the LOGICAL BLOCK APPLICATION TAG field\r\n"
        if(appchkbit == 1):
            return_data += "Device server checks the LOGICAL BLOCK APPLICATION TAG field\r\n"
        refchkbit = (vpddata.data[dataindex] & 0x1)
        return_data += "REF_CHK: %01x\r\n" % refchkbit
        if(refchkbit == 0):
            return_data += "Device server does not check the LOGICAL BLOCK REFERENCE TAG field\r\n"
        if(refchkbit == 1):
            return_data += "Device server checks the LOGICAL BLOCK REFERENCE TAG field\r\n"
        dataindex += 1
        groupsupbit = (vpddata.data[dataindex] & 0x10) >> 4
        return_data += "GROUP_SUP: %01x\r\n" % groupsupbit
        if(groupsupbit == 0):
            return_data += "Grouping function is not supported by the device server\r\n"
        if(groupsupbit == 1):
            return_data += "Grouping function is supported by the device server\r\n"
        priorsupbit = (vpddata.data[dataindex] & 0x8) >> 3
        return_data += "PRIOR_SUP: %01x\r\n" % priorsupbit
        if(priorsupbit == 0):
            return_data += "Task priority is not supported by the Logical Unit\r\n"
        if(priorsupbit == 1):
            return_data += "Task priority is supported by the Logical Unit\r\n"
        headsupbit = (vpddata.data[dataindex] & 0x4) >> 2
        return_data += "HEADSUP: %01x\r\n" % headsupbit
        if(headsupbit == 0):
            return_data += "HEAD OF QUEUE task attribute is not supported by the Logical Unit\r\n"
        if(headsupbit == 1):
            return_data += "HEAD OF QUEUE task attribute is supported by the Logical Unit\r\n"
        ordsupbit = (vpddata.data[dataindex] & 0x2) >> 1
        return_data += "ORDSUP: %01x\r\n" % ordsupbit
        if(ordsupbit == 0):
            return_data += "ORDERED task attribute is not supported by the Logical Unit\r\n"
        if(ordsupbit == 1):
            return_data += "ORDERED task attribute is supported by the Logical Unit\r\n"
        smpsupbit = (vpddata.data[dataindex] & 0x1)
        return_data += "SIMPSUP: %01x\r\n" % smpsupbit
        if(smpsupbit == 0):
            return_data += "SIMPLE task attribute is not supported by the Logical Unit\r\n"
        if(smpsupbit == 1):
            return_data += "SIMPLE task attribute is supported by the Logical Unit\r\n"

        dataindex +=1
        nvsupbit = (vpddata.data[dataindex] & 0x2) >> 1
        return_data += "NV_SUP: %01x\r\n" % nvsupbit
        if(nvsupbit == 0):
            return_data += "Device server may or may not support a non-volatile cache\r\n"
        if(nvsupbit == 1):
            return_data += "Device server supports a non-volatile cache\r\n"
        vsupbit = (vpddata.data[dataindex] & 0x1)
        return_data += "V_SUP: %01x\r\n" % vsupbit
        if(vsupbit == 0):
            return_data += "Device server may or may not support a volatile cache\r\n"
        if(vsupbit == 1):
            return_data += "Device server supports a volatile cache\r\n"

        dataindex += 1
    #vpd ATA page 89
    if(pagecode == 0x89):
        dataindex = 1
        return_data += "ATA Information VPD Page\r\n"
        return_data += "PAGE CODE: %02x\r\n" % vpddata.data[dataindex]
        dataindex = 2
        pagelength = (vpddata.data[dataindex] << 8) | vpddata.data[dataindex + 1] 
        return_data += "PAGE LENGTH: %02x\r\n" % pagelength
        dataindex = 8
        return_data += "SAT VENDOR IDENTIFICATION: %s\r\n" % convertBufToChar(vpddata.data[dataindex: 16])
        dataindex = 16
        return_data += "SAT PRODUCT IDENTIFICATION: %s\r\n" % convertBufToChar(vpddata.data[dataindex: 32])
        dataindex = 32
        return_data += "SAT PRODUCT REVISION LEVEL: %s\r\n" % convertBufToChar(vpddata.data[dataindex: 36])
        dataindex = 36
        return_data += "ATA device signature shall contain the contents of the task file registers\r\n"
        return_data += "after the last power-on reset, hardware reset, software reset,\r\n"
        return_data += "or ATA EXECUTE DEVICE DIAGNOSTIC command : \r\n"
        transportid = vpddata.data[dataindex]
        if(transportid == 0):
            return_data += "TRANSPORT IDENTIFIER %04x PATA" % transportid
        elif(transportid == 0x34):
            return_data += "TRANSPORT IDENTIFIER %04x SATA" % transportid
        else:
            return_data += "TRANSPORT IDENTIFIER %04x RESERVED" % transportid
        return_data += "\r\n"

        dataindex = 37
        interrupt =  (vpddata.data[dataindex] & 0x40) >> 7
        return_data += "INTERRUPT: %01x\r\n" % interrupt
        pmport =  (vpddata.data[dataindex] & 0x0f)
        return_data += "PM PORT: %02x\r\n" % pmport
        dataindex = 38
        return_data += "\r\n"
        
        return_data += "TASK FILE REGISTERS\r\n"        
        status =  vpddata.data[dataindex]
        return_data += "STATUS: %02x\r\n" % status
        dataindex = 39
        error =  vpddata.data[dataindex]
        return_data += "ERROR: %02x\r\n" % error
        dataindex = 40
        lba70 =  vpddata.data[dataindex]        
        return_data += "LBA(7:0): %02x\r\n" % lba70
        dataindex = 41
        lba158 =  vpddata.data[dataindex]        
        return_data += "LBA(15:8): %02x\r\n" % lba158
        dataindex = 42
        lba2316 =  vpddata.data[dataindex]        
        return_data += "LBA(23:16): %02x\r\n" % lba2316
        dataindex = 43
        device =  vpddata.data[dataindex]        
        return_data += "DEVICE: %02x\r\n" % device
        dataindex = 44
        lba3124 =  vpddata.data[dataindex]        
        return_data += "LBA(31:24): %02x\r\n" % lba3124
        dataindex = 45
        lba3932 =  vpddata.data[dataindex]        
        return_data += "LBA(39:32): %02x\r\n" % lba3932
        dataindex = 46
        lba4740 =  vpddata.data[dataindex]        
        return_data += "LBA(47:40): %02x\r\n" % lba4740
        dataindex = 48
        sectorcount70 =  vpddata.data[dataindex]        
        return_data += "SECTOR COUNT(7:0): %02x\r\n" % sectorcount70
        dataindex = 49
        sectorcount158 =  vpddata.data[dataindex]        
        return_data += "SECTOR COUNT(15:8): %02x\r\n" % sectorcount158
        dataindex = 56
        return_data += "END OF TASK FILE REGISTERS\r\n"
        return_data += "\r\n"
        
        commandcode =  vpddata.data[dataindex]        
        return_data += "COMMAND CODE: %02X\r\n" % commandcode
        return_data += "COMMAND CODE field contains the ATA command code used to retrieve\r\n"
        return_data += "the data in the ATA IDENTIFY DEVICE or ATA IDENTIFY PACKET DEVICE DATA field.\r\n"
        if( pagelength > 60 ):
            dataindex = 60
            word_data = []
            return_data += "Parsed IDENTIFY DEVICE\r\n"
            return_data += "DATAINDEX %d\r\n" % dataindex
            #SWAPDATA
            word_data = swapcombinebytestoword(vpddata.data[60: pagelength])
            #*** GET SERIAL NUMBER ***
            return_data += "WORD 10-19\r\n"
            step = 10
            parseataserialnumber = ""
            maxstep = 20
            while(step < maxstep):
                tempholderbyte = (int(word_data[step], 16) & 0xFF00) >> 8
#                return_data += "tempholderbyte:L %d %x " % (step, tempholderbyte)
                parseataserialnumber += "%c" % tempholderbyte
                
                tempholderbyte = (int(word_data[step], 16) & 0x00FF)
#                return_data += "tempholderbyte:R %d %x\r\n" % (step, tempholderbyte)
                parseataserialnumber += "%c" % tempholderbyte
                
                step +=1
            return_data += "Serial Number: %s \r\n" % parseataserialnumber
            
            #*** GET FW VERSION
            return_data += "WORD 23-26\r\n"
            step = 23
            parsefwversion = ""
            maxstep = 27
           
            while(step < maxstep):
                tempholderbyte = (int(word_data[step], 16) & 0xFF00) >> 8
#                return_data += "tempholderbyte:L %d %x " % (step, tempholderbyte)
                parsefwversion += "%c" % tempholderbyte
                
                tempholderbyte = (int(word_data[step], 16) & 0x00FF)
#                return_data += "tempholderbyte:R %d %x\r\n" % (step, tempholderbyte)
                parsefwversion += "%c" % tempholderbyte
                
                step +=1
            return_data += "Firmware revision: %s \r\n" % parsefwversion

            #*** GET Model number
            return_data += "WORD 27-47\r\n"
            step = 27
            parsemodelnumber = ""
            maxstep = 47
           
            while(step < maxstep):
                tempholderbyte = (int(word_data[step], 16) & 0xFF00) >> 8
#                return_data += "tempholderbyte:L %d %x " % (step, tempholderbyte)
                parsemodelnumber += "%c" % tempholderbyte
                
                tempholderbyte = (int(word_data[step], 16) & 0x00FF)
#                return_data += "tempholderbyte:R %d %x\r\n" % (step, tempholderbyte)
                parsemodelnumber += "%c" % tempholderbyte
                
                step +=1
            return_data += "Model Number: %s \r\n" % parsemodelnumber
            
            # test word 49 Capabilities
            return_data += "WORD 49\r\n"
            wordindex = 49
            
            if(int(word_data[wordindex], 16) & 0x2000):
                return_data += "Standby timer values as specified in this standard are supported(ATA-8ACS)"
            else:
                return_data += "Standby timer values shall be managed by the device"
            return_data += "\r\n"
            
            if(int(word_data[wordindex], 16) & 0x0800):
                return_data += "IORDY supported"
            else:
                return_data += "IORDY may be supported"
            return_data += "\r\n"
            
            if(int(word_data[wordindex], 16) & 0x0400):
                return_data += "IORDY may be disabled"
            else:
                return_data += "IORDY may not be disabled"
            return_data += "\r\n"
            
            if(int(word_data[wordindex], 16) & 0x0100):
                return_data += "DMA supported"
            else:
                return_data += "DMA not supported"
            return_data += "\r\n"

            # test word 53 Capabilities
            wordindex = 53
            return_data += "WORD 53\r\n"
            parsefreefallsensitivity = ""
            tempholderbyte = (int(word_data[wordindex], 16) & 0xFF00) >> 8
            parsefreefallsensitivity += "%02x" % tempholderbyte
            return_data += "Free-fall Control Sensitivity: %s\r\n" % parsefreefallsensitivity
            
            if(int(word_data[wordindex], 16) & 0x0004):
                return_data += "The fields reported in word 88 are valid"
            else:
                return_data += "The fields reported in word 88 are not valid"
            return_data += "\r\n"

            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "The fields reported in words (70:64) are valid"
            else:
                return_data += "The fields reported in words (70:64) are not valid"
            return_data += "\r\n"
            
            # test word 59
            wordindex = 59
            return_data += "WORD 59\r\n"
            
            if(int(word_data[wordindex], 16) & 0x0100):
                return_data += "Multiple logical sector setting is valid"
            else:
                return_data += "Multiple logical sector setting is not valid"
            return_data += "\r\n"

            parsenumlogsectrans = ""
            tempholderbyte = (int(word_data[wordindex], 16) & 0x00FF)
            parsenumlogsectrans += "%02x\r\n" % tempholderbyte
            return_data += "Current setting for number of logical sectors that shall be \r\n"
            return_data += "transferred per DRQ data block on READ/WRITE Multiple commands: %s\r\n" % parsenumlogsectrans
            return_data += "\r\n"
            
            # test word 63
            wordindex = 63
            return_data += "WORD 63\r\n"
            if(int(word_data[wordindex], 16) & 0x0400):
                return_data += "Multiword DMA mode 2 is selected"
            else:
                return_data += "Multiword DMA mode 2 is not selected"
            return_data += "\r\n"
 
            if(int(word_data[wordindex], 16) & 0x0200):
                return_data += "Multiword DMA mode 1 is selected"
            else:
                return_data += "Multiword DMA mode 1 is not selected"
            return_data += "\r\n"
            
            if(int(word_data[wordindex], 16) & 0x0100):
                return_data += "Multiword DMA mode 0 is selected"
            else:
                return_data += "Multiword DMA mode 0 is not selected"
            return_data += "\r\n"
            
            if(int(word_data[wordindex], 16) & 0x0004):
                return_data += "Multiword DMA mode 2 and below are supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "Multiword DMA mode 1 and below are supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0001):
                return_data += "Multiword DMA mode 0 is supported\r\n"
            return_data += "\r\n"
            
            # test word 65
            wordindex = 65
            return_data += "WORD %d Minimum Multiword DMA transfer cycle time per word\r\n" % wordindex
            return_data += "%d Cycle time in nanoseconds\r\n" % int(word_data[wordindex], 16)
            return_data += "\r\n"

            # test word 66
            wordindex = 66
            return_data += "WORD %d Manufacturer's recommended Multiword DMA transfer cycle time\r\n" % wordindex
            return_data += "%d Cycle time in nanoseconds\r\n" % int(word_data[wordindex], 16)
            return_data += "\r\n"
            
            # test word 67
            wordindex = 67
            return_data += "WORD %d Minimum PIO transfer cycle time without flow control\r\n" % wordindex
            return_data += "%d Cycle time in nanoseconds\r\n" % int(word_data[wordindex], 16)
            return_data += "\r\n"
            
            # test word 68
            wordindex = 68
            return_data += "WORD %d Minimum PIO transfer cycle time with IORDY flow control\r\n" % wordindex
            return_data += "%d Cycle time in nanoseconds\r\n" % int(word_data[wordindex], 16)
            return_data += "\r\n"
            
            # test word 75
            wordindex = 75
            return_data += "WORD %d Queue depth\r\n" % wordindex
            return_data += "Queue Depth: %d Maximum queue depth - 1\r\n" % (int(word_data[wordindex], 16) & 0x001f)
            return_data += "\r\n"
            
            # test word 76
            wordindex = 76
            return_data += "WORD %d Serial ATA Capabilities\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x0400):
                return_data += "Supports Phy Event Counters\r\n"
            if(int(word_data[wordindex], 16) & 0x0200):
                return_data += "Supports receipt of host initiated power management requests\r\n"
            if(int(word_data[wordindex], 16) & 0x0100):
                return_data += "Supports the NCQ feature set\r\n"
            if(int(word_data[wordindex], 16) & 0x0004):
                return_data += "Supports SATA Gen2 Signaling Speed (3.0Gb/s)\r\n"
            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "Supports SATA Gen1 Signaling Speed (1.5Gb/s)\r\n"
            return_data += "\r\n"
            
            # test word 78
            wordindex = 78
            return_data += "WORD %d Serial ATA features supported\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x0040):
                return_data += "Device supports Software Settings Preservation\r\n"
            if(int(word_data[wordindex], 16) & 0x0020):
                return_data += "Reserved for Serial ATA\r\n"
            if(int(word_data[wordindex], 16) & 0x0010):
                return_data += "Device supports in-order data delivery\r\n"
            if(int(word_data[wordindex], 16) & 0x0008):
                return_data += "Device supports initiating power management\r\n"
            if(int(word_data[wordindex], 16) & 0x0004):
                return_data += "Device supports DMA Setup auto-activation\r\n"
            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "Device supports non-zero buffer offsets\r\n"
            return_data += "\r\n"
            
            # test word 79
            wordindex = 79
            return_data += "WORD %d Serial ATA features enabled\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x0040):
                return_data += "Software Settings Preservation enabled\r\n"
            if(int(word_data[wordindex], 16) & 0x0020):
                return_data += "Reserved for Serial ATA\r\n"
            if(int(word_data[wordindex], 16) & 0x0010):
                return_data += "In-order data delivery enabled\r\n"
            if(int(word_data[wordindex], 16) & 0x0008):
                return_data += "Device initiated power management enabled\r\n"
            if(int(word_data[wordindex], 16) & 0x0004):
                return_data += "DMA Setup auto-activation enabled\r\n"
            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "Non-zero buffer offsets enabled\r\n"
            return_data += "\r\n"
            
            # test word 80
            wordindex = 80
            return_data += "WORD %d Major version number\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x0100):
                return_data += "Supports ATA8-ACS\r\n"
            if(int(word_data[wordindex], 16) & 0x0080):
                return_data += "Supports ATA/ATAPI-7\r\n"
            if(int(word_data[wordindex], 16) & 0x0040):
                return_data += "Supports ATA/ATAPI-6\r\n"
            if(int(word_data[wordindex], 16) & 0x0020):
                return_data += "supports ATA/ATAPI-5\r\n"
            if(int(word_data[wordindex], 16) & 0x0010):
                return_data += "supports ATA/ATAPI-4\r\n"
            return_data += "\r\n"
            
            # test word 82
            wordindex = 82
            return_data += "WORD %d Commands and feature sets supported\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x4000):
                return_data += "The NOP command is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x2000):
                return_data += "The READ BUFFER command is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x1000):
                return_data += "The WRITE BUFFER command is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0400):
                return_data += "The HPA feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0200):
                return_data += "Shall be cleared to zero to indicate that\r\n"
                return_data += "the DEVICE RESET command is not supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0100):
                return_data += "The SERVICE interrupt is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0080):
                return_data += "The release interrupt is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0040):
                return_data += "Read look-ahead is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0020):
                return_data += "The volatile write cache is supported\r\n"
            if((int(word_data[wordindex], 16) & 0x0010) == 0 ):
                return_data += "Shall be cleared to zero to indicate that the PACKET feature set is not supported\r\n"
            if((int(word_data[wordindex], 16) & 0x0008) == 0):
                return_data += "Shall be set to one to indicate that the mandatory Power Management feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "The Security feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0001):
                return_data += "The SMART feature set is supported\r\n"
            return_data += "\r\n"
            
            # test word 83
            wordindex = 83
            return_data += "WORD %d Commands and feature sets supported\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x2000):
                return_data += "The FLUSH CACHE EXT command is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x1000):
                return_data += "Shall be set to one to indicate that the mandatory FLUSH CACHE command is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0800):
                return_data += "The DCO feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0400):
                return_data += "The 48-bit Address feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0200):
                return_data += "The AAM feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0100):
                return_data += "The SET MAX security extension is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0040):
                return_data += "SET FEATURES subcommand is required to spin-up after power-up\r\n"
            if(int(word_data[wordindex], 16) & 0x0020):
                return_data += "The PUIS feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0008):
                return_data += "The APM feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0004):
                return_data += "The CFA feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "The TCQ feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0001):
                return_data += "The DOWNLOAD MICROCODE command is supported\r\n"
            return_data += "\r\n"
            
            # test word 84
            wordindex = 84
            return_data += "WORD %d Commands and feature sets supported\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x2000):
                return_data += "The AAM feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0100):
                return_data += "The 64-bit World wide name is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0080):
                return_data += "The WRITE DMA QUEUED FUA EXT command is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0040):
                return_data += "The WRITE DMA FUA EXT and WRITE MULTIPLE FUA EXT commands are supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0020):
                return_data += "The GPL feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0010):
                return_data += "The Streaming feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0008):
                return_data += "The Media Card Pass Through Command feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0004):
                return_data += "Media serial number is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "The SMART self-test is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0001):
                return_data += "SMART error logging is supported\r\n"
            return_data += "\r\n"
            
            # test word 85
            wordindex = 85
            return_data += "WORD %d Commands and feature sets supported\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x4000):
                return_data += "The NOP command is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x2000):
                return_data += "The READ BUFFER command is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x1000):
                return_data += "The WRITE BUFFER command is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0400):
                return_data += "HPA feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0200):
                return_data += "Shall be cleared to zero to indicate that the DEVICE RESET command is not supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0100):
                return_data += "The SERVICE interrupt is enabled\r\n"
            if(int(word_data[wordindex], 16) & 0x0080):
                return_data += "The release interrupt is enabled\r\n"
            if(int(word_data[wordindex], 16) & 0x0040):
                return_data += "Read look-ahead is enabled\r\n"
            if(int(word_data[wordindex], 16) & 0x0020):
                return_data += "The volatile write cache is enabled\r\n"
            if((int(word_data[wordindex], 16) & 0x0010) == 0):
                return_data += "Shall be cleared to zero to indicate that the PACKET feature set is not supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0008):
                return_data += "Shall be set to one to indicate that the mandatory Power Management feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "The Security feature set is enabled\r\n"
            if(int(word_data[wordindex], 16) & 0x0001):
                return_data += "The SMART feature set is enabled\r\n"
            return_data += "\r\n"
            
            # test word 86
            wordindex = 86
            return_data += "WORD %d Commands and feature sets supported\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x8000):
                return_data += "Words 119-120 are valid\r\n"
            if(int(word_data[wordindex], 16) & 0x2000):
                return_data += "FLUSH CACHE EXT command supported\r\n"
            if(int(word_data[wordindex], 16) & 0x1000):
                return_data += "FLUSH CACHE command supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0800):
                return_data += "The DCO feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0400):
                return_data += "The 48-bit Address features set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0200):
                return_data += "The AAM feature set is enabled\r\n"
            if(int(word_data[wordindex], 16) & 0x0100):
                return_data += "The SET MAX security extension is enabled by SET MAX SET PASSWORD\r\n"
            if(int(word_data[wordindex], 16) & 0x0040):
                return_data += "SET FEATURES subcommand is required to spin-up after power-up\r\n"
            if(int(word_data[wordindex], 16) & 0x0020):
                return_data += "The PUIS feature set is enabled\r\n"
            if(int(word_data[wordindex], 16) & 0x0008):
                return_data += "The APM feature set is enabled\r\n"
            if(int(word_data[wordindex], 16) & 0x0004):
                return_data += "The CFA feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "The TCQ feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0001):
                return_data += "The DOWNLOAD MICROCODE command is supported\r\n"
            return_data += "\r\n"

            # test word 87
            wordindex = 87
            return_data += "WORD %d Commands and feature sets supported\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x2000):
                return_data += "The IDLE IMMEDIATE command with UNLOAD FEATURE is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0100):
                return_data += "The 64-bit World wide name is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0080):
                return_data += "The WRITE DMA QUEUED FUA EXT command is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0040):
                return_data += "The WRITE DMA FUA EXT and WRITE MULTIPLE FUA EXT commands are supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0020):
                return_data += "The GPL feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0008):
                return_data += "The Media Card Pass Through Command feature set is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0004):
                return_data += "Media serial number is valid\r\n"
            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "SMART self-test supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0001):
                return_data += "SMART error logging is supported\r\n"
            return_data += "\r\n"

            # test word 88
            wordindex = 88
            return_data += "WORD %d Ultra DMA modes\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x4000):
                return_data += "Ultra DMA mode 6 is selected\r\n"
            elif((int(word_data[wordindex], 16) & 0x4000) == 0):
                return_data += "Ultra DMA mode 6 is not selected\r\n"
            if(int(word_data[wordindex], 16) & 0x2000):
                return_data += "Ultra DMA mode 5 is selected\r\n"
            elif((int(word_data[wordindex], 16) & 0x2000) == 0):
                return_data += "Ultra DMA mode 5 is not selected\r\n"
            if(int(word_data[wordindex], 16) & 0x1000):
                return_data += "Ultra DMA mode 4 is selected\r\n"
            elif((int(word_data[wordindex], 16) & 0x1000) == 0):
                return_data += "Ultra DMA mode 4 is not selected\r\n"
            if(int(word_data[wordindex], 16) & 0x0800):
                return_data += "Ultra DMA mode 3 is selected\r\n"
            elif((int(word_data[wordindex], 16) & 0x0800) == 0):
                return_data += "Ultra DMA mode 3 is not selected\r\n"
            if(int(word_data[wordindex], 16) & 0x0400):
                return_data += "Ultra DMA mode 2 is selected\r\n"
            elif((int(word_data[wordindex], 16) & 0x0400) == 0):
                return_data += "Ultra DMA mode 2 is not selected\r\n"
            if(int(word_data[wordindex], 16) & 0x0200):
                return_data += "Ultra DMA mode 1 is selected\r\n"
            elif((int(word_data[wordindex], 16) & 0x0200) == 0):
                return_data += "Ultra DMA mode 1 is not selected\r\n"
            if(int(word_data[wordindex], 16) & 0x0100):
                return_data += "Ultra DMA mode 0 is selected\r\n"
            elif((int(word_data[wordindex], 16) & 0x0100) == 0):
                return_data += "Ultra DMA mode 0 is not selected\r\n"
            if(int(word_data[wordindex], 16) & 0x0040):
                return_data += "Ultra DMA mode 6 and below are supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0020):
                return_data += "Ultra DMA mode 5 and below are supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0010):
                return_data += "Ultra DMA mode 4 and below are supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0008):
                return_data += "Ultra DMA mode 3 and below are supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0004):
                return_data += "Ultra DMA mode 2 and below are supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "Ultra DMA mode 1 and below are supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0001):
                return_data += "Ultra DMA mode 0 is supported\r\n"
            return_data += "\r\n"

            # test word 89
            wordindex = 89
            return_data += "WORD %d Time required for Normal Erase mode SECURITY ERASE UNIT command\r\n" % wordindex
            return_data += "%d \r\n" % (int(word_data[wordindex], 16) & 0x00FF)
            return_data += "\r\n"

            # test word 90
            wordindex = 90
            return_data += "WORD %d Time required for an Enhanced Erase mode SECURITY ERASE UNIT command\r\n" % wordindex
            return_data += "%d \r\n" % (int(word_data[wordindex], 16) & 0x00FF)
            return_data += "\r\n"

            # test word 91
            wordindex = 91
            return_data += "WORD %d Current APM level value\r\n" % wordindex
            return_data += "%d \r\n" % (int(word_data[wordindex], 16) & 0xFFFF)
            return_data += "\r\n"

            # test word 92
            wordindex = 92
            return_data += "WORD %d Master Password Identifier\r\n" % wordindex
            return_data += "%d \r\n" % (int(word_data[wordindex], 16) & 0xFFFF)
            return_data += "\r\n"

            # test word 93
            wordindex = 93
            return_data += "WORD %d Hardware reset result\r\n" % wordindex
            return_data += "The contents of bits (12:0) of this word shall\r\n"
            return_data += "change only during the execution of a hardware reset.\r\n"
            return_data += "See 7.16.7.45 for more information."
            return_data += "\r\n"
            if(int(word_data[wordindex], 16) & 0x2000):
                return_data += "Device detected CBLID- above ViHB\r\n"
            elif((int(word_data[wordindex], 16) & 0x2000) == 0):
                return_data += "Device detected CBLID- below ViLB\r\n"
            return_data += "Device 1 hardware reset result. Device 0 shall clear these bits to zero.\r\n"
            return_data += "Device 1 shall set these bits as follows:\r\n"
            if(int(word_data[wordindex], 16) & 0x0800):
                return_data += "Device 1 asserted PDIAG-\r\n"
            elif((int(word_data[wordindex], 16) & 0x0800) == 0):
                return_data += "Device 1 did not assert PDIAG-.\r\n"
            return_data += "These bits indicate how Device 1 determined the device number:\r\n"
            if((int(word_data[wordindex], 16) & 0x0600) == 0):
                return_data += "Reserved.\r\n"
            elif((int(word_data[wordindex], 16) & 0x0600) == 0200):
                return_data += "A jumper was used.\r\n"
            elif((int(word_data[wordindex], 16) & 0x0600) == 0400):
                return_data += "The CSEL signal was used.\r\n"
            elif((int(word_data[wordindex], 16) & 0x0600) == 0600):
                return_data += "some other method was used or the method is unknown\r\n"
            return_data += "Device 0 hardware reset result. Device 1 shall clear these bits to zero.\r\n"
            return_data += "Device 0 shall set these bits as follows:\r\n"
            if(int(word_data[wordindex], 16) & 0x0800):
                return_data += "Device 1 asserted PDIAG-\r\n"
            elif((int(word_data[wordindex], 16) & 0x0800) == 0):
                return_data += "Device 1 did not assert PDIAG-.\r\n"
            return_data += "These bits indicate how Device 1 determined the device number:\r\n"
            if(int(word_data[wordindex], 16) & 0x0040): 
                return_data += "Device 0 responds when Device 1 is selected\r\n"
            elif((int(word_data[wordindex], 16) & 0x0040) == 0):
                return_data += "Device 0 does not respond when Device 1 is selected.\r\n"
            if(int(word_data[wordindex], 16) & 0x0020):
                return_data += "Device 0 detected the assertion of DASP-.\r\n"
            elif((int(word_data[wordindex], 16) & 0x0020) == 0):
                return_data += "Device 0 did not detect the assertion of DASP-\r\n"
            if(int(word_data[wordindex], 16) & 0x0010):
                return_data += "Device 0 detected the assertion of PDIAG-\r\n"
            elif((int(word_data[wordindex], 16) & 0x0010) == 0):
                return_data += "Device 0 did not detect the assertion of PDIAG-.\r\n"
            if(int(word_data[wordindex], 16) & 0x0008):
                return_data += "Device 0 passed diagnostics.\r\n"
            elif((int(word_data[wordindex], 16) & 0x0008) == 0):
                return_data += "Device 0 failed diagnostics.\r\n"
            return_data += "These bits indicate how Device 0 determined the device number:\r\n"
            if((int(word_data[wordindex], 16) & 0x0006) == 0):
                return_data += "Reserved.\r\n"
            elif((int(word_data[wordindex], 16) & 0x0006) == 2):
                return_data += "A jumper was used.\r\n"
            elif((int(word_data[wordindex], 16) & 0x0006) == 4):
                return_data += "The CSEL signal was used.\r\n"
            elif((int(word_data[wordindex], 16) & 0x0006) == 6):
                return_data += "Some other method was used or the method is unknown.\r\n"
            return_data += "\r\n"

            # test word 94
            wordindex = 94
            return_data += "WORD %d Current AAM value\r\n" % wordindex
            tempholderbyte = (int(word_data[step], 16) & 0xFF00) >> 8
            return_data += "Vendor's recommended AAM value %d\r\n" % tempholderbyte
            return_data += "Current AAM value: %d \r\n" % (int(word_data[wordindex], 16) & 0x00FF)
            return_data += "\r\n"
            
            # test word 95
            wordindex = 95
            return_data += "WORD %d Stream Minimum Request Size: %d\r\n" % (wordindex, int(word_data[wordindex], 16))
            return_data += "\r\n"

            # test word 96
            wordindex = 96
            return_data += "WORD %d Streaming Transfer Time - DMA: %d\r\n" % (wordindex, int(word_data[wordindex], 16))
            return_data += "\r\n"

            # test word 97
            wordindex = 97
            return_data += "WORD %d Streaming Access Latency - DMA and PIO: %d\r\n" % (wordindex, int(word_data[wordindex], 16))
            return_data += "\r\n"

            # test word 98
            wordindex = 98
            return_data += "WORD %d and %d Streaming Performance Granularity (DWord): %x%x\r\n" % (wordindex, wordindex + 1, int(word_data[wordindex], 16), int(word_data[wordindex + 1], 16))
            return_data += "\r\n"

            # test word 100
            wordindex = 100
            return_data += "Word 100-103 Total Number of User Addressable Logical Sectors for 48-bit commands (QWord)\r\n"
            return_data += "%x%x%x%x\r\n" % (int(word_data[wordindex], 16), int(word_data[wordindex + 1], 16), int(word_data[wordindex + 2], 16),int(word_data[wordindex + 3], 16))
            return_data += "\r\n"

            # test word 104
            wordindex = 104
            return_data += "WORD %d Streaming Transfer Time - PIO %d\r\n" % (wordindex, int(word_data[wordindex], 16))
            return_data += "\r\n"

            # test word 106
            wordindex = 106
            return_data += "WORD %d Physical sector size / logical sector size\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x2000):
                return_data += "Device has multiple logical sectors per physical sector.\r\n"
            if(int(word_data[wordindex], 16) & 0x1000):
                return_data += "Device Logical Sector longer than 256 Words\r\n"
            return_data += "2X logical sectors per physical sector: %d\r\n" % int(word_data[wordindex], 16)
            return_data += "\r\n"

            # test word 107
            wordindex = 107
            return_data += "WORD %d Inter-seek delay for ISO 7779 standard acoustic testing %d\r\n" % (wordindex, int(word_data[wordindex], 16))
            return_data += "\r\n"
            
            # test word 108-111
            wordindex = 108
            return_data += "WORD %d-111 World wide name %X%X%X%X\r\n" % (wordindex, int(word_data[wordindex], 16), int(word_data[wordindex + 1], 16), int(word_data[wordindex + 2], 16), int(word_data[wordindex + 3], 16))
            return_data += "\r\n"

            # test word 117-118
            wordindex = 117
            return_data += "WORD %d-118 Logical sector size (DWord) %X%X\r\n" % (wordindex, int(word_data[wordindex], 16), int(word_data[wordindex + 1], 16))
            return_data += "\r\n"

            # test word 119
            wordindex = 119
            return_data += "WORD %d Commands and feature sets supported (Continued from words 84:82)\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x0020):
                return_data += "The Free-fall Control feature set is enabled\r\n"
            if(int(word_data[wordindex], 16) & 0x0010):
                return_data += "The DOWNLOAD MICROCODE command with mode 3 is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0008):
                return_data += "The READ LOG DMA EXT and WRITE LOG DMA EXT commands are supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0004):
                return_data += "The WRITE UNCORRECTABLE EXT command is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "The Write-Read-Verify feature set is enabled\r\n"
            return_data += "\r\n"
            
            # test word 128
            wordindex = 128
            return_data += "WORD %d Security status\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x0100):
                return_data += "Mater Password Capability: MAximum\r\n"
            elif((int(word_data[wordindex], 16) & 0x0100) == 0):
                return_data += "Mater Password Capability: High\r\n"
            if(int(word_data[wordindex], 16) & 0x0020):
                return_data += "Enhanced security erase supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0010):
                return_data += "Security count expired\r\n"
            if(int(word_data[wordindex], 16) & 0x0008):
                return_data += "Security frozen\r\n"
            if(int(word_data[wordindex], 16) & 0x0004):
                return_data += "Security locked\r\n"
            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "Security enabled\r\n"
            if(int(word_data[wordindex], 16) & 0x0001):
                return_data += "Security supported\r\n"
            return_data += "\r\n"

            # test word 160
            wordindex = 160
            return_data += "WORD %d CFA power mode\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x8000):
                return_data += "Word 160 supported\r\n"
            if(int(word_data[wordindex], 16) & 0x2000):
                return_data += "CFA power mode 1 is required for one or more commands implemented by the device\r\n"
            if(int(word_data[wordindex], 16) & 0x1000):
                return_data += "CFA power mode 1 disabled\r\n"
            tempbyte = (int(word_data[wordindex], 16) & 0x0FFF)
            return_data += "Maximum current in ma %dma\r\n" % tempbyte
            return_data += "\r\n"

            # test word 168
            wordindex = 168
            return_data += "WORD %d Device Nominal Form Factor %d\r\n" % (wordindex, int(word_data[wordindex], 16) & 0x000f)
            return_data += "\r\n"

            # test word 176
            wordindex = 176
            return_data += "WORD %d-205 Current media serial number (ATA string)\r\n" % wordindex
            return_data_row = ""
            maxwordcount = 205
            while(wordindex <= maxwordcount):
                return_data_row += word_data[wordindex]
                wordindex += 2
            return_data += return_data_row
            return_data += "\r\n"
            return_data += "\r\n"
            
            # test word 206
            wordindex = 206
            return_data += "WORD %d SCT Command Transport\r\n" % wordindex
            if(int(word_data[wordindex], 16) & 0x0020):
                return_data += "The SCT Data Tables command is supported\r\n"
            if((int(word_data[wordindex], 16) & 0x0010) == 0):
                return_data += "The SCT Feature Control command is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0008):
                return_data += "The SCT Error Recovery Control command is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0004):
                return_data += "The SCT Write Same command is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "The SCT Read/Write Long command is supported\r\n"
            if(int(word_data[wordindex], 16) & 0x0001):
                return_data += "The SCT Command Transport is supported\r\n"
            return_data += "\r\n"
            return_data += "\r\n"
            
            
            # test word 209
            wordindex = 209
            return_data += "WORD %d Alignment of logical blocks within a physical block\r\n" % wordindex
            return_data += "%x\r\n" % (int(word_data[wordindex], 16) & 0x2FFF)
            return_data += "\r\n"

            # test word 210
            wordindex = 210
            return_data += "WORD %d-211 Write-Read-Verify Sector Count Mode 3 (DWord)\r\n" % wordindex
            return_data += "%x%x\r\n" % (int(word_data[wordindex], 16),int(word_data[wordindex + 1], 16))
            return_data += "\r\n"

            # test word 212
            wordindex = 212
            return_data += "WORD %d-213 Write-Read-Verify Sector Count Mode 2 (DWord)\r\n" % wordindex
            return_data += "%x%x\r\n" % (int(word_data[wordindex], 16),int(word_data[wordindex + 1], 16))
            return_data += "\r\n"

            # test word 214
            wordindex = 214
            return_data += "WORD %d NV Cache Capabilities\r\n" % wordindex
            return_data += "NV Cache Capabilities: %d" % (int(word_data[wordindex], 16) & 0xF000)
            return_data += "NV Cache Power Mode feature set version %d" % (int(word_data[wordindex], 16) & 0x0F00)
            if(int(word_data[wordindex], 16) & 0x0010):
                return_data += "NV Cache feature set enabled\r\n"
            if((int(word_data[wordindex], 16) & 0x0002) == 0):
                return_data += "NV Cache Power Mode feature set enabled\r\n"
            if(int(word_data[wordindex], 16) & 0x0001):
                return_data += "NV Cache Power Mode feature set supported\r\n"
            return_data += "\r\n"
            return_data += "\r\n"

            # test word 215
            wordindex = 215
            return_data += "WORD %d-216 NV Cache Size in Logical Blocks (DWord)\r\n" % wordindex
            return_data += "%x%x\r\n" % (int(word_data[wordindex], 16),int(word_data[wordindex + 1], 16))
            return_data += "\r\n"

            # test word 217
            wordindex = 217
            return_data += "WORD %d Nominal media rotation rate: %d\r\n" % (wordindex , int(word_data[wordindex], 16))
            return_data += "\r\n"

            # test word 219
            wordindex = 219
            return_data += "WORD %d Device Estimated Time to Spin Up in Seconds: %d\r\n" % (wordindex , (int(word_data[wordindex], 16) & 0x00ff))
            return_data += "\r\n"

            # test word 220
            wordindex = 220
            return_data += "WORD %d Write-Read-Verify feature set current mode: %d\r\n" % (wordindex , (int(word_data[wordindex], 16) & 0x00ff))
            return_data += "\r\n"

            # test word 222
            wordindex = 222
            return_data += "WORD %d Transport major version number\r\n" % wordindex
            if((int(word_data[wordindex], 16) == 0xffff) or (int(word_data[wordindex], 16) == 0)):
                return_data += "Device does not report version\r\n"
            elif((int(word_data[wordindex], 16) & 0xF000) == 0):
                return_data += "Parallel\r\n"
            elif((int(word_data[wordindex], 16) & 0xF000) == 0x1000):
                return_data += "Serial\r\n"
            elif(((int(word_data[wordindex], 16) & 0xF000) >= 0x2000) and ((int(word_data[wordindex], 16) & 0xF000) <= 0xF000)):
                return_data += "Reserved\r\n"
            if(int(word_data[wordindex], 16) & 0x0010):
                return_data += "SATA Rev 2.6\r\n"
            if(int(word_data[wordindex], 16) & 0x0008):
                return_data += "SATA Rev 2.5\r\n"
            if(int(word_data[wordindex], 16) & 0x0004):
                return_data += "SATA II: Extensions\r\n"
            if(int(word_data[wordindex], 16) & 0x0002):
                return_data += "SATA 1.0a\r\n"
            if(int(word_data[wordindex], 16) & 0x0001):
                return_data += "ATA8-AST\r\n"
            return_data += "\r\n"
            
            # test word 223
            wordindex = 223
            return_data += "WORD %d Transport minor version number: %x\r\n" % (wordindex , int(word_data[wordindex], 16))
            return_data += "\r\n"

            # test word 234
            wordindex = 234
            return_data += "WORD %d Minimum number of 512-byte data blocks per DOWNLOAD MICROCODE commandfor mode 03h: %d\r\n" % (wordindex , int(word_data[wordindex], 16))
            return_data += "\r\n"

            # test word 235
            wordindex = 235
            return_data += "WORD %d Maximum number of 512-byte data blocks per DOWNLOAD MICROCODE commandfor mode 03h: %d\r\n" % (wordindex , int(word_data[wordindex], 16))
            return_data += "\r\n"
            
            # test word 255
            wordindex = 255
            return_data += "WORD %d Integrity word\r\n" % wordindex
            
            return_data += "Checksum %d\r\n" % vpddata.data[571]
            return_data += "Checksum Validity Indicator %d\r\n" %  vpddata.data[570]
            return_data += "\r\n"
            
            


            return_data += "\r\n"
            return_data += "\r\n"
            return_data += "DATA DUMP IDENTIFY DEVICE BYTES COMBINED & SWAPPED\r\n"
            worddisplay = swapcombinebytestowordpluschar(vpddata.data[60: pagelength])
            return_data += worddisplay
            return_data += "\r\n"
            return_data += "DATA DUMP IDENTIFY DEVICE BYTES COMBINED\r\n"
            worddisplay = combinebytestowordpluschar(vpddata.data[60: pagelength])
            return_data += worddisplay
            return_data += "\r\n"
            
        return_data += "\r\n"

    #vpd page 8A - AF
    if(pagecode >= 0x8A and pagecode <= 0xAF):
        # THIS PAGE IS RESERVED
        return_data += "This page is RESERVED\r\n"
    #vpd page B0 - BF
    if(pagecode >= 0xB0 and pagecode <= 0xBF):
        # THIS PAGE IS RESERVED
        return_data += "See Spedific Device type\r\n"
        
        
    #vpd PARSE PAGE DC    
    if(pagecode == 0xDC):
        dataindex = 1
        return_data += "This page is DELL VENDOR SPECIFIC\r\n"
        return_data += "PAGE CODE: %02X\r\n" % vpddata.data[dataindex]
        dataindex = 2
        pagelength = (vpddata.data[dataindex] << 8) | vpddata.data[dataindex + 1] 
        return_data += "PAGE LENGTH: %04X\r\n" % pagelength
        dataindex = 4
        return_data += "VENDOR ID (DELL(tm), ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 12])
        dataindex = 12
        return_data += "PRODUCT ID (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 28])
        dataindex = 28
        return_data += "FIRMWARE REVISION LEVEL (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 32])
        dataindex = 52
        return_data += "TARGET DEVICE NAME (SAS): %X\r\n" % shiftbytes(vpddata.data[dataindex: 60] , 7)
        dataindex = 60
        return_data += "TARGET PORT IDENTIFIER 1 (SAS): %X\r\n" % shiftbytes(vpddata.data[dataindex: 68] , 7)
        dataindex = 68
        return_data += "TARGET PORT IDENTIFIER 2 (SAS): %X\r\n" % shiftbytes(vpddata.data[dataindex: 76] , 7)
        dataindex = 76
        return_data += "FORM FACTOR WIDTH (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 80])
        dataindex = 80
        return_data += "FORM FACTOR HEIGHT (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 84])
        dataindex = 84
        return_data += "DEVICE ID (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 92])
        dataindex = 92
        return_data += "SERVO CODE LEVEL (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 100])
        dataindex = 100
        return_data += "PCBA SERIAL NUMBER (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 116])
        dataindex = 116
        return_data += "PCBA PART NUMBER (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 132])
        dataindex = 132
        return_data += "DISK MEDIA VENDOR (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 148])
        dataindex = 148
        return_data += "MOTOR SERIAL NUMBER (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 164])
        dataindex = 164
        return_data += "FLEX CIRCUIT ASSEMBLY SERIAL NUMBER (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 180])
        dataindex = 180
        return_data += "HEAD VENDOR (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 196])
        dataindex = 196
        if(dataindex < pagelength):
            return_data += "HDC REVISION (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 212])
            dataindex = 212
            return_data += "ACTUATOR SERIAL NUMBER (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 228])
            dataindex = 228
            return_data += "HEAD DISK ASSEMBLY SERIAL NUMBER (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 244])
            dataindex = 244
            return_data += "YEAR OF MANUFACTURE (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 248])
            dataindex = 248
            return_data += "WEEK OF MANUFACTURE (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 250])
            dataindex = 250
            return_data += "DAY OF MANUFACTURE (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 252])
            dataindex = 252
            return_data += "LOCATION OF MANUFACTURE (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 260])
            dataindex = 260
            return_data += "DELL PPID (ASCII): %s\r\n" % convertBufToChar(vpddata.data[dataindex: 283])
            dataindex = 284
            return_data += "MEDIUM ROTATION RATE: %d\r\n" % shiftbytes(vpddata.data[dataindex: 286] , 1)
            dataindex = 286
            if(vpddata.data[dataindex] & 0x02) == 1:
                return_data += "DIF = 1\r\n"
            else:
                return_data += "DIF = 0\r\n"
            if(vpddata.data[dataindex] & 0x01) == 1:
                return_data += "SED = 1\r\n"
            else:
                return_data += "SED = 0\r\n"

        return_data += "\r\n"
        
    #vpd page C0 - FF
    if((pagecode >= 0xC0 and pagecode <= 0xFF) and pagecode != 0xDC):
        # THIS PAGE IS RESERVED
        return_data += "This page is VENDOR SPECIFIC\r\n"

    return_data += "Complete Raw Dump\r\n"           
    return_data += returnParsedData(vpddata)
    return return_data

def swapcombinebytestoword(data):

    dataindex = 0
    return_data = ""
    return_data_row = []
    wordcount = 0
    while(dataindex < len(data)):
        if((dataindex + 1) == len(data)):
            return_data_row.append("%02x" % data[dataindex])
        else:            
            return_data_row.append("%02x%02x" % (data[dataindex + 1], data[dataindex]))
        dataindex += 2
    #print len(data)
    return return_data_row
    
def combinebytestowordpluschar(data):

    dataindex = 0
    return_data = ""
    return_data_row = ""
    wordcount = 0
    while(dataindex < len(data)):
        return_data_row += ("WORD %04d: %02X%02X\t" % (wordcount, data[dataindex], data[dataindex + 1]))
        if ((data[dataindex] >= 0x20) and (data[dataindex] < 0x7F)):
            return_data_row += ("%c" % data[dataindex])
        else:
            return_data_row += "."  # eliminate non-printable characters            

        if ((data[dataindex + 1] >= 0x20) and (data[dataindex + 1] < 0x7F)):
            return_data_row += ("%c" % data[dataindex + 1])
        else:
            return_data_row += "."  # eliminate non-printable characters            
        return_data_row += "\r\n"
        dataindex += 2
        wordcount += 1
        
    return_data += return_data_row
    return return_data


def swapcombinebytestowordpluschar(data):

    dataindex = 0
    return_data = ""
    return_data_row = ""
    wordcount = 0
    while(dataindex < len(data)):
        return_data_row += ("WORD %04d: %02X%02X\t" % (wordcount, data[dataindex + 1], data[dataindex]))
        if ((data[dataindex + 1] >= 0x20) and (data[dataindex + 1] < 0x7F)):
            return_data_row += ("%c" % data[dataindex + 1])
        else:
            return_data_row += "."  # eliminate non-printable characters            
        if ((data[dataindex] >= 0x20) and (data[dataindex] < 0x7F)):
            return_data_row += ("%c" % data[dataindex])
        else:
            return_data_row += "."  # eliminate non-printable characters            
        return_data_row += "\r\n"
        dataindex += 2
        wordcount += 1
        
    return_data += return_data_row
    return return_data

    
def returnlogdata(pd, logpage):
        scsi_params = scsi.SCSI_PARAMS()
        scsi_params.op_code = sd.SCSI_LOG_SENSE
        scsi_params.page_code = logpage
        ret, scsi_pt = pd.create_scsi_passthru(scsi_params)
        if ret:
            return "Failed create passthru"
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = False)
        if ret:
            return "Failed sending passthru"
        else:
            return scsi_pt

def returnparsedlogdata(logdata):
    dataindex = 0
    return_data = ""
    pagecode = (logdata.data[0] & 0x3f)
    #return_data = "PAGE CODE: %02X\r\n" % pagecode
    
    if(pagecode >= 0x02 and pagecode <= 0x05):
        dataindex = 2
        pagelength = (logdata.data[dataindex] << 8) | logdata.data[dataindex + 1]
        return_data += "PAGE LENGTH: %04X\r\n" % pagelength
        if(pagecode == 0x02):
            return_data += "Write Error Counter\r\n"
        if(pagecode == 0x03):
            return_data += "Read Error Counter\r\n"
        if(pagecode == 0x04):
            return_data += "Read Reverse Error Counter\r\n"
        if(pagecode == 0x05):
            return_data += "Verify Error Counter\r\n"

        dataindex = 4
        while(dataindex < pagelength):
            paramcode = logdata.data[dataindex]
            paramcode << 8
            dataindex += 1
            paramcode += logdata.data[dataindex]
            #errors corrected without substantial delay
            if(paramcode == 0x0000):
                return_data += "Parameter code: %d Errors corrected without substantial delay:" % paramcode
            elif(paramcode == 0x0001):
                return_data += "Parameter code: %d Errors corrected with possible delays:" % paramcode
            elif(paramcode == 0x0002):
                return_data += "Parameter code: %d Total (e.g., rewrites or rereads):" % paramcode
            elif(paramcode == 0x0003):
                return_data += "Parameter code: %d Total errors corrected:" % paramcode
            elif(paramcode == 0x0004):
                return_data += "Parameter code: %d Total times correction algorithm processed:" % paramcode
            elif(paramcode == 0x0005):
                return_data += "Parameter code: %d Total bytes processed:" % paramcode
            elif(paramcode == 0x0006):
                return_data += "Parameter code: %d Total uncorrected errors:" % paramcode
            elif(paramcode >= 0x0007 and paramcode <= 0x7FFF):
                return_data += "Parameter code: %d Reserved:" % paramcode
            elif(paramcode >= 0x8000 and paramcode <= 0xFFFF):
                return_data += "Parameter code: %d Vendor specific:" % paramcode
            else:
                return_data += "Parameter code: %d INVALID PARAMETER CODE:" % paramcode
            #get size of counter
            dataindex += 2
            ecounter = logdata.data[dataindex]
            dataindex += 1
            looperrordata = 0
            errorvalue = 0
            while(looperrordata < ecounter):
                errorvalue |= (logdata.data[dataindex] << (8*(ecounter-looperrordata)))
                looperrordata += 1
            return_data += "%d\r\n" % errorvalue
            #bring back
            dataindex += ecounter
            #dataindex = pagelength
            #return_data += "MEDIUM ROTATION RATE: %d\r\n" % shiftbytes(vpddata.data[dataindex: 286] , 1)
        return_data += "\r\n"
            
    if(pagecode == 0x0D):
        return_data += "Temperature log page\r\n"
        dataindex = 0
        dataindex = 2
        pagelength = (logdata.data[dataindex] << 8) | logdata.data[dataindex + 1]
        return_data += "PAGE LENGTH: %04X\r\n" % pagelength
        return_data += "PARAMETER CODE 0x0000 Temperature\r\n"
        dataindex = 6
        if((logdata.data[dataindex] & 0x80) == 0):
            return_data += "DU:Value provided by device server\r\n"
        if(logdata.data[dataindex] & 0x40):
            return_data += "DS:Device server does not support saving of parameter\r\n"
        if((logdata.data[dataindex] & 0x20) == 0):
            return_data += "TSD:Device server does not support saving of parameter\r\n"
        if((logdata.data[dataindex] & 0x10) == 0):
            return_data += "ETC:No threshold comparison is made on this value\r\n"
        if((logdata.data[dataindex] & 0x02) == 1):
            return_data += "LBIN:The parameter is in binary format\r\n"
        if((logdata.data[dataindex] & 0x01) == 1):
            return_data += "LP:The parameter is a list parameter\r\n"
        dataindex = 9
        return_data += "TEMPERATURE (degrees Celsius): %d\r\n" % logdata.data[dataindex]
        return_data += "\r\n"
        return_data += "PARAMETER CODE 0x0001 Reference temperature\r\n"
        dataindex = 12
        if((logdata.data[dataindex] & 0x80) == 0):
            return_data += "DU:Value provided by device server\r\n"
        if(logdata.data[dataindex] & 0x40):
            return_data += "DS:Device server does not support saving of parameter\r\n"
        if((logdata.data[dataindex] & 0x20) == 0):
            return_data += "TSD:Device server does not support saving of parameter\r\n"
        if((logdata.data[dataindex] & 0x10) == 0):
            return_data += "ETC:No threshold comparison is made on this value\r\n"
        if((logdata.data[dataindex] & 0x02) == 1):
            return_data += "LBIN:The parameter is in binary format\r\n"
        if((logdata.data[dataindex] & 0x01) == 1):
            return_data += "LP:The parameter is a list parameter\r\n"
        dataindex = 15
        return_data += "TEMPERATURE (degrees Celsius): %d\r\n" % logdata.data[dataindex]
        return_data += "\r\n"

    if(pagecode == 0x10):
        return_data += "Self-test results log\r\n"
        dataindex = 2
        pagelength = (logdata.data[dataindex] << 8) | logdata.data[dataindex + 1]
        return_data += "PAGE LENGTH: %04X\r\n" % pagelength
        dataindex = 4

        while(dataindex <= pagelength):
            paramcode = logdata.data[dataindex]
            paramcode << 8
            # 5
            dataindex += 1
            paramcode += logdata.data[dataindex]
            
            
            return_data += "=========Test No.:%d=========\r\n" % paramcode
            #8
            dataindex += 3
            return_data += "SELF-TEST CODE: %02X " % (logdata.data[dataindex] >> 4 )
            if((logdata.data[dataindex] & 0xE0) == 0x00):
                return_data += "No TEST"
            if((logdata.data[dataindex] & 0xE0) == 0x20):
                return_data += "Bckgrd Short"
            if((logdata.data[dataindex] & 0xE0) == 0x40):
                return_data += "Bckgrd Ext."
            if((logdata.data[dataindex] & 0xE0) == 0x60):
                return_data += "Reserved."
            if((logdata.data[dataindex] & 0xE0) == 0x80):
                return_data += "Aborted."
            return_data += "\r\n"
            return_data += "SELF-TEST Results:"
            if((logdata.data[dataindex] & 0x0F) == 0x00):
                return_data += "The self-test completed without error.\r\n"
            if((logdata.data[dataindex] & 0x0F) == 0x01):
                return_data += "The background self-test was aborted by the application client using a\r\n"
                return_data += "SEND DIAGNOSTIC command (see 6.28) with the SELF-TEST CODE field set to\r\n"
                return_data += "100b (i.e., abort background self-test).\r\n"
            if((logdata.data[dataindex] & 0x0F) == 0x02):
                return_data += "The self-test routine was aborted by an application client using a method\r\n"
                return_data += "other than a SEND DIAGNOSTIC command with the SELF-TEST CODE field set to\r\n"
                return_data += "100b (e.g., by a task management function, or by issuing an exception\r\n"
                return_data += "command as defined in 5.5.3).\r\n"
                return_data += "An unknown error occurred while the device server was processing the self-test\r\n"
                return_data += "and the device server was unable to complete the self-test.\r\n"
            if((logdata.data[dataindex] & 0x0f) == 0x04):
                return_data += "The self-test completed with a failure in a test segment, and the test segment that failed is not known.\r\n"
            if((logdata.data[dataindex] & 0x0f) == 0x05):
                return_data += "The first segment of the self-test failed.\r\n"
            if((logdata.data[dataindex] & 0x0f) == 0x06):
                return_data += "The second segment of the self-test failed.\r\n"
            if((logdata.data[dataindex] & 0x0f) == 0x07):
                return_data += "Another segment of the self-test failed and which test is indicated by the\r\n"
                return_data += "contents of the SELF-TEST NUMBER field.\r\n"
            if((logdata.data[dataindex] & 0x0f) >= 0x08 and (logdata.data[dataindex] & 0x0f) <= 0x0e):
                return_data += "Reserved\r\n"
            if((logdata.data[dataindex] & 0x0f) == 0x0f):
                return_data += "The self-test is in progress\r\n"
            # 9
            dataindex += 1
            return_data += "Self Test Number:%d\r\n" % logdata.data[dataindex]
            #10
            dataindex += 1
            return_data += "Time Stamp:%02X%02X\r\n" % (logdata.data[dataindex], logdata.data[dataindex + 1])
            # 12
            dataindex += 2
            return_data += "ADDRESS OF FIRST FAILURE:"
            maxcount = dataindex + (15 - 8)
            while(dataindex <= maxcount):
                return_data += "%x" % logdata.data[dataindex]
                dataindex += 1
            return_data += "\r\n"
            #20
            return_data += "SENSE KEY %02X" % logdata.data[dataindex]
            return_data += "\r\n"
            #21
            dataindex += 1
            return_data += "ADDITIONAL SENSE CODE %02X" % logdata.data[dataindex]
            return_data += "\r\n"
            #22
            dataindex += 1
            return_data += "ADDITIONAL SENSE CODE QUALIFIER%02X" % logdata.data[dataindex]
            return_data += "\r\n"
            #23
            dataindex += 2

        dataindex = 4
        while(dataindex <= pagelength):
            paramcode = logdata.data[dataindex]
            paramcode << 8
            # 5
            dataindex += 1
            paramcode += logdata.data[dataindex]
            
            
            return_data += "Test No.:%04d" % paramcode
            #8
            dataindex += 3
            return_data += ":%02X:" % ((logdata.data[dataindex] >> 5 ) & 0x07)
            return_data += "%02X:" % (logdata.data[dataindex] & 0x0F)
            # 9
            dataindex += 1
            return_data += "%02X:" % logdata.data[dataindex]
            #10
            dataindex += 1
            return_data += "%02X%02X:" % (logdata.data[dataindex], logdata.data[dataindex + 1])
            # 12
            dataindex += 2
            maxcount = dataindex + (15 - 8)
            while(dataindex <= maxcount):
                return_data += "%x" % logdata.data[dataindex]
                dataindex += 1
            return_data += ":"
            #20
            return_data += "%02X:" % logdata.data[dataindex]
            #21
            dataindex += 1
            return_data += "%02X:" % logdata.data[dataindex]
            #22
            dataindex += 1
            return_data += "%02X" % logdata.data[dataindex]
            return_data += "\r\n"
            #23
            dataindex += 2
            
            #if(dataindex >= 46):
            #    dataindex = pagelength+1
            
        return_data += "\r\n"

    if(pagecode == 0x15):
        dataindex = 999999
        return_data += "Background Scan Results log page\r\n"
        dataindex = 2
        pagelength = (logdata.data[dataindex] << 8) | logdata.data[dataindex + 1]
        return_data += "PAGE LENGTH: %04X\r\n" % pagelength
        dataindex = 4
        paramcode = 0xFFFF
        while(dataindex < pagelength):
            paramcode = (logdata.data[dataindex] << 8) | logdata.data[dataindex + 1]

            if(paramcode == 0x0000):
                return_data += "===Background Scan Status parameter %04X===\r\n" % paramcode
                #return_data += "dataindex %d\r\n" % dataindex
                dataindex += 3
                #return_data += "dataindex %d\r\n" % dataindex
                paramlength = logdata.data[dataindex]
                maxparamcount = dataindex + paramlength
                dataindex += 1
                #return_data += "data index %d\r\n" % dataindex
                return_data += "ACCUMULATED POWER ON MINUTES %d\r\n" % shiftbytes(logdata.data[dataindex: (dataindex + 4) ], 3)
                #return_data += "data index %d\r\n" % dataindex
                dataindex += 5
                #return_data += "data index %d\r\n" % dataindex
                
                if((logdata.data[dataindex] & 0xff) == 0):
                    return_data += "No background scan operation is active.\r\n"
                elif((logdata.data[dataindex] & 0xff) == 1):
                    return_data += "A background medium scan operation is active.\r\n"
                elif((logdata.data[dataindex] & 0xff) == 2):
                    return_data += "A background pre-scan operation is active..\r\n"
                elif((logdata.data[dataindex] & 0xff) == 3):
                    return_data += "A background scan operation was halted due to a fatal error.\r\n"
                elif((logdata.data[dataindex] & 0xff) == 4):
                    return_data += "A background scan operation was halted due to a vendor specific pattern of errors.\r\n"
                elif((logdata.data[dataindex] & 0xff) == 5):
                    return_data += "A background scan operation was halted due to the medium being formatted without the P-list.\r\n"
                elif((logdata.data[dataindex] & 0xff) == 6):
                    return_data += "A background scan operation was halted due to a vendor specific cause.\r\n"
                elif((logdata.data[dataindex] & 0xff) == 7):
                    return_data += "A background scan operation was halted due to the temperature being out of the allowed range.\r\n"
                elif((logdata.data[dataindex] & 0xff) == 8):
                    return_data += "Background medium scan operations are enabled (i.e., the EN_BMS bit is set to one in the\r\n"
                    return_data += "Background Control mode page (see 6.3.3)), and no background medium scan operation is\r\n"
                    return_data += "active (i.e., the device server is waiting for Background Medium Scan Interval timer expiration\r\n"
                    return_data += "before starting the next background medium scan operation).\r\n"
                elif(logdata.data[dataindex] >= 0x09 and logdata.data[dataindex] <= 0x0f):
                    return_data += "Reserved.\r\n"
                dataindex += 1
                return_data += "NUMBER OF BACKGROUND SCANS PERFORMED %d\r\n" % shiftbytes(logdata.data[dataindex: (dataindex + 2) ], 1)
                dataindex += 2
                return_data += "BACKGROUND SCAN PROGRESS %d%%\r\n" % ((shiftbytes(logdata.data[dataindex: (dataindex + 2) ], 1) / 0xFFFF) * 100)
                dataindex += 2
                return_data += "NUMBER OF BACKGROUND MEDIUM SCANS PERFORMED %d\r\n" % shiftbytes(logdata.data[dataindex: (dataindex + 2) ], 1)
                dataindex += 2
                #return_data += "dataindex %d\r\n" % dataindex
            elif(paramcode >= 0x0001 and paramcode <= 0x0800):
                return_data += "===Background Scan parameter format %04X===\r\n" % paramcode
                #return_data += "dataindex %d\r\n" % dataindex
                dataindex += 3
                #return_data += "dataindex %d\r\n" % dataindex
                paramlength = logdata.data[dataindex]
                #maxparamcount = dataindex + paramlength
                dataindex += 1
                #return_data += "data index %d\r\n" % dataindex
                return_data += "ACCUMULATED POWER ON MINUTES %04X\r\n" % shiftbytes(logdata.data[dataindex: (dataindex + 4) ], 3)
                dataindex += 4
                #return_data += "data index %d\r\n" % dataindex
                
                return_data += "Reassign status\r\n"
                if((logdata.data[dataindex] & 0xf0) == 0):
                    return_data += "Error Logging: No -Reserved\r\n"
                elif((logdata.data[dataindex] & 0xf0) == 0x10):
                    return_data += "Error Logging: Yes -An error was detected while reading the logical block specified by the LOGICAL BLOCK\r\n"
                    return_data += "ADDRESS field during a background scan operation, and reassignment of the logical block is pending receipt\r\n"
                    return_data += "of: b c a) a command performing a write operation, if automatic write reassignment is allowed (i.e., the\r\n"
                    return_data += "AWRE bit is set to one in the Read-Write Error Recovery mode page (see 6.4.7); or b) a REASSIGN BLOCKS command\r\n"
                    return_data += "(see 5.19).Reserved\r\n"
                elif((logdata.data[dataindex] & 0xf0) == 0x20):
                    return_data += "Error Logging: No -An error was detected while reading the logical block specified by the LOGICAL BLOCK\r\n"
                    return_data += "ADDRESS field during a background scan operation and the logical block was reassigned by the device\r\n"
                    return_data += "server with recovered data.\r\n"
                elif((logdata.data[dataindex] & 0xf0)  == 0x30):
                    return_data += "Reserved.\r\n"
                elif((logdata.data[dataindex] & 0xf0) == 0x40):
                    return_data += "Error Logging: Yes -An error was detected:\r\n"
                    return_data += "a) while reading the logical block specified by the LOGICAL BLOCK ADDRESS field\r\n"
                    return_data += "during a background scan operation;\r\n"
                    return_data += "b) reassignment of the logical block by the device server failed; and\r\n"
                    return_data += "c) the logical block may or may not have an uncorrectable error.\r\n"
                elif((logdata.data[dataindex] & 0xf0) == 0x50):
                    return_data += "Error Logging: No -An error was detected while reading the logical block specified by the LOGICAL BLOCK\r\n"
                    return_data += "ADDRESS field during a background scan operation and the error was corrected by the\r\n"
                    return_data += "device server rewriting the logical block without reassignment\r\n"
                elif((logdata.data[dataindex] & 0xf0) == 0x60):
                    return_data += "Error Logging: Yes -An error was detected while reading the logical block specified by the LOGICAL BLOCK\r\n"
                    return_data += "ADDRESS field during a background scan operation, and the logical block:\r\n"
                    return_data += "a) was reassigned by the application client: and\r\n"
                    return_data += "b) contains valid data (e.g., as the result of reassignment by a REASSIGN\r\n"
                    return_data += "BLOCKS command during which the data was recovered, or by a command\r\n"
                    return_data += "performing a write operation)\r\n"
                elif((logdata.data[dataindex] & 0xf0) == 0x70):
                    return_data += "Error Logging: Yes -An error was detected while reading the logical block specified by the LOGICAL BLOCK\r\n"
                    return_data += "ADDRESS field during a background scan operation, and the logical block:\r\n"
                    return_data += "a) was reassigned by the application client; and\r\n"
                    return_data += "b) does not contain valid data (e.g., as a result of reassignment by a REASSIGN\r\n"
                    return_data += "BLOCKS command during which the data was not recovered).\r\n"
                elif((logdata.data[dataindex] & 0xf0) == 0x80):
                    return_data += "Error Logging: Yes -An error was detected while reading the logical block specified by the LOGICAL BLOCK\r\n"
                    return_data += "ADDRESS field during a background scan operation and the logical block was not\r\n"
                    return_data += "successfully reassigned by the application client (e.g., by a REASSIGN BLOCKS\r\n"
                    return_data += "command that failed)\r\n"
                elif((logdata.data[dataindex] & 0xf0) >= 0x90 and (logdata.data[dataindex] & 0xf0) <= 0xf0):
                    return_data += "Reserved.\r\n"
                return_data += "SENSE KEY %02X\r\n" % (logdata.data[dataindex] & 0x0f)                    
                dataindex += 1
                return_data += "ADDITIONAL SENSE CODE %02X\r\n" % logdata.data[dataindex]
                dataindex += 1
                return_data += "ADDITIONAL SENSE CODE QUALIFIER %02X\r\n" % logdata.data[dataindex]
                dataindex += 1
                #return_data += "dataindex %d\r\n" % dataindex
                return_data += "Vendor Specific: "
                shiftLBA = dataindex + 4
                
                while(dataindex <= shiftLBA):
                     return_data += "%02X" % logdata.data[dataindex]
                     dataindex += 1
                return_data += "\r\n"
                #return_data += "dataindex %d\r\n" % dataindex
                
                #return_data += "vendor specific %X\r\n" % shiftbytes(logdata.data[dataindex: (dataindex + 5) ], 4)
                #dataindex += 5
                return_data += "LOGICAL BLOCK ADDRESS: "
                shiftLBA = dataindex + 7
                while(dataindex <= shiftLBA):
                    try:
                        return_data += "%02X" % logdata.data[dataindex]
                    except IndexError:
                        print "at failure len of data buffer = %d, dataindex = %d" % (len(logdata.data), dataindex)
                        dataindex = pagelength + 1
                        break                        
                    #return_data += "%02X" % logdata.data[dataindex]
                    dataindex += 1
                return_data += "\r\n"
                return_data += "dataindex %d\r\n" % dataindex
                
                #if(paramcode == 0x0100):
                    

            else:
                dataindex = pagelength + 1
            
    if(pagecode == 0x2f):
        return_data += "Informational Exceptions log page\r\n"
        dataindex = 2
        pagelength = (logdata.data[dataindex] << 8) | logdata.data[dataindex + 1]
        return_data += "PAGE LENGTH: %04X\r\n" % pagelength
        dataindex = 4
        while(dataindex < pagelength):
            paramcode = (logdata.data[dataindex] << 8) | logdata.data[dataindex + 1]
            dataindex += 1
            if(paramcode == 0x0000):
                return_data += "===Informational exceptions general parameter data ===\r\n"
                return_data += "Parameter Code Decimal:%d Hex:%04X\r\n" % (paramcode, paramcode)
                dataindex += 2
                paramlength = logdata.data[dataindex]
                maxparamcount = dataindex + paramlength
                dataindex += 1
                return_data += "INFORMATIONAL EXCEPTION ADDITIONAL SENSE CODE %02X\r\n" % logdata.data[dataindex]
                dataindex += 1
                return_data += "INFORMATIONAL EXCEPTION ADDITIONAL SENSE CODE QUALIFIER %02X\r\n" % logdata.data[dataindex]
                dataindex += 1
                return_data += "MOST RECENT TEMPERATURE READING %d%%C\r\n" % logdata.data[dataindex]
                dataindex += 1
                return_data += "Vendor specific:\r\n"    
                while(dataindex <= maxparamcount):
                    return_data += "%02X " % logdata.data[dataindex]
                    dataindex += 1
                #dataindex += 1
                return_data += "\r\n"
#                return_data += "index %d\r\n" % dataindex
            elif(paramcode >= 0x0001):
                if(paramcode == 0x0001):
                    return_data += "===Raw read error rate ===\r\n"
                elif(paramcode == 0x0005):
                    return_data += "===Reallocated block count ===\r\n"
                elif(paramcode == 0x0009):
                    return_data += "===Power-on hours count===\r\n"
                elif(paramcode == 0x000C):
                    return_data += "===Power cycle count===\r\n"
                elif(paramcode == 0x000D):
                    return_data += "===ECC rate===\r\n"
                elif(paramcode == 0x00AF):
                    return_data += "===Program fail count (by chip)===\r\n"
                elif(paramcode == 0x00B0):
                    return_data += "===Erase fail count (by chip)===\r\n"
                elif(paramcode == 0x00B1):
                    return_data += "===Wear leveling (total)===\r\n"
                elif(paramcode == 0x00B2):
                    return_data += "===Used reserved block count (by chip)===\r\n"
                elif(paramcode == 0x00B3):
                    return_data += "===Used reserved block count (total)===\r\n"
                elif(paramcode == 0x00B4):
                    return_data += "===Unused Reserved block count (total)===\r\n"
                elif(paramcode == 0x00B6):
                    return_data += "===Erase fail count (total)===\r\n"
                elif(paramcode == 0x00B7):
                    return_data += "===Hardware fail count (by chip)===\r\n"
                elif(paramcode == 0x00C2):
                    return_data += "===Drive case temperature===\r\n"
                elif(paramcode == 0x00C3):
                    return_data += "===Uncorrectable error count===\r\n"
                elif(paramcode == 0x00C6):
                    return_data += "===Offline scan uncorrectable sector count===\r\n"
                elif(paramcode == 0x00C7):
                    return_data += "===Offline scan uncorrectable sector count===\r\n"
                elif(paramcode == 0x00C9):
                    return_data += "===Volatile Memory Backup Source failure===\r\n"
                elif(paramcode == 0x00CA):
                    return_data += "===Exception Mode Status (Read Only Mode)===\r\n"
                elif(paramcode == 0x00E8):
                    return_data += "===Unused reserved block count (by chip)===\r\n"
                elif(paramcode == 0x00E9):
                    return_data += "===Number of write count ===\r\n"
                elif(paramcode == 0x00F0):
                    return_data += "===Link Error Event===\r\n"
                else:
                    return_data += "===UNKNOWN===\r\n"
                return_data += "Parameter Code Decimal:%d Hex:%04X\r\n" % (paramcode, paramcode)
                dataindex += 1
                return_data += "DATA CODE %02X\r\n" % logdata.data[dataindex]
                dataindex += 1
                paramlength = logdata.data[dataindex]
                
#                return_data += "param length %d\r\n" % paramlength
#                return_data += "index %d\r\n" % dataindex
                maxparamcount = dataindex + paramlength
#                return_data += "maxparamcount = %d\r\n" % maxparamcount
                dataindex += 1
                return_data += "PARAM VALUE DATA CODE %02X\r\n" % logdata.data[dataindex]
                dataindex += 1
#                return_data += "index %d\r\n" % dataindex
#                return_data += "maxparamcount = %d\r\n" % maxparamcount
                return_data += returnparsedbuffer(logdata.data[dataindex: (maxparamcount + 1)])
                dataindex = maxparamcount + 1
                return_data += "\r\n"
#                return_data += "index %d\r\n" % dataindex
                
            else:
                 dataindex = pagelength + 1
#            return_data += "\r\n"                     
#            return_data += "Data index %d" % dataindex
#            return_data += "\r\n"                                
        return_data += "\r\n"            
    return_data += returnParsedData(logdata)
    return return_data

def returndefectglist(pd):
        scsi_params = scsi.SCSI_PARAMS()
        scsi_params.op_code = sd.SCSI_READ_DFCT_DATA_10
        ret, scsi_pt = pd.create_scsi_passthru(scsi_params)
        if ret:
            return "Failed create passthru"
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = False)
        if ret:
            return "Failed sending passthru"
        else:
            return scsi_pt    

def returnmodedata(pd, modepage, subpage = 0):
        scsi_params = scsi.SCSI_PARAMS()
        scsi_params.op_code = sd.SCSI_MODE_SENSE_10
        scsi_params.page_code = modepage
        scsi_params.subpage_code = subpage
        ret, scsi_pt = pd.create_scsi_passthru(scsi_params)
        if ret:
            return "Failed create passthru"
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = False)
        if ret:
            return "Failed sending passthru"
        else:
            return scsi_pt    

def returnInquiryData(pd):
    scsi_params = scsi.SCSI_PARAMS()
    scsi_params.op_code = sd.SCSI_INQUIRY
    ret, scsi_pt = pd.create_scsi_passthru(scsi_params)
    if ret:
        return "Failed create passthru"
    ret = pd.send_scsi_passthru(scsi_pt, print_flag = False)
    if ret:
        return "Failed sending passthru"
    return scsi_pt


def returnParsedData(data):
    
    dataindex = 0
    columncount = 0
    return_data = ""
    return_data_row = ""
    return_char_row = ""
    bytetext = ""
    bytetext = ("BYTE %04d:" % dataindex)
    #columncount += 1
    while(dataindex < data.data_length):
        
        if(columncount == 8):
            return_data += ("%s\t%s\t%s\r\n" % (bytetext, return_data_row, return_char_row))
            return_char_row = ""
            return_data_row = ""
            bytetext = ("BYTE %04d:" % dataindex)
            columncount = 0

        if ((data.data[dataindex] >= 0x20) and (data.data[dataindex] < 0x7F)):
            return_char_row += ("%c" % data.data[dataindex])
        else:
            return_char_row += "."  # eliminate non-printable characters            
        return_data_row += ("%02X " % data.data[dataindex])
            
        dataindex += 1
        columncount += 1
    if(columncount <= 7):
        if(columncount < 3):
            return_data_row += "\t\t" #% 0x23 #add filler
        if(columncount > 3 and columncount < 6):
            return_data_row += "\t" #% 0x23 #add filler
    return_data += "%s\t%s\t%s\r\n" % (bytetext, return_data_row, return_char_row)

    return return_data


def returnparsedbuffer(data):
    
    dataindex = 0
    columncount = 0
    return_data = ""
    return_data_row = ""
    return_char_row = ""
    bytetext = ""
    bytetext = ("BYTE %04d:" % dataindex)
    #columncount += 1
    while(dataindex < len(data)):
        
        if(columncount == 8):
            return_data += ("%s\t%s\t%s\r\n" % (bytetext, return_data_row, return_char_row))
            return_char_row = ""
            return_data_row = ""
            bytetext = ("BYTE %04d:" % dataindex)
            columncount = 0

        if ((data[dataindex] >= 0x20) and (data[dataindex] < 0x7F)):
            return_char_row += ("%c" % data[dataindex])
        else:
            return_char_row += "."  # eliminate non-printable characters            
        return_data_row += ("%02X " % data[dataindex])
            
        dataindex += 1
        columncount += 1
    if(columncount <= 7):
        if(columncount < 3):
            return_data_row += "\t\t" #% 0x23 #add filler
        if(columncount > 3 and columncount < 6):
            return_data_row += "\t" #% 0x23 #add filler
    return_data += "%s\t%s\t%s\r\n" % (bytetext, return_data_row, return_char_row)

    return return_data



def returnVendorName(data):
    inquiry = sd.SCSI_INQUIRY_DATA()    
    memmove(addressof(inquiry), addressof(data.data), 40)
    vendor_name = create_string_buffer(sizeof(inquiry.vendor_id))
    memmove(vendor_name, inquiry.vendor_id, 8)

    return vendor_name.value   

def convertBufToChar(buf):
    returnbuf = ""
    for j in range(0, len(buf)):
        if ((buf[j] >= 0x20) and (buf[j] < 0x7F)):
            returnbuf += "%c" % buf[j]
        else:
            returnbuf += "."  # eliminate non-printable characters
    return returnbuf      

def returnSerialNumber(item):
        #**************** GET SERIAL NUMBER
        scsi_params = scsi.SCSI_PARAMS()
        scsi_params.op_code = sd.SCSI_INQUIRY
        scsi_params.page_code = 0x80
        ret, scsi_pt = item.create_scsi_passthru(scsi_params)
        if ret:
            sys.exit(1)
        ret = item.send_scsi_passthru(scsi_pt, print_flag = False)
        if ret:
            sys.exit(1)
        serialnumberbuf = scsi_pt.data[4:scsi_pt.data_length]

#        convertbuffer = convertdata.convertdata()
        pdserialnumber = convertBufToChar(serialnumberbuf)                    
        
        return pdserialnumber

def returnControllerData(ctrl):
    """
    Get controller info into string
    """
    displaycontrollerinfo = ("Controller Name:%s\r\nFirmware Version:%s\r\n" % (ctrl.info.product_name,
                                  ctrl.info.fw_version))
    displaycontrollerinfo += "Enclosures\r\n"
    for encl in ctrl.config.config_mgr.encl_list:
        displaycontrollerinfo += "%-11s%-12s%-12s%-12s\r\n" % (encl.name, 
                                    encl.inquiry.product_id, encl.inquiry.product_rev_level, 
                                    encl.status)
    displaycontrollerinfo += "Physical Disks\r\n"
    for pd in ctrl.config.config_mgr.pd_list:
        displaycontrollerinfo += "%-11s\t%-7s\t%-10s\t%-10s\t%-20s\r\n" % (pd.name, pd.device_id,
                                    (pd.size / defs.ONE_GB), pd.pd_type, pd.state)
    displaycontrollerinfo += "Virtual Disks\r\n"
    for vd in ctrl.config.config_mgr.vd_list:
        size_str = "%-.2f" % (float(vd.size) / (1024 * 1024 * 1024))
        displaycontrollerinfo += "%-11s%-6s%-10s%-10s%-12s%-20s\r\n" % (vd.target_id, vd.raid,
                                    size_str, vd.pd_type, vd.os_disk_name, vd.state)
    
    return displaycontrollerinfo
    
def hextonum(bytestrnum):
    
    return scsi.xtonum(bytestrnum)

def shiftbytes(data, size):
    maxcapacitybytes = size
    returndata = 0
    i = 0
    while(i <= maxcapacitybytes):
        returndata |= data[i] << (8*(maxcapacitybytes-i))
        i += 1
    return returndata
    

def combinecapacitybytes(pd):
    scsi_params = scsi.SCSI_PARAMS()
    scsi_params.op_code = sd.SCSI_READ_CAPACITY_10
    ret, scsi_pt = pd.create_scsi_passthru(scsi_params)
    if ret:
        sys.exit(1)

    ret = pd.send_scsi_passthru(scsi_pt, print_flag = False)
    maxcapacitybytes = 3
    capacity_value = 0
    i = 0
    while(i <= maxcapacitybytes):
        capacity_value |= (scsi_pt.data[i] << (8*(maxcapacitybytes-i)))
        i += 1
    if ret:
        sys.exit(1)
    return capacity_value

def combinesasaddress(pd):
    
    maxcapacitybytes = pd.sas_address.count
    sasaddress = 0
    i = 0
    while(i <= maxcapacitybytes):
        sasaddress |= (pd.sas_address[i] << (8*(maxcapacitybytes-i)))
        i += 1
    if ret:
        sys.exit(1)
    return sasaddress

def get_supported_log_pages(pd, pagecode = 0):
    """Used to store a list of SCSI log pages supported by the drive."""
    ret = 0
    #params = scsi.SCSI_PARAMS()
    #params.op_code = sd.SCSI_LOG_SENSE
    #params.page_code = pagecode
    #ret, scsi_pt = pd.create_scsi_passthru(params)
    fileb = open('dell_checkin_file.txt','w')

    params_s = sd.SCSI_INQUIRY_INPUTS()
	
    params_s.page_code = 0xDC  # the drive will dump all supported pages
    params_s.subpage_code = 0xFF
	#params_s.page_code = 0xDC  # the drive will dump all supported pages
    
    params_s.evpd = 1
    params_s.data_length = 338
    ret_t, scsi_pt = pd.create_scsi_passthru(params_s)
    if ret_t:
	return ret_t
    ret_t = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
    if ret_t:    
	return ret_t
    fileb.close()
        
    if ret:
        return "damn it!"
    return "Passed"
    """
    ret = pd.send_scsi_passthru(scsi_pt, print_flag = False)
    if ret:
        return ret
    pd._spc_props.supported_log_pages = scsi_pt.data[5 : scsi_pt.data_length]
    return ret
    """
    
def getmodepages(object, mode_page_type):
    """Used to dump get suppored mode pages pd, dellinq_file, page_code"""
    ret = 0
    
    params = scsi.SCSI_PARAMS()
    params.op_code = sd.SCSI_MODE_SENSE_10
    params.page_code = 0x3f  # the drive will dump all supported pages
    params.subpage_code = 0xFF
    params.mode_page_type = mode_page_type
    ret, scsi_pt = object.create_scsi_passthru(params, print_flag = False)
    if ret:
        return ret
    ret = object.send_scsi_passthru(scsi_pt, print_flag = False)
    if ret:
        return ret

    # The data field contains all mode page data.
    # Separate and print the data for each mode page.
    page_code_mask = 0x3f
    spfbit_mask = 0x40
    
    i = 8
    #dataparse = ""
    #datastring = ""
    supportedmodepages = []
    passbit = 0
    while(i < scsi_pt.data_length - 1):

        page_code = scsi_pt.data[i] & page_code_mask
        spf_bit = scsi_pt.data[i] & spfbit_mask
        if passbit:
            passbit = 0
            page_length = 1
            i += page_length + 1
        elif spf_bit:
            subpage_code = scsi_pt.data[i + 1]
            page_length = ((scsi_pt.data[i + 2] << 8) | scsi_pt.data[i + 3]) + 1
            supportedmodepages.append("Mode Page 0x%02X SubPage 0x%02X" % (page_code, subpage_code))
            #_log(INFO, "Mode page 0x%02x Subpage 0x%02X: %04x" % (page_code, subpage_code, page_length))
            i += page_length + 1
            passbit = 1
        else:
            page_length = scsi_pt.data[i + 1] + 1
            supportedmodepages.append("Mode Page 0x%02X" % page_code)    
            #_log(INFO, "Mode page 0x%02x: %x" % (page_code, page_length))
#            scsi.hex_dump(scsi_pt.data[i : i + page_length + 1],
#                     page_length + 1)
            i += page_length + 1

    return ret, supportedmodepages
   
 
def getsupportedmodepages(pd, dellinq_file, page_code, subpage_code):
    """Used to dump get suppored mode pages"""
    
    
    """params = scsi.SCSI_PARAMS()
    params.op_code = sd.SCSI_MODE_SENSE_10
    params.page_code = 0x3f  # the drive will dump all supported pages
    params.subpage_code = 0xFF
    params.mode_page_type = mode_page_type"""
    
    
    ret = 0
    fileb = open(dellinq_file,'w')
    params_s = sd.SCSI_INQUIRY_INPUTS()	
    params_s.page_code = eval(page_code)  # the drive will dump all supported pages
    if eval(page_code) == 0x19:
        params_s.subpage_code = 0x01
    elif eval(page_code) == 0x1C:
        params_s.subpage_code = 0x01
        
    #params_s.page_code = 0xDC  # the drive will dump all supported pages    
    params_s.evpd = 1
    params_s.data_length = 338
    ret_t, scsi_pt = pd.create_scsi_passthru(params_s)
    #if ret_t:
    #	return ret_t
    ret_t = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
    if ret_t:    
    	return ret_t
    #print ret_t
    fileb.close()

    # The data field contains all mode page data. 
    # Separate and print the data for each mode page.
    #page_code_mask = 0x3f
    #spfbit_mask = 0x40	
    #i = 8
    #dataparse = ""
    #datastring = ""
    #supportedmodepages = []
    #passbit = 0
    #while(i < scsi_pt.data_length - 1):
    
    #	page_code = scsi_pt.data[i] & page_code_mask
    #	spf_bit = scsi_pt.data[i] & spfbit_mask
    #if passbit:
    #	passbit = 0
    #	page_length = 1
    #	i += page_length + 1
    #elif spf_bit:
    #	subpage_code = scsi_pt.data[i + 1]
    #	page_length = ((scsi_pt.data[i + 2] << 8) | scsi_pt.data[i + 3]) + 1
    #	supportedmodepages.append("Mode Page 0x%02X SubPage 0x%02X" % (page_code, subpage_code))
    #	#_log(INFO, "Mode page 0x%02x Subpage 0x%02X: %04x" % (page_code, subpage_code, page_length))
    #	i += page_length + 1
    #	passbit = 1
    #else:
    #	page_length = scsi_pt.data[i + 1] + 1
    #	supportedmodepages.append("Mode Page 0x%02X" % page_code)    
    #	#_log(INFO, "Mode page 0x%02x: %x" % (page_code, page_length))
    #	#            scsi.hex_dump(scsi_pt.data[i : i + page_length + 1],
    #	#                     page_length + 1)
    #	i += page_length + 1
    #return ret_t
    #return ret_t, supportedmodepages
       

def file_name_builder(pd, mode_page):
    ret, size = pd.get_read_capacity()
    if ret:
        return ret

    if size > 10**12:
        size_str = str(size / 10**12) + "TB"
    else:
        size_str = str(size / 10**9) + "GB"

    # Fill in SCSI info for this disk, particularly the Serial Number.
    ret = pd.init_scsi_attributes()
    if ret:
        return ret

    serial_number = re.sub("\s+", "", pd.spc_props.unit_serial_number)
        
    vendor = re.sub("\s+", "", pd.inquiry.vendor_id)
    model = re.sub("\s+", "", pd.inquiry.product_id)
    hdd_name = model_map.get(model)
    if hdd_name is None:
        hdd_name = model
    hdd_name = re.sub("\s+", "_", hdd_name)
    fw_version = re.sub("\s+", "", pd.inquiry.product_rev_level)
    #sys_name, model_name, service_tag = _get_sys_info()
        
    #ctrl_name = re.sub(" ", "-", ctrl.info.product_name)
    type = pd.pd_type
    date = time.strftime("%m%d%y%H%M%S")
    if mode_page == '0xC0':
        mode = '0xC0_Saved'
        dellinq_file = "%s_%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number,mode)   
    elif mode_page == '0x80':
        mode = '0x80_Default'
        dellinq_file = "%s_%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number,mode) 
    else:
        dellinq_file = "%s_%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number,mode_page)   
        
    return dellinq_file

def drive_inquiry(page,subpage):
    inquiry=[]
    controllers = inventory.ctrl_list
    for ctrl in controllers: #inventory.ctrl_list:
        pd_list = ctrl.config.config_mgr.pd_list
        
        for pd in pd_list:
            #if(pd.pd_type == "SAS"):
	    dellinq_file = file_name_builder(pd, page)
            #print get_supported_log_pages(pd, 0xff)
	    getsupportedmodepages(pd, dellinq_file, page, subpage)
	    inquiry.append(dellinq_file)
	    #print dellinq_file
    return inquiry

def main():
#    """
#        Vendor Specific Mode Page (00h)	Uncorrectable Error Autoreallocation (UEAR, byte 2, bit 0) = 1b
#        Read-Write Error Recovery Mode Page (01h)
#                Automatic Write Reallocation Enabled (AWRE, byte 2, bit 7) = 1b
#                Automatic Read Reallocation Enabled (ARRE, byte 2, bit 6) = 1b
#                Transfer Block (TB, byte 2, bit 5) = 0b
#                Enable Early Recovery (EER, byte 2, bit 3) = 0b
#                Post Error (PER, byte 2, bit 2) = 0b
#                Recovery Time Limit (RTL, bytes 10 and 11) = 1F40h (8 seconds).
#                
#        Verify Error Recovery Mode Page (07h)
#                Enable Early Recovery (EER, byte 2, bit 3) = 0b
#                Post Error (PER, byte 2, bit 2) = 0b
#                Verify Recovery Time Limit (bytes 10 and 11) = 1F40h (8 seconds).
#                
#        Caching Mode Page (08h)
#                HDD: Write Cache Enable (WCE, byte 2, bit 2) = 0b
#                SSD: Write Cache Enable (WCE, byte 2, bit 2) = 0b
#
#
#        Control Mode Page (0Ah)
#                Global Logging Target Save Disable (GLTSD, byte 2, bit 1) = 0b
#
#        Protocol-Specific Logical Unit Mode Page for SAS SSP (18h)
#                TRANSPORT LAYER RETRIES (byte 2, bit 4) = 0b
#
#                
#	Protocol-Specific Port Mode Page for SAS SSP (19h)
#                READY LED MEANING (byte 2, bit 4) = 1b 
#                BROADCAST ASYNCHRONOUS EVENT (byte 2, bit 5) = 0b
#                CONTINUE AWT (byte 2, bit 6) = 1b
#                I_T NEXUS LOSS TIME (bytes 4 and 5) = 07D0h (2 seconds)
#                INITIATOR RESPONSE TIMEOUT (bytes 6 and 7) = 2710h (10 seconds) 
#
#
#        Power Condition Mode Page (1Ah)
#                Drives shall support the version of this page with a page length of 0Ah
#
#	Phy Control and Discover (19h, subpage 01h)
#                Table 11 shows the default settings for the Programmed Minimum Physical Link Rate and Programmed
#                Maximum Physical Link Rate fields in the SAS Phy Mode descriptors.
#
#        Background Control Mode Page (1Ch, subpage 01h)
#                This section applies to HDD and, optionally, SSD. SSD will require timer values to be mutually established with Dell.
#                Enable BMS (EN_BMS, byte 4, bit 0) = 1b
#                Suspend on Log Full (S_L_FULL, byte 4, bit 1) = 0b
#                Log Only When Intervention Required (LOWIR, byte 4, bit 2) = 0b
#                Enable Pre-scan (EN_PS, byte 5, bit 0) = 0b
#                BMS Interval Time (bytes 6?7) = 0150h (336 hours)
#                Minimum Idle Time Before Background Scan (bytes 10?11) = 00FAh (250 ms)
#
#        Log Page 00h 02h 03h 05h 06h 0Dh 0Fh 10h 15h 18h 1Ah 2Fh
#    """
    cmd_list=['0x00', '0x01', '0x07', '0x08', '0x0A', '0x18', '0x19', '0x1A', '0x1C']
    log_pages = ['0x00', '0x02', '0x03', '0x05', '0x06', '0x0D', '0x0F', '0x10', '0x15', '0x18', '0x1A', '0x2F']
    for p in cmd_list:        
        var = drive_inquiry(p,0xFF)
    return var
if __name__ == "__main__":
    main()
#def main():
#    drive_inquiry()
    
    #controllers = inventory.ctrl_list

    #for ctrl in controllers: #inventory.ctrl_list:
    #    pd_list = ctrl.config.config_mgr.pd_list
        
    #    for pd in pd_list:
            #if(pd.pd_type == "SAS"):
    #        print get_supported_log_pages(pd, 0xff)
    #    getsupportedmodepages(pd, dellinq_file)
    #        """
    #        if(get_supported_log_pages(pd, 0xff)):
    #            print "Failed"
    #        else:
    #            print "***************************************"
    #            for page in pd._spc_props.supported_log_pages:
    #                print "%x " % page
    #        """        
                


