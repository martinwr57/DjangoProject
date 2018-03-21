from dashboarding.models import Device
from dashboarding.models import Devicerev
from dashboarding.models import Result
from dashboarding.models import Test
from dashboarding.models import Testrev
from dashboarding.models import Testscripts
from dashboarding.models import Systems
from dashboarding.models import Dellinqdata
from dashboarding.models import Codenames
from django.utils.safestring import mark_safe

from django.contrib import admin
# django.contrib.admin.templatetags.admin_list
import re
from subprocess import Popen, PIPE
from threading import Thread
import sys, time, os, os.path
from AutoPerfAnalysis3 import analysis
#from AutoPerfAnalysis import perf_mc
#from TestAutomation.dash_func import load_names, Pinger, PingAgent
import thread
import threading
import xmlrpclib

sep = os.sep
paths = '%s%shddlab%sPerformance_Results%s' % (sep,sep,sep,sep)

      
      
class CodenamesAdmin(admin.ModelAdmin):
    list_display = ('vendor','codename', 'modelnumber')
    search_fields = ('modelnumber', 'vendor','codename')
    list_filter = ('vendor',)    
    list_select_related = True
    
    
    
    def load_codenames(self, request,queryset):
        ld = load_names()
        ld.addcodename()
        message_bit = "for devices"
        self.message_user(request, "Load Code Names %s " % message_bit)
           
 
    def add_marketnames(self, request, queryset):
        ld = load_names()
        ld.update_CodeNames()
        message_bit = "for Results"
        self.message_user(request, "Load Code Names %s " % message_bit)
           
    
    load_codenames.short_description = "Load Drive Code Names"
    add_marketnames.short_description = "Update Code Names"

    actions = [load_codenames, add_marketnames]

class DellinqdataAdmin(admin.ModelAdmin):
    list_display = ('headvendor','formfactorwidth', 'mediumrotationrate', 'productserialnumber', 'productid')
    search_fields = ('productserialnumber', 'headvendor','headdiskassembly', 'dellppid')
    list_filter = ('mediumrotationrate','formfactorwidth','headvendor',)
    
    list_display_links = ('headvendor', 'productserialnumber')
    list_select_related = True
    
    class Media:
        css ={ 'all':("report.css",) }
        js = ("jquery.collapser.js",)
        
        
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('manufacturer','interfacetype', 'firmware','modelnumber', 'serialnumber', 'shipping', 'supportdup', 'report')
    search_fields = ('manufacturer', 'formfactor','interfacetype', 'firmware','capacity','serialnumber')
    list_filter = ('interfacetype','memorytype', 'modelnumber','formfactor','supportdup','shipping',)
    list_select_related = True
    
    
    def ready_toship(self, request,queryset):
        rows_updated = queryset.update(shipping=1)
        if rows_updated == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" % rows_updated
        self.message_user(request, "%s successfully marked as shipped." % message_bit)
        
    def not_shipping(self, request,queryset):
        rows_updated = queryset.update(shipping=0)
        if rows_updated == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" % rows_updated
        self.message_user(request, "%s successfully marked as not shipped." % message_bit)
        
    def dup_support(self, request,queryset):
        rows_updated = queryset.update(supportdup=1)
        if rows_updated == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" % rows_updated
        self.message_user(request, "%s successfully marked as having DUP support." % message_bit)
        
    def nodup_support(self, request,queryset):
        rows_updated = queryset.update(supportdup=0)
        if rows_updated == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" % rows_updated
        self.message_user(request, "%s successfully marked as not having DUP support." % message_bit)       
        
        
        
    ready_toship.short_description = "Mark selected devices to be shipped"
    not_shipping.short_description = "Mark selected devices not being shipped"   
    dup_support.short_description = "Mark selected devices to be DUP supported"
    nodup_support.short_description = "Mark selected devices not supporting DUP" 
    actions = [ready_toship, not_shipping, dup_support, nodup_support]

