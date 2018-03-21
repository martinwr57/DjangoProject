#!/usr/bin/env python

import psutil
import os

pidlist = []
proclist = psutil.get_process_list()
for proc in proclist:
    # print proc.pid
    # print proc.cmdline
    itspy = False
    itssv = False
    for elem in proc.cmdline:
        if 'python' in elem.lower():
	    print proc.pid, proc.cmdline
	    itspy = True
    for elem in proc.cmdline:
        if 'remote_server_db' in elem.lower(): itssv = True
        if 'manage.py' in elem.lower(): itssv = True
        if 'explorer.exe' in elem.lower(): itssv = True

    if itspy and itssv: pidlist.append(proc.pid)

for pid in pidlist:
    psutil.Process(pid).terminate()


os.system('start /min python /python26/lib/site-packages\
/testautomation/remote_server_db.py')
os.system('start /min python /dashboard/manage.py runserver')
os.system('start explorer http://localhost:8000/admin')
