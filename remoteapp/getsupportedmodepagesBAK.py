#!/usr/bin/env python
"""This is a module is to support the module Big Bird
    by returning a list of controllers and devices
"""
__author__ = "Bob Clausen"
__date__ = "10-10-2009"
__version__ = '1.0'

import os
import sys
import time
from ctypes import *
import re
import threading, thread
#**************FAST API IMPORTS***************************
import fast
import fast.defs as defs
import fast.scsi.scsi as scsi
import fast.scsi.scsi_defs as sd

import convertdata
#import scsipassthru_checkIn as check
DBUG = fast.log.DBUG
INFO = fast.log.INFO
WARN = fast.log.WARN
CRIT = fast.log.CRIT

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
#fast.log.write(DBUG, "BigBird CLI Version = %s" % __version__, LOG_PREFIX)
inventory = fast.Inventory()

def getmodepages(pd, dellinq_file, mode_page_type):
    """Used to dump get suppored mode pages"""
    print dellinq_file, mode_page_type
    new_file = '\\'.join(('mode_pages', dellinq_file))
    ret = 0
    fileb = open(new_file,'w')
    
    if mode_page_type == 0x00:   
        params = sd.SCSI_INQUIRY_INPUTS()
        params = sd.SCSI_MODE_SENSE_6_INPUTS()    
        params.mode_page_type = 0x00
        params.page_code = 0x00 # the drive will dump all supported pages 
        #params.subpage_code = 0x00         
        params.data_length = 24
        params.evpd = 1
        ret, scsi_pt = pd.create_scsi_passthru(params)
        if ret:
            return ret
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
        if ret:
            return ret
        
    
    elif mode_page_type == 0x01:   
        params = sd.SCSI_INQUIRY_INPUTS()
        params = sd.SCSI_MODE_SENSE_6_INPUTS()        
        #params.op_code = sd.SCSI_MODE_SENSE_6 
        params.mode_page_type = 0x01
        params.page_code = 0x00  # the drive will dump all supported pages   
        #params.subpage_code = 0x00
        params.data_length = 24
        params.evpd = 1       
        
        ret, scsi_pt = pd.create_scsi_passthru(params)
        if ret:
            return ret
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
        if ret:
            return ret
        
    
    elif mode_page_type == 0x07:
        params = sd.SCSI_INQUIRY_INPUTS() 
        params = sd.SCSI_MODE_SENSE_6_INPUTS()        
        #params.op_code = sd.SCSI_MODE_SENSE_6 
        params.mode_page_type = 0x07
        params.page_code = 0x00  # the drive will dump all supported pages   
        #params.subpage_code = 0x01
        params.data_length = 24
        ret, scsi_pt = pd.create_scsi_passthru(params)
        if ret:
            
            return ret
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
        if ret:
            return ret
        
        
    
    elif mode_page_type == 0x08:
        #params = sd.SCSI_INQUIRY_INPUTS()
        params = sd.SCSI_MODE_SENSE_6_INPUTS()
        params.page_code = 0x08  # the drive will dump all supported pages    
        params.subpage_code = 0x00       
        params.data_length = 24
        params.evpd = 1
        ret, scsi_pt = pd.create_scsi_passthru(params)
        if ret:
            return ret
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
        if ret:
            return ret
        
        
    
    elif mode_page_type == 0x0A:
        params = sd.SCSI_INQUIRY_INPUTS()
        params = sd.SCSI_MODE_SENSE_6_INPUTS()   
        params.page_code = 0x0A  # the drive will dump all supported pages   
        params.subpage_code = 0x00       
        params.data_length = 32
        params.evpd = 1
        ret, scsi_pt = pd.create_scsi_passthru(params)
        if ret:
            return ret
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
        if ret:
            return ret
        
        
    
    elif mode_page_type == 0x1A:
        params = sd.SCSI_INQUIRY_INPUTS()
        params = sd.SCSI_MODE_SENSE_6_INPUTS()    
        params.page_code = 0x1A # the drive will dump all supported pages     
        params.subpage_code = 0x00     
        params.data_length = 32
        params.evpd = 1
        ret, scsi_pt = pd.create_scsi_passthru(params)
        if ret:
            return ret
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
        if ret:
            return ret
        
        
    
    elif mode_page_type == 0x1C:
        params = sd.SCSI_INQUIRY_INPUTS()
        params = sd.SCSI_MODE_SENSE_6_INPUTS()
        params.mode_page_type = 0x1C
        params.page_code = 0x00  # the drive will dump all supported pages
        params.subpage_code = 0x00     
        params.data_length = 32
        params.evpd = 1
        ret, scsi_pt = pd.create_scsi_passthru(params)
        if ret:
            return ret
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
        if ret:
            return ret
        
        
    elif mode_page_type == 0x18:
        params = sd.SCSI_INQUIRY_INPUTS()
        params = sd.SCSI_MODE_SENSE_6_INPUTS()   
        params.page_code = 0x18  # the drive will dump all supported pages   
        params.subpage_code = 0x00       
        params.data_length = 32
        params.evpd = 1
        ret, scsi_pt = pd.create_scsi_passthru(params)
        if ret:
            return ret
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
        if ret:
            return ret
        
        
    elif mode_page_type == 0x19:
        params = sd.SCSI_INQUIRY_INPUTS()
        params = sd.SCSI_MODE_SENSE_6_INPUTS() 
        params.page_code = 0x19  # the drive will dump all supported pages
        params.subpage_code = 0x00      
        params.data_length = 32
        params.evpd = 1
        ret, scsi_pt = pd.create_scsi_passthru(params)
        if ret:
            return ret
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
        if ret:
            return ret
        
        
    elif mode_page_type == 0xC0:
        params = sd.SCSI_INQUIRY_INPUTS()
        #params = sd.SCSI_MODE_SENSE_10_INPUTS()    
        params.page_code = 0xC0  # the drive will dump all supported pages
        #params.page_code = mode_page_type # the drive will dump all supported pages
        params.subpage_code = 0x01      
        params.data_length = 24
        params.evpd = 1
        ret, scsi_pt = pd.create_scsi_passthru(params)
        if ret:
            return ret
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
        if ret:
            return ret
        
        
    elif mode_page_type == 0x80:
        params = sd.SCSI_INQUIRY_INPUTS()   
        params.page_code = 0x80  # the drive will dump all supported pages
        #params.page_code = mode_page_type # the drive will dump all supported pages
        params.subpage_code = 0x01      
        params.data_length = 24
        params.evpd = 1
        ret, scsi_pt = pd.create_scsi_passthru(params)
        if ret:
            return ret
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
        if ret:
            return ret
        
    else:
        
        params = scsi.SCSI_PARAMS()
        params.op_code = sd.SCSI_MODE_SENSE_10
        params.page_code = 0x3f  # the drive will dump all supported pages
        params.subpage_code = 0xFF
        params.mode_page_type = mode_page_type     
        params.data_length = 88
        params.evpd = 1
        ret, scsi_pt = pd.create_scsi_passthru(params)
        if ret:
            return ret
        ret = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
        if ret:
            return ret
        
    
    
    

    fileb.close()
    # The data field contains all mode page data.
    # Separate and print the data for each mode page.