class ResultAdmin(admin.ModelAdmin):
    search_fields = ('marketname','vendor','capacity','serialnumber', 'modelnumber','testname', 'timestamp', 'formfactor')
    list_display = ('testname','modelnumber','formfactor', 'timestamp')
    list_filter = ('vendor','testname','formfactor','modelnumber',)
    #date_hierarchy = 'timestamp'
    ordering = ('-timestamp','serialnumber')
    
    list_select_related = True
    
    def load_data(self, request,queryset):
        rows_analysis = queryset
        device_list=[]
        for obj in queryset:
            if obj.rawdata:
                cmd = obj.rawdata
                os.system(cmd)
            if obj.reports:
                cmd = obj.reports
                os.system(cmd)
                
        if rows_analysis == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" % rows_analysis
        self.message_user(request, "%s successfully selected." % message_bit)
        
    def analyze_data(self, request,queryset):
        rows_analysis = queryset
        device_list=[]
        for obj in queryset:
            device_list.append(obj.reports)
        f = obj.modelnumber + '_compare.xlsx'
        metrics = os.path.join(paths, f)     
        #d = perf_mc.run(device_list, paths, f)

        if rows_analysis == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" % d
        self.message_user(request, "%s successfully selected and analyzed." % message_bit)
        
        
    
    analyze_data.short_description = "Model Compare"
    load_data.short_description ="Select results to open"
    actions = [analyze_data, load_data]

class TestRevAdmin(admin.ModelAdmin):
    list_display = ('system', 'controller', 'script')
    list_filter = ('system','controller','testname',)
    #date_hierarchy = 'timestamp'
    ordering = ('-controller',)


class TestAdmin(admin.ModelAdmin):
    list_display = ('system', 'controller', 'script')
    list_filter = ('system','controller','testname',)
    #date_hierarchy = 'timestamp'
    ordering = ('-controller',)
    

class TestscriptsAdmin(admin.ModelAdmin):
    search_fields = ('type', 'scriptref','networkid', 'devicetype')
    list_display = ('type', 'duration', 'devicetype','description', 'networkid', 'multidevice')
    list_filter = ('type','devicetype','networkid',)
    #date_hierarchy = 'timestamp'
    ordering = ('duration','type')
    
    def load_script(self, request,queryset):
        rows_analysis = queryset
        device_list=[]
        for obj in queryset:
            if obj.scriptref:
                cmd = obj.scriptref
                os.system(cmd)
                
        if rows_analysis == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" % rows_analysis
        self.message_user(request, "%s successfully selected." % message_bit)
    
    def check_and_script(self, request,queryset):
        rows_analysis = queryset
        script_list=[]
        servers=[]
        postproc = None
        for obj in queryset:
            script_list.append((obj.scriptref).strip())
            script = (obj.scriptref).strip()
            postproc = 1
            print script_list
            server_name = 'http://' +  (obj.networkid).strip() + ':1332'
            print server_name
            server = xmlrpclib.ServerProxy(server_name, allow_none=True)            
            server.drive_checkin('Inquiry')
            thread.start_new_thread(server.run_performance_multi, (script_list, postproc,"thread-2", 20)) 
            #server.run_performance_testing(script_list, postproc)
        
                
        if rows_analysis == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" % rows_analysis
        self.message_user(request, "%s successfully selected and executed." % message_bit)
        
    
    
    def run_script(self, request,queryset):
        rows_analysis = queryset
        script_list=[]
        postproc = None
        for obj in queryset:
            script_list.append((obj.scriptref).strip())
            script = (obj.scriptref).strip()
            postproc = 1
            print script_list
            server_name = 'http://' +  (obj.networkid).strip() + ':1332'
            print server_name
            server = xmlrpclib.ServerProxy(server_name, allow_none=True)            
            thread.start_new_thread(server.run_performance_multi, (script_list, postproc,"thread-2", 20)) 
            #server.run_performance_testing(script_list, postproc)
        if rows_analysis == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" %  rows_analysis
        self.message_user(request, "%s successfully selected and executed." % message_bit)
        #drive_checkin
    
    check_and_script.short_description = "Check in system drives and execute selected script" 
    run_script.short_description = "Execute selected script"
    load_script.short_descripttion ="Load Iometer scripts"
    actions = [run_script, check_and_script, load_script]

