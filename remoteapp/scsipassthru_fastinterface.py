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

from remoteapp.scsi_output_preprocess import hex_dump
import SimpleXMLRPCServer
import xmlrpclib
import remote_client_db

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

def get_supported_log_pages(pd, pagecode = 0):
    """Used to store a list of SCSI log pages supported by the drive."""
    ret = 0
    
    fileb = open('dellinq_file.txt','w')

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
    
    
 
def getsupportedmodepages(pd, dellinq_file):
    """Used to dump get suppored mode pages"""
    ret = 0    
    fileb = open(dellinq_file,'w')
    params_s = sd.SCSI_INQUIRY_INPUTS()	
    params_s.page_code = 0xDC  # the drive will dump all supported pages
    params_s.subpage_code = 0xFF
    params_s.evpd = 1
    params_s.data_length = 338
    ret_t, scsi_pt = pd.create_scsi_passthru(params_s)
    serial_number = re.sub("\s+", "", pd.spc_props.unit_serial_number)

    #ret_t = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
    ret_t = pd.send_scsi_passthru(scsi_pt, print_flag = True)
    data = hex_dump(scsi_pt.data, scsi_pt.data_length, fileb)

    
    #server = xmlrpclib.ServerProxy("http://dashboard.hdd.lab:1332", allow_none=True)
    #server.setInquiryData(ret_t, serial_number)
    fileb.close()
    return data
  


def file_name_builder(pd):
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
    if pd.os_disk_name:
        dellinq_file = "%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number)   
	    
        return dellinq_file
    else:
        return 0
def drive_inquiry():
    inquiry=[]
    output ={}
    controllers = inventory.ctrl_list
    for ctrl in controllers: #inventory.ctrl_list:
        pd_list = ctrl.config.config_mgr.pd_list
        
        for pd in pd_list:
            #if(pd.pd_type == "SAS"):
            #if len(serial_namber) == 8:

	    dellinq_file = file_name_builder(pd)
            if dellinq_file:
                serial_number = pd.spc_props.unit_serial_number
                data = getsupportedmodepages(pd, dellinq_file)
                output[serial_number] = data
                inquiry.append(dellinq_file)
    #print output
    #thread.start_new_thread(remote_client_db.check_in, ('Inquiry', output, 'CheckIn', 100))
    remote_client_db.checkin('Inquiry', output)

    #return output

def main():
    var = drive_inquiry()
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
                