#    page_code_mask = 0x3f
#    spfbit_mask = 0x40
#    
#    i = 8
#    #dataparse = ""
#    #datastring = ""
#    supportedmodepages = []
#    passbit = 0
#    while(i < scsi_pt.data_length - 1):
#
#        page_code = scsi_pt.data[i] & page_code_mask
#        spf_bit = scsi_pt.data[i] & spfbit_mask
#        if passbit:
#            passbit = 0
#            page_length = 1
#            i += page_length + 1
#        elif spf_bit:
#            subpage_code = scsi_pt.data[i + 1]
#            page_length = ((scsi_pt.data[i + 2] << 8) | scsi_pt.data[i + 3]) + 1
#            supportedmodepages.append("Mode Page 0x%02X SubPage 0x%02X" % (page_code, subpage_code))
#            #_log(INFO, "Mode page 0x%02x Subpage 0x%02X: %04x" % (page_code, subpage_code, page_length))
#            i += page_length + 1
#            passbit = 1
#        else:
#            page_length = scsi_pt.data[i + 1] + 1
#            supportedmodepages.append("Mode Page 0x%02X" % page_code)    
#            #_log(INFO, "Mode page 0x%02x: %x" % (page_code, page_length))
##            scsi.hex_dump(scsi_pt.data[i : i + page_length + 1],
##                     page_length + 1)
#            i += page_length + 1

    #return ret, supportedmodepages
    

