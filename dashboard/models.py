# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Device(models.Model):
    memorytype = models.CharField(max_length=64, db_column=u'MemoryType', blank=True) # Field name made lowercase.
    manufacturer = models.CharField(max_length=64, db_column=u'Manufacturer', blank=True) # Field name made lowercase.
    modelnumber = models.CharField(max_length=64, db_column=u'ModelNumber') # Field name made lowercase.
    delleqlpn = models.CharField(max_length=64, db_column=u'DellEQLPN', blank=True) # Field name made lowercase.
    firmware = models.CharField(max_length=64, db_column=u'Firmware', blank=True) # Field name made lowercase.
    serialnumber = models.CharField(max_length=64, db_column=u'SerialNumber') # Field name made lowercase.
    ppid = models.CharField(max_length=64, db_column=u'PPID', blank=True) # Field name made lowercase.
    interfacetype = models.CharField(max_length=8, db_column=u'InterfaceType', blank=True) # Field name made lowercase.
    interfacespeed = models.IntegerField(null=True, db_column=u'InterfaceSpeed', blank=True) # Field name made lowercase.
    capacity = models.CharField(max_length=64, db_column=u'Capacity', blank=True) # Field name made lowercase.
    formfactor = models.FloatField(null=True, db_column=u'FormFactor', blank=True) # Field name made lowercase.
    height = models.FloatField(null=True, db_column=u'Height', blank=True) # Field name made lowercase.
    spinspeed = models.IntegerField(null=True, db_column=u'SpinSpeed', blank=True) # Field name made lowercase.
    parrallepaths = models.IntegerField(null=True, db_column=u'ParrallePaths', blank=True) # Field name made lowercase.
    shipping = models.BooleanField(null=True, db_column=u'Shipping', blank=True) # Field name made lowercase.
    supportdup = models.BooleanField(null=True, db_column=u'SupportDUP', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Device'

class Test(models.Model):
    testname = models.CharField(max_length=64, db_column=u'TestName') # Field name made lowercase.
    script = models.CharField(max_length=265, db_column=u'Script', blank=True) # Field name made lowercase.
    system = models.CharField(max_length=64, db_column=u'System', blank=True) # Field name made lowercase.
    controller = models.CharField(max_length=64, db_column=u'Controller', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Test'

class Result(models.Model):
    timestamp = models.CharField(max_length=64, db_column=u'Timestamp', blank=True) # Field name made lowercase.
    serialnumber = models.CharField(max_length=64, db_column=u'SerialNumber') # Field name made lowercase.
    rawdata = models.CharField(max_length=265, db_column=u'RawData', blank=True) # Field name made lowercase.
    reports = models.CharField(max_length=265, db_column=u'Reports', blank=True) # Field name made lowercase.
    ppid = models.CharField(max_length=64, db_column=u'PPID', blank=True) # Field name made lowercase.
    modelnumber = models.CharField(max_length=64, db_column=u'ModelNumber') # Field name made lowercase.
    rev_id = models.IntegerField(null=True, blank=True)
    testname = models.CharField(max_length=64, db_column=u'TestName') # Field name made lowercase.
    key = models.AutoField()
    key1 = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'Result'

class Devicerev(models.Model):
    fwrev = models.CharField(max_length=64, db_column=u'FWRev', blank=True) # Field name made lowercase.
    modelnumber = models.CharField(max_length=64, db_column=u'ModelNumber') # Field name made lowercase.
    key1 = models.AutoField()
    class Meta:
        db_table = u'DeviceRev'

class Testrev(models.Model):
    script = models.CharField(max_length=265, db_column=u'Script', blank=True) # Field name made lowercase.
    system = models.CharField(max_length=64, db_column=u'System', blank=True) # Field name made lowercase.
    controller = models.CharField(max_length=64, db_column=u'Controller', blank=True) # Field name made lowercase.
    analysis = models.CharField(max_length=64, db_column=u'Analysis', blank=True) # Field name made lowercase.
    id = models.AutoField()
    testname = models.CharField(max_length=64, db_column=u'TestName') # Field name made lowercase.
    class Meta:
        db_table = u'TestRev'

