# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.utils.safestring import mark_safe

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
import django_filters


SHIPPING_CHOICES = (
    ('1', 'Shipping' ),
    ('0', 'Not Shipping'),
)

DUP_CHOICES = (
    ('1', 'DUP Supported'),
    ('0', 'DUP Not Supported'),
)

ONLINE_CHOICES = (
    ('1', 'Available' ),
    ('0', 'Unavailable'),
)

BUSY_CHOICES = (
    ('1', 'Available' ),
    ('0', 'Unavailable'),
)
class Systems(models.Model):
    system_id = models.AutoField(primary_key=True)
    systemname = models.CharField(max_length=64, db_column=u'SystemName', blank=True) # Field name made lowercase.
    controller = models.CharField(max_length=64, db_column=u'Controller', blank=True) # Field name made lowercase.
    os = models.CharField(max_length=64, db_column=u'OS', blank=True) # Field name made lowercase.
    cpu = models.CharField(max_length=64, db_column=u'CPU', blank=True) # Field name made lowercase.
    ram = models.CharField(max_length=64, db_column=u'RAM', blank=True) # Field name made lowercase.
    hdd = models.CharField(max_length=64, db_column=u'HDD', blank=True) # Field name made lowercase.
    networkid = models.CharField(max_length=64, db_column=u'NetworkID', blank=True) # Field name made lowercase.
    modelname = models.CharField(max_length=64, db_column=u'ModelName', blank=True) # Field name made lowercase.
    configuration = models.TextField(db_column=u'Configuration', blank=True) # Field name made lowercase.
    online = models.BooleanField(null=False, db_column=u'Online', blank=True) # Field name made lowercase.
    busy = models.BooleanField(null=False, db_column=u'Busy', blank=True) # Field name made lowercase.

    
    # ...
    def __unicode__(self):
        system =  self.modelname + self.controller + self.networkid 
        return system

    class Meta:
        db_table = u'Systems'
        ordering = ['systemname']

        