def name_builder(pd, mode_page):
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

    if mode_page == 0xC0:
        mode = '0xC0_Saved'
        dellinq_file = "%s_%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number,mode)   
    elif mode_page == 0x80:
        mode = '0x80_Default'
        dellinq_file = "%s_%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number,mode) 
    elif mode_page == 0x00:
        mode = '0x00'
        dellinq_file = "%s_%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number,mode)   
    elif mode_page == 0x01:
        mode = '0x01'
        dellinq_file = "%s_%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number,mode)  
    elif mode_page == 0x07:
        mode = '0x07'
        dellinq_file = "%s_%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number,mode)   
    elif mode_page == 0x08:
        mode = '0x08'
        dellinq_file = "%s_%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number,mode)   
    elif mode_page == 0x0A:
        mode = '0x0A'
        dellinq_file = "%s_%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number,mode)   
    elif mode_page == 0x18:
        mode = '0x18'
        dellinq_file = "%s_%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number,mode)   
    elif mode_page == 0x19:
        mode = '0x19'
        dellinq_file = "%s_%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number,mode)   
    elif mode_page == 0x1A:
        mode = '0x1A'
        dellinq_file = "%s_%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number,mode)   
    elif mode_page == 0x1C:
        mode = '0x1C'
        dellinq_file = "%s_%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number,mode) 
    else:
        mode = str(mode_page)
        dellinq_file = "%s_%s_%s_%s_%s.txt" % (vendor, size_str,type, serial_number,mode)  
        
    return dellinq_file

def _log(lvl, msg):
    """ Helper for sending log messages. """
    fast.log.write(lvl, msg, LOG_PREFIX)
    
def main():
    
    cmd_list=[0x00, 0x01, 0x07, 0x08, 0x0A, 0x18, 0x19, 0x1A, 0x1C, 0xC0, 0x80]
    log_pages = ['0x00', '0x02', '0x03', '0x05', '0x06', '0x0D', '0x0F', '0x10', '0x15', '0x18', '0x1A', '0x2F']
    
    controllers = inventory.ctrl_list
    
    for ctrlr in controllers:
        for strdev in ctrlr.config.config_mgr.pd_list:
            #ret, modepages = getsupportedmodepages(strdev)
            print dir(strdev)
            print strdev.pd_type
            if strdev.pd_type == "SAS":
                print "Current"
                for p in cmd_list: 
                    ret, modepages = strdev.get_supported_mode_pages()
                    print p, 'beginning'
                    dellinq_file = name_builder(strdev, p)
                    getmodepages(strdev, dellinq_file, p)
                for modepage in modepages:
                    print modepage
                for p in log_pages:
                    ret, logpages = strdev.get_supported_log_pages()
		    print 'LOGPAGES=', logpages
                #print "Saved"
                #ret, modepages = strdev.get_supported_mode_pages(0xC0)
                #for modepage in modepages:
                #    print modepage
                #print "Default"
                #ret, modepages = strdev.get_supported_mode_pages(0x80)
                #for modepage in modepages:
                #    print modepage

if __name__ == "__main__":
    main()