class SystemsAdmin(admin.ModelAdmin):
    search_fields = ('controller','networkid', 'os')
    list_select_related = True
    list_display = ('modelname', 'systemname', 'configuration', 'online', 'busy')
    list_filter = ('controller',)
    #date_hierarchy = 'timestamp'
    ordering = ('systemname',)
   
    def check_availablity(self, request,queryset):
        #rows_updated = queryset.update(shipping=0)

        available = queryset
        ip=[]
        for h in queryset:
            ip.append((h.networkid).strip())            
            
        up = Pinger(ip)
        message_bit = up
        #if available == 1:
        #    message_bit = "1 system was"
        #else:
        #    message_bit = "%s systems were" % available
        self.message_user(request, "Test System online status %s " % message_bit)
        
        
    def run_drive_inquirycheck(self, request,queryset):
        check_in = queryset
        system_list=[]
        for obj in queryset:
            system_list.append((obj.networkid).strip())           
        
            server_name = 'http://' +  (obj.networkid).strip() + ':1332'
            print server_name
            server = xmlrpclib.ServerProxy(server_name, allow_none=True)
            server.drive_inquiry('Inquiry')
        if check_in == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" % check_in
        self.message_user(request, "%s successfully selected and executed." % message_bit)
        
    def drive_checkin(self, request,queryset):
        check_in = queryset
        system_list=[]
        for obj in queryset:
            system_list.append((obj.networkid).strip())           
        
            server_name = 'http://' +  (obj.networkid).strip() + ':1332'
            print server_name
            server = xmlrpclib.ServerProxy(server_name, allow_none=True)
            server.drive_mode_pages('CheckIn')
        if check_in == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" % check_in
        self.message_user(request, "%s successfully selected and executed." % message_bit)
        
    def drive_checkout(self, request,queryset):
        check_in = queryset
        system_list=[]
        for obj in queryset:
            system_list.append((obj.networkid).strip())           
        
            server_name = 'http://' +  (obj.networkid).strip() + ':1332'
            print server_name
            server = xmlrpclib.ServerProxy(server_name, allow_none=True)
            server.drive_mode_pages('CheckOut')
        if check_in == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" % check_in
        self.message_user(request, "%s successfully selected and executed." % message_bit)
    
    
    def run_system_check(self, request,queryset):
        check_in = queryset
        system_list=[]
        for obj in queryset:
            system_list.append((obj.networkid).strip())         
        
            server_name = 'http://' +  (obj.networkid).strip() + ':1332'
            print server_name
            server = xmlrpclib.ServerProxy(server_name, allow_none=True)
            server.system_query()
        if check_in == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" % check_in
        self.message_user(request, "%s successfully selected and executed." % message_bit)
    
    run_drive_inquirycheck.short_description = "Dell Inquiry Page"
    run_system_check.short_description = "Check current configuration"
    check_availablity.short_description = "Check availability"
    #drive_checkin.short_description = "Check In - Mode Pages"
    #drive_checkout.short_description = "Check Out - Mode Pages"
    #actions = [run_drive_check, run_system_check, drive_checkin, drive_checkout, check_availablity]
    actions = [run_drive_inquirycheck, run_system_check, check_availablity]


admin.site.register(Device, DeviceAdmin)
admin.site.register(Devicerev)
admin.site.register(Result, ResultAdmin)
admin.site.register(Test)
admin.site.register(Testrev, TestRevAdmin)
admin.site.register(Testscripts, TestscriptsAdmin)
admin.site.register(Systems, SystemsAdmin)
admin.site.register(Dellinqdata, DellinqdataAdmin)
admin.site.register(Codenames, CodenamesAdmin)


