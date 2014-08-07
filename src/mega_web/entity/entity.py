from django.db import models


class Server(models.Model):
    class Meta(object):
        db_table='server'
      
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    os = models.CharField(max_length=50)
    owner = models.CharField(max_length=50)
    online_date = models.DateTimeField(default=0)
    stat= models.IntegerField(default=1)

class Instance(models.Model):
    class Meta(object):
        db_table='instance'
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50) 
    server_id =  models.IntegerField(null=False)
    ip = models.CharField(max_length=20)    
    port = models.IntegerField(null=False)
    owner =  models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    business_id = models.IntegerField(default=0)
    #mysql oracle etc
    db_type = models.CharField(max_length=10)
    #none mha mmm keepalived
    ha_type = models.CharField(max_length=10)
    #1 master >1 slave
    role= models.IntegerField(default=1)
    
    version = models.CharField(max_length=20)
    
    stat= models.IntegerField(default=1)
    online_date = models.DateTimeField(default=0)


class Database(models.Model):
    class Meta(object):
        db_table='databases'
    
    id = models.AutoField(primary_key=True)
    instance_id = models.IntegerField(null=False)
    name = models.CharField(max_length=16)
    business_id = models.IntegerField()
    level = models.IntegerField()
    owner = models.IntegerField()
    stat= models.IntegerField(default=1)
    online_date = models.DateTimeField(default=0)


class User(models.Model):
    class Meta(object):
        db_table='user'
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32) 
    #dba op diaosi
    role = models.IntegerField()
    sign = models.IntegerField()
    pwd =  models.CharField(max_length=10)
    p_id = models.IntegerField()
    phone = models.IntegerField()
    stat= models.IntegerField(default=1)
    
class Business(models.Model):
    class Meta(object):
        db_table='business'
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16) 
    owner = models.IntegerField()
    phone = models.IntegerField()
    stat= models.IntegerField(default=1)

class Backup_History_Info(models.Model):
    class Meta(object):
        db_table='backup_history_info'
     
class Backup_Policy(models.Model):
    class Meta(object):
        db_table='backup_policy'
    id = models.AutoField(primary_key=True)
    host_ip=models.CharField(max_length=20)
    port=models.IntegerField(default=0)
    db_type=models.CharField(max_length=20)
    backup_tool=models.CharField(max_length=20)
    backup_level=models.CharField(max_length=20)
    level_value=models.CharField(max_length=8000)
    backup_type=models.CharField(max_length=20)
    need_data=models.CharField(max_length=2)
    need_schema=models.CharField(max_length=2)
    iscompressed=models.CharField(max_length=2)
    isencrypted=models.CharField(max_length=2)
    retention=models.IntegerField()
    is_schedule=models.IntegerField()
    cycle=models.CharField(max_length=20)
    backup_time=models.CharField(max_length=45)
    schedule_time=models.CharField(max_length=45)
    modify_time=models.DateTimeField(auto_now=True)
    
class Users(models.Model):
    class Meta(object):
        db_table='user'
    
    id = models.AutoField(primary_key=True)   
    name=models.CharField(max_length=20)
    role=models.CharField(max_length=20)
    sign=models.CharField(max_length=20)
    pwd=models.CharField(max_length=20)
    p_id=models.IntegerField(default=1)
    phone=models.IntegerField()
    stat=models.IntegerField()
    
    
class Document(models.Model):
    class Meta(object):
        db_table='document'
    file = models.FileField(upload_to='documents/%Y/%m/%d')   

class Task(models.Model):
    class Meta(object):
        db_table='task'
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20)
    type=models.IntegerField(default=1)
    value=models.CharField(max_length=100)
    last_time=models.DateTimeField()
    cycle=models.IntegerField(default=1)
    target=models.CharField(max_length=200)
    owner=models.IntegerField(default=1)
    script=models.CharField(max_length=50)
    stat=models.IntegerField(default=1)
    create_time=models.DateTimeField(auto_now=True)

class Client(models.Model):
    class Meta(object):
        db_table='client'
    server_id=models.IntegerField(primary_key=True)
    version=models.CharField(max_length=20)
    heartbeat=models.DateTimeField(auto_now=True)