class Dellinqdata(models.Model):
    timestamp = models.CharField(max_length=64, db_column=u'Timestamp', blank=True) # Field name made lowercase.
    venderid = models.CharField(max_length=64, db_column=u'VenderID') # Field name made lowercase.
    productid = models.CharField(max_length=64, db_column=u'ProductID') # Field name made lowercase.
    firmwarerevisionlevel = models.CharField(max_length=64, db_column=u'FirmwareRevisionLevel', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    productserialnumber = models.CharField(max_length=64, db_column=u'ProductSerialNumber', blank=True) # Field name made lowercase.
    #targetdevicename = models.CharField(max_length=64, db_column=u'TargetDeviceName', blank=True) # Field name made lowercase.
    #targetportidentifier1 = models.CharField(max_length=64, db_column=u'TargetPortIdentifier1', blank=True) # Field name made lowercase.
    #targetportidentifier2 = models.CharField(max_length=64, db_column=u'TargetPortIdentifier2', blank=True) # Field name made lowercase.
    formfactorwidth = models.CharField(max_length=64, db_column=u'FormFactorWidth', blank=True) # Field name made lowercase.
    formfactorheight = models.CharField(max_length=64, db_column=u'FormFactorHeight', blank=True) # Field name made lowercase.
    deviceid = models.CharField(max_length=64, db_column=u'DeviceID', blank=True) # Field name made lowercase.
    servocodelevel = models.CharField(max_length=64, db_column=u'ServoCodeLevel', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    pcbaserialnumber = models.CharField(max_length=64, db_column=u'PCBASerialNumber', blank=True) # Field name made lowercase.
    pcbapartnumber = models.CharField(max_length=64, db_column=u'PCBAPartNumber', blank=True) # Field name made lowercase.
    diskmediavendor = models.CharField(max_length=64, db_column=u'DiskMediaVendor', blank=True) # Field name made lowercase.
    motorserialnumber = models.CharField(max_length=64, db_column=u'MotorSerialNumber', blank=True) # Field name made lowercase.
    flexcircuitassemblyserialnumber = models.CharField(max_length=64, db_column=u'FlexCircuitAssemblySerialNumber', blank=True) # Field name made lowercase.
    headvendor = models.CharField(max_length=64, db_column=u'HeadVendor', blank=True) # Field name made lowercase.
    hdcrevision = models.CharField(max_length=64, db_column=u'HDCRevision', blank=True) # Field name made lowercase.
    actuatorserialnumber = models.CharField(max_length=64, db_column=u'ActuatorSerialNumber', blank=True) # Field name made lowercase.
    headdiskassembly = models.CharField(max_length=64, db_column=u'HeadDiskAssembly', blank=True) # Field name made lowercase.
    yearofmanufacture = models.CharField(max_length=64, db_column=u'YearofManufacture', blank=True) # Field name made lowercase.
    weekofmanufacture = models.CharField(max_length=64, db_column=u'WeekofManufacture', blank=True) # Field name made lowercase.
    dayofmanufacture = models.CharField(max_length=64, db_column=u'DayofManufacture', blank=True) # Field name made lowercase.
    locationofmanufacture = models.CharField(max_length=64, db_column=u'LocationofManufacture', blank=True) # Field name made lowercase.
    dellppid = models.CharField(primary_key=True, max_length=64, db_column=u'DellPPID') # Field name made lowercase.
    mediumrotationrate = models.IntegerField(null=True, db_column=u'MediumRotationRate', blank=True) # Field name made lowercase.
    diff = models.CharField(max_length=64, db_column=u'Diff', blank=True) # Field name made lowercase.
    sed = models.CharField(max_length=64, db_column=u'SED', blank=True) # Field name made lowercase.
    key = models.AutoField(primary_key=True)
    #devicekey = models.CharField(default=Device, max_length=64, db_column=u'Devicekey') # Field name made lowercase.
    devicekey = models.CharField(max_length=64, db_column=u'Devicekey', blank=True) # Field name made lowercase.
    # ...
    def __unicode__(self):
        inquiry =  self.venderid + self.productid + self.dellppid + self.headdiskassembly 
        return inquiry
    

    class Meta:
        db_table = u'DELLInqData'
        ordering = ['productserialnumber']


class Testscripts(models.Model):
    script_id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=64, db_column=u'Author', blank=True) # Field name made lowercase.
    description = models.CharField(max_length=264, db_column=u'Description', blank=True) # Field name made lowercase.
    scriptref = models.CharField(max_length=800, db_column=u'ScriptRef', blank=True) # Field name made lowercase.
    #scriptref = models.FilePathField(path="\\\\hddlab\\FileShare\\Test_Libary\\Perf_scripts\\") #(max_length=800, db_column=u'ScriptRef', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=64, db_column=u'Type', blank=True) # Field name made lowercase.
    duration = models.CharField(max_length=264, db_column=u'Duration', blank=True) # Field name made lowercase.
    devicetype = models.CharField(max_length=64, db_column=u'DeviceType', blank=True) # Field name made lowercase.
    networkid = models.CharField(max_length=64, db_column=u'NetworkID', blank=True) # Field name made lowercase.
    multidevice = models.BooleanField(null=False, db_column=u'MultiDevice', blank=True) # Field name made lowercase.
    multithread = models.BooleanField(null=False, db_column=u'MultiThread', blank=True) # Field name made lowercase.
    # ...
    def __unicode__(self):
        script_lib =  self.type + self.author + self.description + self.scriptref 
        return script_lib

    class Meta:
        db_table = u'Testscripts'
        ordering = ['type']

class Devicerev(models.Model):
    fwrev = models.CharField(max_length=64, db_column=u'FWRev', blank=True) # Field name made lowercase.
    modelnumber = models.CharField(primary_key=True, max_length=64, db_column=u'ModelNumber') # Field name made lowercase.
    #key1 = models.IntegerField(null=True, db_column=u'key1')
    dellpartno = models.CharField(max_length=64, db_column=u'DellPartNo', blank=True) # Field name made lowercase.
    manufacturepartno = models.CharField(max_length=64, db_column=u'ManufacturePartNo', blank=True) # Field name made lowercase.
    codename = models.CharField(max_length=64, db_column=u'CodeName', blank=True) # Field name made lowercase.
        
    # ...
    def __unicode__(self):
        return self.fwrev + self.modelnumber
    
    class Meta:
        db_table = u'DeviceRev'

class Device(models.Model):
    memorytype = models.CharField(max_length=64, db_column=u'MemoryType', blank=True) # Field name made lowercase.
    manufacturer = models.CharField(max_length=64, db_column=u'Manufacturer', blank=True) # Field name made lowercase.
    modelnumber = models.CharField(max_length=264, db_column=u'ModelNumber') # Field name made lowercase.
    delleqlpn = models.CharField(max_length=64, db_column=u'DellEQLPN', blank=True) # Field name made lowercase.
    firmware = models.CharField(max_length=64, db_column=u'Firmware', blank=True) # Field name made lowercase.
    serialnumber = models.CharField(primary_key=True, max_length=264, db_column=u'SerialNumber') # Field name made lowercase.
    dellppid = models.CharField(max_length=64, db_column=u'DellPPID', blank=True) # Field name made lowercase.
    #dellppid = models.CharField(max_length=64, db_column=u'DellPPID', model=Dellinqdata)
    interfacetype = models.CharField(max_length=8, db_column=u'InterfaceType', blank=True) # Field name made lowercase.
    interfacespeed = models.IntegerField(null=True, db_column=u'InterfaceSpeed', blank=True) # Field name made lowercase.
    capacity = models.CharField(max_length=64, db_column=u'Capacity', blank=True) # Field name made lowercase.
    formfactor = models.FloatField(null=True, db_column=u'FormFactor', blank=True) # Field name made lowercase.
    height = models.FloatField(null=True, db_column=u'Height', blank=True) # Field name made lowercase.
    rpm = models.IntegerField(null=True, db_column=u'RPM', blank=True) # Field name made lowercase.
    parrallepaths = models.IntegerField(null=True, db_column=u'ParrallePaths', blank=True) # Field name made lowercase.
    windowslocation = models.CharField(max_length=264, db_column=u'WindowsLocation') # Field name made lowercase.
    shipping = models.BooleanField(null=False, db_column=u'Shipping', blank=True) # Field name made lowercase.
    supportdup = models.BooleanField(null=False, db_column=u'SupportDUP', blank=True) # Field name made lowercase.
    #id = models.IntegerField(null=True, db_column=u'Id', blank=True) # Field name made lowercase.
    # ...
    def __unicode__(self):
        device_drive =  self.memorytype + self.interfacetype + self.manufacturer + self.serialnumber + self.capacity + self.modelnumber
        return device_drive
    
    def report(self):
        return mark_safe(u'<a href="/admin/dashboarding/device/report/'+ str(self.serialnumber).strip() + ',' + str(self.modelnumber).strip() + '">VIEW</a>')
        
    report.allow_tags = True

    class Meta:
        db_table = u'Device'
        ordering = ['manufacturer']

class Test(models.Model):
    testname = models.CharField(max_length=64, db_column=u'TestName') # Field name made lowercase.
    script = models.CharField(max_length=265, db_column=u'Script', blank=True) # Field name made lowercase.
    system = models.CharField(max_length=64, db_column=u'System', blank=True) # Field name made lowercase.
    controller = models.CharField(max_length=64, db_column=u'Controller', blank=True) # Field name made lowercase.
    test_id = models.AutoField(primary_key=True) # Field name made lowercase.
    
    # ...
    def __unicode__(self):
        test_info =  self.testname + self.script 
        return test_info
    
    class Meta:
        db_table = u'Test'

class Result(models.Model):
    timestamp = models.DateTimeField(max_length=164, db_column=u'Timestamp', blank=True) # Field name made lowercase.
    #serialnumber = models.CharField(max_length=64, db_column=u'SerialNumber') # Field name made lowercase.
    serialnumber = models.TextField(db_column=u'SerialNumber', blank=True) # Field name made lowercase. This field type is a guess.
    rawdata = models.CharField(max_length=365, db_column=u'RawData', blank=True) # Field name made lowercase.
    reports = models.CharField(max_length=365, db_column=u'Reports', blank=True) # Field name made lowercase.
    ppid = models.CharField(max_length=64, db_column=u'PPID', blank=True) # Field name made lowercase.
    modelnumber = models.CharField(max_length=264, db_column=u'ModelNumber') # Field name made lowercase.
    #modelnumber = models.OneToOneField(Device)
    firmware = models.CharField(max_length=64, db_column=u'Firmware', blank=True) # Field name made lowercase.
    #rev_id = models.IntegerField(null=True, blank=True)
    memorytype = models.CharField(max_length=64, db_column=u'MemoryType') # Field name made lowercase.
    vendor = models.CharField(max_length=264, db_column=u'Vendor') # Field name made lowercase.
    capacity = models.CharField(max_length=64, db_column=u'Capacity') # Field name made lowercase.
    testname = models.CharField(max_length=264, db_column=u'TestName') # Field name made lowercase.
    key = models.AutoField(primary_key=True)
    #key1 = models.IntegerField(null=True, blank=True)
    raw = models.TextField(db_column=u'Raw', blank=True) # Field name made lowercase. This field type is a guess.
    rts = models.DateTimeField(max_length=164, db_column=u'RTS', blank=True) # Field name made lowercase.
    rtsminus = models.DateTimeField(max_length=164, db_column=u'RTSMinus', blank=True) # Field name made lowercase.
    codename = models.CharField(max_length=264, db_column=u'CodeName', blank=True) # Field name made lowercase.
    formfactor = models.FloatField(null=True, db_column=u'FormFactor', blank=True) # Field name made lowercase.
    rpm = models.IntegerField(null=True, db_column=u'RPM', blank=True) # Field name made lowercase.
    #firmware = models.CharField(max_length=64, db_column=u'Firmware', blank=True) # Field name made lowercase.
    
    # ...
    def __unicode__(self):
        results_info =  self.testname + self.modelnumber + self.serialnumber +  str(self.timestamp)
        return results_info
    
    class Meta:
        db_table = u'Result'
        ordering = ['timestamp']
        
        
class Codenames(models.Model):
    modelnumber = models.CharField(max_length=264, db_column=u'ModelNumber', blank=True) # Field name made lowercase.
    codename = models.CharField(max_length=264, db_column=u'CodeName', blank=True) # Field name made lowercase.
    vendor = models.CharField(max_length=264, db_column=u'Vendor', blank=True) # Field name made lowercase.
    key = models.AutoField(primary_key=True)
   
    def __unicode__(self):
        name_info =  self.codename + self.vendor + self.modelnumber 
        return name_info
    
    class Meta:
        db_table = u'CodeNames'
        ordering = ['codename']



class Testrev(models.Model):
    script = models.CharField(max_length=265, db_column=u'Script', blank=True) # Field name made lowercase.
    system = models.CharField(max_length=64, db_column=u'System', blank=True) # Field name made lowercase.
    controller = models.CharField(max_length=64, db_column=u'Controller', blank=True) # Field name made lowercase.
    analysis = models.CharField(max_length=64, db_column=u'Analysis', blank=True) # Field name made lowercase.
    testrev_id = models.AutoField(primary_key=True)
    testname = models.CharField(max_length=64, db_column=u'TestName') # Field name made lowercase.
    
    
    # ...
    def __unicode__(self):
        test_info =  self.controller + self.testname +  self.script 
        return test_info
    
    class Meta:
        db_table = u'TestRev'
        
   
class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Device
        fields = ['memorytype', 'modelnumber', 'firmware', 'capacity', 'interfacetype']

class DjangoContentType(models.Model):
    name = models.CharField(max_length=100)
    app_label = models.CharField(unique=True, max_length=100)
    model = models.CharField(unique=True, max_length=100)
    class Meta:
        db_table = u'django_content_type'

class AuthGroup(models.Model):
    #id = models.IntegerField()
    name = models.CharField(max_length=80)
    class Meta:
        db_table = u'auth_group'

class AuthGroupPermissions(models.Model):
    #id = models.IntegerField()
    group_id = models.IntegerField()
    permission_id = models.IntegerField()
    class Meta:
        db_table = u'auth_group_permissions'

class AuthMessage(models.Model):
    #id = models.IntegerField()
    user_id = models.IntegerField()
    message = models.TextField()
    class Meta:
        db_table = u'auth_message'

class AuthPermission(models.Model):
    #id_user = models.AutoField(primary_key=True) #.IntegerField()
    name = models.CharField(max_length=50)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)
    class Meta:
        db_table = u'auth_permission'

class AuthUser(models.Model):
    #id = models.IntegerField()
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    is_superuser = models.BooleanField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = u'auth_user'

class AuthUserGroups(models.Model):
    #id = models.IntegerField()
    user_id = models.IntegerField()
    group_id = models.IntegerField()
    class Meta:
        db_table = u'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    #id = models.IntegerField()
    user_id = models.IntegerField()
    permission_id = models.IntegerField()
    class Meta:
        db_table = u'auth_user_user_permissions'

        
class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = u'django_session'

class DjangoSite(models.Model):
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    class Meta:
        db_table = u'django_site'

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey(DjangoContentType, null=True, blank=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = u'django_admin_log'

"""class Testing(models.Model):
    name = models.TextField(blank=True)
    class Meta:
        db_table = u'testing'"""