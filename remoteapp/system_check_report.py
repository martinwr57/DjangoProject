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
from sqlalchemy import create_engine
from sqlalchemy import sql, schema, types, exc, pool
from sqlalchemy import Table, Integer, Sequence, Column, String, MetaData
from sqlalchemy.orm import sessionmaker


#engine = create_engine('mssql+pyodbc://@DATABASE\SQLEXPRESS/RADatabase')
engine = create_engine('mssql+pyodbc://@DATABASE\AUTOMATION/Automation')
connection = engine.connect()
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
NAME = os.environ['COMPUTERNAME']
DOMAIN = os.environ['USERDNSDOMAIN']
server_name = '.'.join((NAME, DOMAIN))


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



#*********** Load Inventory ***********************************
inventory = fast.Inventory()


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
        #displaycontrollerinfo += "%-11s\t%-7s\t%-10s\t%-10s\t%-20s\r\n" % (pd.name, pd.device_id,
        #                            (pd.size / defs.ONE_GB), pd.pd_type, pd.state)
	
        displaycontrollerinfo += get_devices(pd)[0]
	d = get_devices(pd)
	data = d[1]
	
    displaycontrollerinfo += "Virtual Disks\r\n"
    for vd in ctrl.config.config_mgr.vd_list:
        size_str = "%-.2f" % (float(vd.size) / (1024 * 1024 * 1024))
        displaycontrollerinfo += "%-11s%-6s%-10s%-10s%-12s%-20s\r\n" % (vd.target_id, vd.raid,
                                    size_str, vd.pd_type, vd.os_disk_name, vd.state)
    
    info = [displaycontrollerinfo, data]
    return info

def get_supported_log_pages(pd, pagecode = 0):
    """Used to store a list of SCSI log pages supported by the drive."""
    ret = 0
    #params = scsi.SCSI_PARAMS()
    #params.op_code = sd.SCSI_LOG_SENSE
    #params.page_code = pagecode
    #ret, scsi_pt = pd.create_scsi_passthru(params)
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
    print ret_t
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
    #params_s.page_code = 0xDC  # the drive will dump all supported pages    
    params_s.evpd = 1
    params_s.data_length = 338
    ret_t, scsi_pt = pd.create_scsi_passthru(params_s)
    #if ret_t:
    #	return ret_t
    ret_t = pd.send_scsi_passthru(scsi_pt, print_flag = True, fp = fileb)
    #if ret_t:    
    #	return ret_t
    #print ret_t
    fileb.close()
    #transmitOne(file_path, port=1331,address='hddlab.hdd.lab')

    #thread.start_new_thread(running, (results, "thread-2", 5)) 
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
       

def get_devices(pd):
    data={}
    ret, size = pd.get_read_capacity()
    #print dir(pd)
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
    
    location = ''.join(('PHYSICALDRIVE:',str(pd.os_disk_name)))
    #ctrl_name = re.sub(" ", "-", ctrl.info.product_name)
    type = pd.pd_type
    data = {'MemoryType': pd.media_type, 'CodeName':hdd_name, 'Manufacturer':vendor, 'InterfaceType': type, 'WindowsLocation':location,
	'InterfaceSpeed': 6,'Capacity':size_str,'ModelNumber':model,'SerialNumber':serial_number,'Firmware':fw_version}
		
    #product = "%s_%s_%s_%s_%s_%s" % (vendor, hdd_name,size_str, type, serial_number, fw_version)
    product = "%-11s\t%-7s\t%-10s\t%-5s\t%-10s\t%-5s\r\n" % (vendor, hdd_name,size_str, type, serial_number, fw_version)   

	    
    return product, data

def drive_inquiry():
    inquiry=[]
    controllers = inventory.ctrl_list
    for ctrl in controllers: #inventory.ctrl_list:
        pd_list = ctrl.config.config_mgr.pd_list
        
        for pd in pd_list:
            #if(pd.pd_type == "SAS"):
	    dellinq_file = file_name_builder(pd)
            #print get_supported_log_pages(pd, 0xff)
	    getsupportedmodepages(pd, dellinq_file)
	    inquiry.append(dellinq_file)
	    #print dellinq_file
    return inquiry

def enter_device(data, name, sleeptime):
    drive_info = data
    #print data
    drive = Table('Device', metadata, autoload=True)
    info ={}
    #s = drive.select((drive.columns.ModelNumber != drive_info['ModelNumber']) & (drive.columns.SerialNumber != drive_info['SerialNumber']) )
    s = drive.select(drive.columns.SerialNumber == drive_info['SerialNumber'])

    val = connection.execute(s)
    print val.rowcount
    if val.rowcount == 0:
	for d in drive.columns:
		col = str(d).split('.')[1]
		if col in drive_info.keys():		
			info[col]=str(drive_info[col]).strip()	
		if col == 'Shipping':		
			info[col]=0    
		if col == 'SupportDUP':		
			info[col]=0

	  
	try:
	    i = drive.insert()
	    i.execute(info)  
	    print 'device....', info
	except Exception:
	    print 'Entry not made'
	    pass
    else:
	driverev = Table('DeviceRev', metadata, autoload=True)
	info.clear()
	s = driverev.select((driverev.columns.ModelNumber == drive_info['ModelNumber']) & (driverev.columns.FWRev != drive_info['Firmware']))

	#s = driverev.select(driverev.columns.FWRev != drive_info['Firmware'])
	val = connection.execute(s)
	print val.rowcount
	if val.rowcount:
	    try: 
		info = {'ModelNumber':drive_info['ModelNumber'], 'FWRev':drive_info['Firmware']}
		i = driverev.insert()
		i.execute(info)
		#print 'device.... revision'
	    except Exception:
		print 'Entry not made'
		pass
    time.sleep(sleeptime) 


def main():
    #var = drive_inquiry()
    config=''
    controllers = inventory.ctrl_list
    #data={}
    for ctrl in controllers:
	var = returnControllerData(ctrl)
	
	for pd in ctrl.config.config_mgr.pd_list:
	    d = get_devices(pd)
	    print d[1]
	    thread.start_new_thread(enter_device, (d[1], "thread-1", 5)) 

	#data = var[1]
	config = config + var[0] + '\r\n'
	#enter_device(data)
	#thread.start_new_thread(enter_device, (data, "thread-1", 5)) 

	#for p in pd_list:
	#     drive = get_devices(p)
	#     print '-----',drive

	
    system = Table('Systems', metadata, autoload=True)
    s = system.select((system.columns.NetworkID == server_name) & (system.columns.SystemName == NAME))
    val = s.execute()
    print val.rowcount
    if val.rowcount == -1:
	#row = rs.fetchone()
	#system_name = row['SystemName']
	#OS = row['OS']
	#address = row['NetworkID']
	#print OS, system_name, address
	input = {'Configuration':config}
	ss = system.update(whereclause=(((system.columns.NetworkID == server_name) & (system.columns.SystemName == NAME))), values=input )
	ss.execute()
	
	
    #return var
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
                


